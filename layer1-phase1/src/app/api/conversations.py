"""
Conversation API endpoints.
"""

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.conversation import (
    ConversationCreate,
    ConversationResponse,
    ConversationUpdate,
    MessageCreate,
    MessageResponse,
    ConversationAnalytics,
)
from app.services import conversation_service

router = APIRouter(prefix="/conversations", tags=["conversations"])


@router.post(
    "",
    response_model=ConversationResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new conversation",
)
async def create_conversation(
    conversation: ConversationCreate,
    db: AsyncSession = Depends(get_db),
):
    """
    Create a new conversation.
    
    - **title**: Optional title for the conversation
    """
    db_conversation = await conversation_service.create_conversation(
        db=db,
        conversation=conversation,
    )
    
    return db_conversation


@router.get(
    "",
    response_model=list[ConversationResponse],
    summary="List all conversations",
)
async def list_conversations(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(10, ge=1, le=100, description="Maximum number of records"),
    status_filter: Optional[str] = Query(None, description="Filter by status"),
    db: AsyncSession = Depends(get_db),
):
    """
    List all conversations with pagination.
    
    - **skip**: Number of records to skip (offset)
    - **limit**: Maximum number of records to return
    - **status_filter**: Optional filter by status (active, archived, deleted)
    """
    status_enum = None
    if status_filter:
        try:
            from app.models.conversation import ConversationStatus
            status_enum = ConversationStatus(status_filter.lower())
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid status. Must be one of: active, archived, deleted",
            )
    
    conversations = await conversation_service.get_conversations(
        db=db,
        skip=skip,
        limit=limit,
        status=status_enum,
    )
    
    return conversations


@router.get(
    "/{conversation_id}",
    response_model=ConversationResponse,
    summary="Get a conversation by ID",
)
async def get_conversation(
    conversation_id: int,
    db: AsyncSession = Depends(get_db),
):
    """
    Get a specific conversation by ID.
    
    - **conversation_id**: The ID of the conversation
    """
    conversation = await conversation_service.get_conversation(
        db=db,
        conversation_id=conversation_id,
    )
    
    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Conversation {conversation_id} not found",
        )
    
    return conversation


@router.patch(
    "/{conversation_id}",
    response_model=ConversationResponse,
    summary="Update a conversation",
)
async def update_conversation(
    conversation_id: int,
    conversation_update: ConversationUpdate,
    db: AsyncSession = Depends(get_db),
):
    """
    Update a conversation.
    
    - **conversation_id**: The ID of the conversation
    - **title**: Optional new title
    - **status**: Optional new status
    """
    conversation = await conversation_service.update_conversation(
        db=db,
        conversation_id=conversation_id,
        title=conversation_update.title,
        status=conversation_update.status,
    )
    
    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Conversation {conversation_id} not found",
        )
    
    return conversation


@router.delete(
    "/{conversation_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a conversation",
)
async def delete_conversation(
    conversation_id: int,
    db: AsyncSession = Depends(get_db),
):
    """
    Delete a conversation.
    
    - **conversation_id**: The ID of the conversation
    """
    success = await conversation_service.delete_conversation(
        db=db,
        conversation_id=conversation_id,
    )
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Conversation {conversation_id} not found",
        )
    
    return None


@router.post(
    "/{conversation_id}/messages",
    response_model=MessageResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Add a message to a conversation",
)
async def create_message(
    conversation_id: int,
    message: MessageCreate,
    db: AsyncSession = Depends(get_db),
):
    """
    Add a message to a conversation.
    
    - **conversation_id**: The ID of the conversation
    - **role**: Message role (user, assistant, system)
    - **content**: Message content
    """
    try:
        db_message = await conversation_service.create_message(
            db=db,
            conversation_id=conversation_id,
            message=message,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
    
    return db_message


@router.get(
    "/{conversation_id}/messages",
    response_model=list[MessageResponse],
    summary="Get messages from a conversation",
)
async def get_messages(
    conversation_id: int,
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(50, ge=1, le=200, description="Maximum number of records"),
    db: AsyncSession = Depends(get_db),
):
    """
    Get messages from a conversation.
    
    - **conversation_id**: The ID of the conversation
    - **skip**: Number of messages to skip
    - **limit**: Maximum number of messages to return
    """
    # Verify conversation exists
    conversation = await conversation_service.get_conversation(
        db=db,
        conversation_id=conversation_id,
    )
    
    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Conversation {conversation_id} not found",
        )
    
    messages = await conversation_service.get_messages_by_conversation(
        db=db,
        conversation_id=conversation_id,
        skip=skip,
        limit=limit,
    )
    
    return messages


@router.get(
    "/analytics/summary",
    response_model=ConversationAnalytics,
    summary="Get conversation analytics",
)
async def get_analytics(
    db: AsyncSession = Depends(get_db),
):
    """
    Get analytics summary for conversations.
    
    Returns statistics including:
    - Total conversations
    - Total messages
    - Active conversations
    - Average messages per conversation
    - Top conversations by message count
    """
    analytics = await conversation_service.get_conversation_analytics(db=db)
    return analytics
