"""
Chat API endpoints with streaming support.
"""

import json
from typing import Optional
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query, Request
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
import uuid

from app.core.database import get_db
from app.core.config import get_settings
from app.services.llm.client import create_llm_client
from app.services.llm.provider import LLMError
from app.services import conversation_service
from app.schemas.conversation import MessageCreate, MessageResponse
from app.models.conversation import MessageRole

settings = get_settings()
router = APIRouter(prefix="/chat", tags=["chat"])


@router.post(
    "",
    response_model=MessageResponse,
    summary="Chat with LLM",
)
async def chat(
    message: str = Query(..., description="User message"),
    conversation_id: Optional[int] = Query(None, description="Existing conversation ID"),
    model: Optional[str] = Query(None, description="Model to use"),
    db: AsyncSession = Depends(get_db),
):
    """
    Chat with an LLM.
    
    - **message**: User message
    - **conversation_id**: Optional existing conversation ID (creates new if not provided)
    - **model**: Optional model override
    """
    try:
        llm = create_llm_client(model=model)
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )
    
    # Create or get conversation
    if conversation_id:
        conversation = await conversation_service.get_conversation(db, conversation_id)
        if not conversation:
            raise HTTPException(404, f"Conversation {conversation_id} not found")
    else:
        conversation = await conversation_service.create_conversation(
            db,
            type("ConversationCreate", (), {"title": None})(),
        )
    
    # Save user message
    user_message = await conversation_service.create_message(
        db=db,
        conversation_id=conversation.id,
        message=MessageCreate(role=MessageRole.USER, content=message),
    )
    
    # Get LLM response
    try:
        response = await llm.complete(prompt=message)
    except LLMError as e:
        raise HTTPException(500, detail=f"LLM error: {e.message}")
    
    # Save assistant response
    assistant_message = await conversation_service.create_message(
        db=db,
        conversation_id=conversation.id,
        message=MessageCreate(role=MessageRole.ASSISTANT, content=response.content),
        token_count=response.tokens_out,
        cost_usd=response.cost_usd,
        model_name=response.model,
    )
    
    return assistant_message


@router.post(
    "/stream",
    summary="Chat with LLM (Streaming)",
)
async def chat_stream(
    message: str = Query(..., description="User message"),
    conversation_id: Optional[int] = Query(None, description="Existing conversation ID"),
    model: Optional[str] = Query(None, description="Model to use"),
    db: AsyncSession = Depends(get_db),
):
    """
    Chat with an LLM using Server-Sent Events (SSE) streaming.
    
    - **message**: User message
    - **conversation_id**: Optional existing conversation ID
    - **model**: Optional model override
    """
    try:
        llm = create_llm_client(model=model)
    except ValueError as e:
        raise HTTPException(400, detail=str(e))
    
    # Create or get conversation
    if conversation_id:
        conversation = await conversation_service.get_conversation(db, conversation_id)
        if not conversation:
            raise HTTPException(404, f"Conversation {conversation_id} not found")
    else:
        conversation = await conversation_service.create_conversation(
            db,
            type("ConversationCreate", (), {"title": None})(),
        )
    
    # Save user message
    await conversation_service.create_message(
        db=db,
        conversation_id=conversation.id,
        message=MessageCreate(role=MessageRole.USER, content=message),
    )
    
    # Create placeholder for assistant message
    request_id = str(uuid.uuid4())
    
    async def generate():
        """Generate SSE stream."""
        full_content = ""
        tokens_out = 0
        model_name = llm.config.model
        
        try:
            async for chunk in llm.stream(prompt=message):
                if chunk.content:
                    full_content += chunk.content
                    # Send SSE format
                    yield f"data: {json.dumps({'content': chunk.content, 'request_id': request_id})}\n\n"
                
                if chunk.is_final:
                    # Save final message
                    from app.services.llm.tokens import count_tokens_openai
                    tokens_out = count_tokens_openai(full_content, model_name)
                    
                    await conversation_service.create_message(
                        db=db,
                        conversation_id=conversation.id,
                        message=MessageCreate(role=MessageRole.ASSISTANT, content=full_content),
                        token_count=tokens_out,
                        cost_usd=llm.calculate_cost(0, tokens_out),
                        model_name=model_name,
                    )
                    
                    # Send final marker
                    yield f"data: {json.dumps({'done': True, 'request_id': request_id})}\n\n"
                    
        except LLMError as e:
            yield f"data: {json.dumps({'error': e.message, 'request_id': request_id})}\n\n"
        
        # Signal end of stream
        yield "data: [DONE]\n\n"
    
    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Request-ID": request_id,
        },
    )


@router.get(
    "/costs",
    summary="Get LLM cost summary",
)
async def get_cost_summary(
    conversation_id: Optional[int] = Query(None, description="Filter by conversation"),
    db: AsyncSession = Depends(get_db),
):
    """
    Get LLM cost summary.
    
    - **conversation_id**: Optional filter by conversation
    """
    from sqlalchemy import select, func, sum
    from app.models.conversation import Message
    
    query = select(
        func.count(Message.id).label("total_messages"),
        sum(Message.token_count).label("total_tokens"),
        sum(Message.cost_usd).label("total_cost"),
    ).where(Message.role == MessageRole.ASSISTANT)
    
    if conversation_id:
        query = query.where(Message.conversation_id == conversation_id)
    
    result = await db.execute(query)
    row = result.first()
    
    return {
        "total_messages": row.total_messages or 0,
        "total_tokens": row.total_tokens or 0,
        "total_cost_usd": round(float(row.total_cost or 0), 6),
    }
