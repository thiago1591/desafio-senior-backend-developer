from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "transport_cards" ALTER COLUMN "balance" TYPE INT USING "balance"::INT;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "transport_cards" ALTER COLUMN "balance" TYPE DECIMAL(10,2) USING "balance"::DECIMAL(10,2);
        ALTER TABLE "transport_cards" ALTER COLUMN "balance" TYPE DECIMAL(10,2) USING "balance"::DECIMAL(10,2);"""
