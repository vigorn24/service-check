# в файле доставем переменные из файла .env

from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

    """ 
    RABBITMQ_URL = os.getenv("RABBITMQ_URL", "amqp://guest:guest@localhost/")
    MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017/")
    MONGODB_DB = os.getenv("MONGODB_DB", "test_db")
    KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
    KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "test_topic")
    """

config = Config()