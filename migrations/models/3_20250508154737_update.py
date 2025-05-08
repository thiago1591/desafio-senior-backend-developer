from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "chat_interactions" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "node_id" VARCHAR(100) NOT NULL,
    "user_selection" VARCHAR(255) NOT NULL,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "chat_session_id" INT NOT NULL REFERENCES "chat_sessions" ("id") ON DELETE CASCADE
);
        CREATE TABLE IF NOT EXISTS "chat_sessions" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "current_node_id" VARCHAR(100) NOT NULL,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "last_interaction_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "is_active" BOOL NOT NULL DEFAULT True,
    "user_id" INT NOT NULL REFERENCES "users" ("id") ON DELETE CASCADE
);
        CREATE TABLE IF NOT EXISTS "chatbot_nodes" (
    "id" VARCHAR(100) NOT NULL PRIMARY KEY,
    "parent_id" VARCHAR(100),
    "type" VARCHAR(4) NOT NULL,
    "message" TEXT NOT NULL,
    "options" JSONB NOT NULL
);
COMMENT ON COLUMN "chatbot_nodes"."type" IS 'ROOT: root\nMENU: menu\nLEAF: leaf';"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "chat_interactions";
        DROP TABLE IF EXISTS "chatbot_nodes";
        DROP TABLE IF EXISTS "chat_sessions";"""
