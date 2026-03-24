"""
Pydantic schemas for request/response validation.
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict

from app.models.conversation import ConversationStatus, MessageRole


# Message Schemas
class MessageBase(BaseModel):
    """Base schema for messages."""
    
    role: MessageRole = Field(default=MessageRole.USER, description="Message role")
    content: str = Field(..., min_length=1, max_length=10000, description="Message content")


class MessageCreate(MessageBase):
    """Schema for creating a message."""
    
    pass


class MessageResponse(MessageBase):
    """Schema for message responses."""
    
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    conversation_id: int
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


# Conversation Schemas
class ConversationBase(BaseModel):
    """Base schema for conversations."""
    
    title: Optional[str] = Field(None, max_length=255, description="Conversation title")


class ConversationCreate(ConversationBase):
    """Schema for creating a conversation."""
    
    pass


class ConversationUpdate(BaseModel):
    """Schema for updating a conversation."""
    
    title: Optional[str] = Field(None, max_length=255)
    status: Optional[ConversationStatus] = None


class ConversationResponse(ConversationBase):
    """Schema for conversation responses."""
    
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    status: ConversationStatus
    created_at: datetime
    updated_at: datetime
    messages: Optional[list[MessageResponse]] = None


# Analytics Schema
class ConversationAnalytics(BaseModel):
    """Schema for conversation analytics."""
    
    total_conversations: int
    total_messages: int
    active_conversations: int
    avg_messages_per_conversation: float
    top_conversations: list[dict]
