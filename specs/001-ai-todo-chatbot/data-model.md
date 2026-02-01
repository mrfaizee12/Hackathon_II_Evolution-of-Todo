# Data Model: AI Todo Chatbot

## Overview
This document defines the data models for the AI Todo Chatbot feature, including entity definitions, relationships, and validation rules.

## Entity: AIConversation

Represents a session of interaction between user and AI assistant, including message history and context.

**Fields:**
- id: UUID (primary key)
- user_id: UUID (foreign key to user)
- title: String (summary of conversation topic)
- created_at: DateTime
- updated_at: DateTime
- is_active: Boolean (whether conversation is ongoing)

**Validation Rules:**
- user_id must reference existing user
- title must not exceed 200 characters
- created_at and updated_at are automatically managed

**Relationships:**
- One-to-many with AIMessage (conversation contains many messages)

## Entity: AIMessage

Represents individual messages exchanged between user and AI assistant.

**Fields:**
- id: UUID (primary key)
- conversation_id: UUID (foreign key to AIConversation)
- sender_type: Enum (USER or ASSISTANT)
- content: Text (the actual message content)
- message_type: Enum (TEXT, ACTION_REQUEST, ACTION_RESULT, SYSTEM)
- metadata: JSON (additional context like tool calls, parameters)
- created_at: DateTime

**Validation Rules:**
- conversation_id must reference existing conversation
- sender_type must be either USER or ASSISTANT
- content must not exceed 10,000 characters
- message_type must be one of the defined enum values

**Relationships:**
- Many-to-one with AIConversation (message belongs to one conversation)

## Entity: TodoAction

Represents actions performed on todo items through AI commands.

**Fields:**
- id: UUID (primary key)
- conversation_id: UUID (foreign key to AIConversation)
- message_id: UUID (foreign key to AIMessage that triggered this action)
- action_type: Enum (ADD, UPDATE, DELETE, COMPLETE, LIST)
- todo_details: JSON (details about the todo being acted upon)
- status: Enum (PENDING, PROCESSING, COMPLETED, FAILED)
- result: Text (result of the action, if applicable)
- created_at: DateTime

**Validation Rules:**
- conversation_id must reference existing conversation
- message_id must reference existing message
- action_type must be one of the defined enum values
- status must be one of the defined enum values

**Relationships:**
- Many-to-one with AIConversation (action belongs to conversation)
- Many-to-one with AIMessage (action triggered by specific message)

## Entity: Todo (Extending Existing Model)

Extends the existing Todo entity with additional fields for AI integration.

**Additional Fields:**
- ai_generated: Boolean (indicates if todo was created via AI)
- ai_context: Text (context from AI conversation that created this todo)

**Validation Rules:**
- Existing validation rules continue to apply
- ai_context must not exceed 500 characters

**Relationships:**
- No new relationships - extends existing Todo model

## Indexes

- AIConversation.user_id: Index for efficient user-based queries
- AIConversation.created_at: Index for chronological ordering
- AIMessage.conversation_id: Index for conversation-based queries
- AIMessage.created_at: Index for chronological ordering
- TodoAction.conversation_id: Index for conversation-based queries
- TodoAction.message_id: Index for message-based queries