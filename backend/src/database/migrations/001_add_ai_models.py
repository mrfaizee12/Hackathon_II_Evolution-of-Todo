"""
Migration script to add AI-related models to the database.
This includes AIConversation, AIMessage, and TodoAction tables.
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
import uuid


# Revision identifiers
revision = '001_add_ai_models'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    """
    Create tables for AI-related models:
    - aiconversation: Stores AI conversation sessions
    - aimessage: Stores individual messages in conversations
    - todoaction: Stores actions performed on todos via AI
    """

    # Create AIConversation table
    op.create_table(
        'aiconversation',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False, default=sa.text('gen_random_uuid()')),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('title', sa.String(length=200), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('now()')),
        sa.Column('is_active', sa.Boolean, nullable=False, default=True),
        sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    # Create AIMessage table
    op.create_table(
        'aimessage',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False, default=sa.text('gen_random_uuid()')),
        sa.Column('conversation_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('sender_type', sa.String(length=20), nullable=False),  # USER or ASSISTANT
        sa.Column('content', sa.Text, nullable=False, server_default=''),
        sa.Column('message_type', sa.String(length=30), nullable=False, default='TEXT'),  # TEXT, ACTION_REQUEST, etc.
        sa.Column('extra_metadata', postgresql.JSONB, nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('now()')),
        sa.ForeignKeyConstraint(['conversation_id'], ['aiconversation.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    # Create TodoAction table
    op.create_table(
        'todoaction',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False, default=sa.text('gen_random_uuid()')),
        sa.Column('conversation_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('message_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('action_type', sa.String(length=20), nullable=False),  # ADD, UPDATE, DELETE, COMPLETE, LIST
        sa.Column('todo_details', postgresql.JSONB, nullable=True),
        sa.Column('status', sa.String(length=20), nullable=False, default='PENDING'),  # PENDING, PROCESSING, COMPLETED, FAILED
        sa.Column('result', sa.String(length=1000), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('now()')),
        sa.ForeignKeyConstraint(['conversation_id'], ['aiconversation.id'], ),
        sa.ForeignKeyConstraint(['message_id'], ['aimessage.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    # Add indexes for better performance
    op.create_index('ix_aiconversation_user_id', 'aiconversation', ['user_id'])
    op.create_index('ix_aiconversation_created_at', 'aiconversation', ['created_at'])
    op.create_index('ix_aimessage_conversation_id', 'aimessage', ['conversation_id'])
    op.create_index('ix_aimessage_created_at', 'aimessage', ['created_at'])
    op.create_index('ix_todoaction_conversation_id', 'todoaction', ['conversation_id'])
    op.create_index('ix_todoaction_message_id', 'todoaction', ['message_id'])


def downgrade():
    """
    Drop AI-related tables in reverse order to respect foreign key constraints.
    """
    op.drop_table('todoaction')
    op.drop_table('aimessage')
    op.drop_table('aiconversation')