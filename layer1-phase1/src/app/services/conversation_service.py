"""
CRUD operations for conversations and messages.
"""

from datetime import datetime
from typing import Optional

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.conversation import Conversation, Message, ConversationStatus, MessageRole
from app.schemas.conversation import ConversationCreate, MessageCreate


# Conversation CRUD
async def get_conversation(db: AsyncSession, conversation_id: int) -> Optional[Conversation]:
    """Get a conversation by ID."""
    result = await db.execute(
        select(Conversation).where(Conversation.id == conversation_id)
    )
    return result.scalar_one_or_none()


async def get_conversations(
    db: AsyncSession,
    skip: int = 0,
    limit: int = 10,
    status: Optional[ConversationStatus] = None,
) -> list[Conversation]:
    """Get all conversations with pagination and optional status filter."""
    query = select(Conversation)
    
    if status:
        query = query.where(Conversation.status == status)
    
    query = query.offset(skip).limit(limit).order_by(Conversation.created_at.desc())
    
    result = await db.execute(query)
    return list(result.scalars().all())


async def create_conversation(
    db: AsyncSession,
    conversation: ConversationCreate,
) -> Conversation:
    """Create a new conversation."""
    db_conversation = Conversation(
        title=conversation.title,
        status=ConversationStatus.ACTIVE,
    )
    
    db.add(db_conversation)
    await db.flush()  # Get the ID
    await db.refresh(db_conversation)
    
    return db_conversation


async def update_conversation(
    db: AsyncSession,
    conversation_id: int,
    title: Optional[str] = None,
    status: Optional[ConversationStatus] = None,
) -> Optional[Conversation]:
    """Update a conversation."""
    conversation = await get_conversation(db, conversation_id)
    
    if not conversation:
        return None
    
    if title is not None:
        conversation.title = title
    
    if status is not None:
        conversation.status = status
    
    conversation.updated_at = datetime.utcnow()
    
    await db.flush()
    await db.refresh(conversation)
    
    return conversation


async def delete_conversation(db: AsyncSession, conversation_id: int) -> bool:
    """Delete a conversation."""
    conversation = await get_conversation(db, conversation_id)
    
    if not conversation:
        return False
    
    await db.delete(conversation)
    await db.flush()
    
    return True


# Message CRUD
async def get_message(db: AsyncSession, message_id: int) -> Optional[Message]:
    """Get a message by ID."""
    result = await db.execute(select(Message).where(Message.id == message_id))
    return result.scalar_one_or_none()


async def create_message(
    db: AsyncSession,
    conversation_id: int,
    message: MessageCreate,
    token_count: Optional[int] = None,
    cost_usd: Optional[float] = None,
    model_name: Optional[str] = None,
) -> Message:
    """Create a new message in a conversation."""
    # Verify conversation exists
    conversation = await get_conversation(db, conversation_id)
    if not conversation:
        raise ValueError(f"Conversation {conversation_id} not found")
    
    db_message = Message(
        conversation_id=conversation_id,
        role=message.role,
        content=message.content,
        token_count=token_count,
        cost_usd=cost_usd,
        model_name=model_name,
    )
    
    db.add(db_message)
    await db.flush()
    await db.refresh(db_message)
    
    # Update conversation timestamp
    conversation.updated_at = datetime.utcnow()
    
    return db_message


async def get_messages_by_conversation(
    db: AsyncSession,
    conversation_id: int,
    skip: int = 0,
    limit: int = 50,
) -> list[Message]:
    """Get all messages for a conversation."""
    query = (
        select(Message)
        .where(Message.conversation_id == conversation_id)
        .order_by(Message.created_at.asc())
        .offset(skip)
        .limit(limit)
    )
    
    result = await db.execute(query)
    return list(result.scalars().all())


# Analytics
async def get_conversation_analytics(db: AsyncSession) -> dict:
    """Get conversation analytics."""
    # Total conversations
    total_conv_result = await db.execute(
        select(func.count(Conversation.id))
    )
    total_conversations = total_conv_result.scalar() or 0
    
    # Total messages
    total_msg_result = await db.execute(select(func.count(Message.id)))
    total_messages = total_msg_result.scalar() or 0
    
    # Active conversations
    active_result = await db.execute(
        select(func.count(Conversation.id)).where(
            Conversation.status == ConversationStatus.ACTIVE
        )
    )
    active_conversations = active_result.scalar() or 0
    
    # Average messages per conversation
    avg_messages = total_messages / total_conversations if total_conversations > 0 else 0.0
    
    # Top conversations by message count
    top_conv_query = (
        select(
            Conversation.id,
            Conversation.title,
            func.count(Message.id).label("message_count"),
        )
        .join(Message, Conversation.id == Message.conversation_id)
        .group_by(Conversation.id, Conversation.title)
        .order_by(func.count(Message.id).desc())
        .limit(5)
    )
    
    top_result = await db.execute(top_conv_query)
    top_conversations = [
        {"id": row.id, "title": row.title, "message_count": row.message_count}
        for row in top_result.all()
    ]
    
    return {
        "total_conversations": total_conversations,
        "total_messages": total_messages,
        "active_conversations": active_conversations,
        "avg_messages_per_conversation": round(avg_messages, 2),
        "top_conversations": top_conversations,
    }
