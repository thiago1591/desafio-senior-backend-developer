from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP INDEX IF EXISTS "uid_users_full_na_7cbdf3";
        CREATE TABLE IF NOT EXISTS "chatbot_states" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "last_intent" VARCHAR(16),
    "step" INT,
    "context" JSONB,
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "user_id" INT NOT NULL REFERENCES "users" ("id") ON DELETE CASCADE
);
COMMENT ON COLUMN "chatbot_states"."last_intent" IS 'CONSULTAR_SALDO: consultar_saldo\nCANCELAR_CARTAO: cancelar_cartao\nSALVAR_DOCUMENTO: salvar_documento\nVER_DOCUMENTOS: ver_documentos\nPERGUNTA_LIVRE: pergunta_livre';
        DROP TABLE IF EXISTS "chatbot_nodes";
        DROP TABLE IF EXISTS "chat_interactions";
        DROP TABLE IF EXISTS "chat_sessions";"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "chatbot_states";
        CREATE UNIQUE INDEX IF NOT EXISTS "uid_users_full_na_7cbdf3" ON "users" ("full_name");"""
