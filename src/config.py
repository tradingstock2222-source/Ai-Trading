import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    ENV = os.getenv("ENV", "development")
    LOG_LEVEL = os.getenv("LOG_LEVEL", "DEBUG")
    KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
    KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "market_ticks")
    KAFKA_GROUP_ID = os.getenv("KAFKA_GROUP_ID", "tick_persister")
    DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://ai_trader:ai_trader_pass@localhost:5432/ai_trading")

settings = Settings()
