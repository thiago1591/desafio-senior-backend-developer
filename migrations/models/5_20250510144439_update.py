from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "chatbot_states" ALTER COLUMN "last_intent" TYPE SMALLINT USING "last_intent"::SMALLINT;
        COMMENT ON COLUMN "chatbot_states"."last_intent" IS 'CONSULTAR_SALDO: 1
CANCELAR_CARTAO: 2
SALVAR_DOCUMENTO: 3
VER_DOCUMENTOS: 4
PERGUNTA_LIVRE: 5';"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "chatbot_states" ALTER COLUMN "last_intent" TYPE VARCHAR(16) USING "last_intent"::VARCHAR(16);
        COMMENT ON COLUMN "chatbot_states"."last_intent" IS 'CONSULTAR_SALDO: consultar_saldo
CANCELAR_CARTAO: cancelar_cartao
SALVAR_DOCUMENTO: salvar_documento
VER_DOCUMENTOS: ver_documentos
PERGUNTA_LIVRE: pergunta_livre';"""
