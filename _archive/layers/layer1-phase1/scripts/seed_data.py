"""
Seed database with sample data for testing.

Usage:
    python scripts/seed_data.py
"""

import asyncio
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy import select
import random

from app.core.config import get_settings
from app.models.conversation import Conversation, Message, ConversationStatus, MessageRole

settings = get_settings()


# Sample data
SAMPLE_TITLES = [
    "Python Best Practices",
    "FastAPI Questions",
    "Database Design Discussion",
    "API Architecture",
    "Testing Strategies",
    "Docker Configuration",
    "CI/CD Pipeline Setup",
    "Code Review Tips",
    "Performance Optimization",
    "Security Best Practices",
]

SAMPLE_MESSAGES = [
    {"role": MessageRole.USER, "content": "What are the best practices for Python async/await?"},
    {"role": MessageRole.ASSISTANT, "content": "Here are key best practices for async/await in Python:\n\n1. Use `async def` for functions that perform I/O operations\n2. Always `await` coroutines\n3. Use `asyncio.gather()` for concurrent execution\n4. Handle exceptions in async code\n5. Use `asyncio.sleep()` instead of `time.sleep()`"},
    {"role": MessageRole.USER, "content": "How do I handle errors in async code?"},
    {"role": MessageRole.ASSISTANT, "content": "Error handling in async code follows similar patterns to sync code:\n\n1. Use try/except blocks around await calls\n2. Catch specific exceptions when possible\n3. Use asyncio.gather() with return_exceptions=True for batch operations\n4. Consider using context managers for resource cleanup"},
    {"role": MessageRole.USER, "content": "Can you explain FastAPI dependency injection?"},
    {"role": MessageRole.ASSISTANT, "content": "FastAPI's dependency injection system allows you to:\n\n1. Create reusable components with `Depends()`\n2. Share database sessions across endpoints\n3. Handle authentication centrally\n4. Validate request parameters\n5. Test components in isolation"},
]


async def seed_database():
    """Seed database with sample conversations and messages."""
    
    # Create engine and session
    database_url = settings.database_url or f"postgresql+asyncpg://{settings.postgres_user}:{settings.postgres_password}@{settings.postgres_host}:{settings.postgres_port}/{settings.postgres_db}"
    
    engine = create_async_engine(database_url, echo=True)
    AsyncSessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    async with AsyncSessionLocal() as session:
        # Check if data already exists
        result = await session.execute(select(Conversation))
        existing = result.scalars().first()
        
        if existing:
            print("⚠️  Database already has data. Skipping seed.")
            return
        
        print("🌱 Seeding database with sample data...")
        
        # Create 10 conversations
        conversations = []
        for i, title in enumerate(SAMPLE_TITLES):
            conversation = Conversation(
                title=title,
                status=random.choice([ConversationStatus.ACTIVE, ConversationStatus.ACTIVE, ConversationStatus.ARCHIVED]),
            )
            session.add(conversation)
            conversations.append(conversation)
            
            # Add 2-5 messages to each conversation
            num_messages = random.randint(2, 5)
            for j in range(num_messages):
                if j < len(SAMPLE_MESSAGES):
                    msg_data = SAMPLE_MESSAGES[j]
                else:
                    msg_data = {
                        "role": MessageRole.USER if j % 2 == 0 else MessageRole.ASSISTANT,
                        "content": f"Sample message {j+1} in conversation {i+1}",
                    }
                
                message = Message(
                    conversation_id=conversation.id,
                    role=msg_data["role"],
                    content=msg_data["content"],
                    token_count=random.randint(50, 500),
                    cost_usd=round(random.uniform(0.0001, 0.001), 6),
                    model_name=random.choice(["gpt-3.5-turbo", "gpt-4", "claude-3-haiku"]),
                )
                session.add(message)
            
            await session.flush()
        
        await session.commit()
        
        print(f"✅ Seeded {len(conversations)} conversations with messages")
        
        # Print summary
        result = await session.execute(
            select(Conversation).order_by(Conversation.created_at.desc())
        )
        conversations = result.scalars().all()
        
        print("\n📊 Summary:")
        for conv in conversations:
            result = await session.execute(
                select(Message).where(Message.conversation_id == conv.id)
            )
            msg_count = len(result.scalars().all())
            print(f"  - {conv.title}: {msg_count} messages ({conv.status.value})")


def main():
    """Main seed function."""
    print("="*60)
    print("DATABASE SEED SCRIPT")
    print("="*60)
    print()
    
    try:
        asyncio.run(seed_database())
        print("\n✅ Seed completed successfully!")
    except Exception as e:
        print(f"\n❌ Seed failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
