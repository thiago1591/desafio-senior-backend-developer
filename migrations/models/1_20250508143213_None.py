from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "users" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "full_name" VARCHAR(50) NOT NULL UNIQUE,
    "email" VARCHAR(255) NOT NULL UNIQUE,
    "password" VARCHAR(128) NOT NULL,
    "birth_date" DATE,
    "cpf" VARCHAR(14) UNIQUE,
    "phone" VARCHAR(20),
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS "documents" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "document_type" VARCHAR(50) NOT NULL,
    "file_path" VARCHAR(255),
    "file_name" VARCHAR(255),
    "document_number" VARCHAR(50) NOT NULL,
    "uploaded_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "user_id" INT NOT NULL REFERENCES "users" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "transport_cards" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "balance" DECIMAL(10,2) NOT NULL DEFAULT 0,
    "card_number" VARCHAR(20) NOT NULL UNIQUE,
    "status" VARCHAR(20) NOT NULL DEFAULT 'active',
    "user_id" INT NOT NULL REFERENCES "users" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "transport_transaction_history" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "type" VARCHAR(8) NOT NULL,
    "amount" INT NOT NULL,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "card_id" INT NOT NULL REFERENCES "transport_cards" ("id") ON DELETE CASCADE
);
COMMENT ON COLUMN "transport_transaction_history"."type" IS 'RECHARGE: recharge\nDEBIT: debit';
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
