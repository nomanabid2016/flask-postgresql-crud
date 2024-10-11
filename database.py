import uuid

from sqlalchemy import Boolean, Column, DateTime, MetaData, create_engine
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func

from config import Config

# Create a postgres engine instance
engine = create_engine(
    Config.DB.CONNECTION_STR, pool_size=int(Config.DB.POOL_SIZE), max_overflow=0
)

Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

metadata = MetaData()
Base = declarative_base(metadata=metadata)


class BaseModel(Base):
    __abstract__ = True

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    is_active = Column(Boolean, default=True)

    def model_dump(self, update_dict: dict):
        for key, value in update_dict.items():
            if hasattr(self, key):
                setattr(self, key, value)