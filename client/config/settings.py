import os

from dotenv import load_dotenv

load_dotenv()


class BaseConfig:
    """Base configuration shared by all environments."""

    DEBUG = os.getenv("DEBUG", "False").lower() == "true"
    SECRET_KEY = os.getenv("SECRET_KEY", "super-secret-key")

    # gRPC Server Config
    GRPC_HOST = os.getenv("GRPC_SERVER_HOST", "localhost")
    GRPC_PORT = int(os.getenv("GRPC_SERVER_PORT", "50051"))
    GRPC_ADDRESS = f"{GRPC_HOST}:{GRPC_PORT}"

    # Flask Server Config
    FLASK_HOST = os.getenv("FLASK_HOST", "0.0.0.0")
    FLASK_PORT = int(os.getenv("FLASK_PORT", "5000"))


class DevelopmentConfig(BaseConfig):
    """Development environment config."""

    DEBUG = True


class ProductionConfig(BaseConfig):
    """Production environment config."""

    DEBUG = False


def get_config():
    """Return config class based on ENV variable."""
    env = os.getenv("FLASK_ENV", "development").lower()
    if env == "production":
        return ProductionConfig
    return DevelopmentConfig
