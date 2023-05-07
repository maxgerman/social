from sqlalchemy import Column, Integer, ForeignKey, TIMESTAMP, func, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from db.base_class import Base
from models import Storage, User


class Post(Base):
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey(User.id, ondelete='CASCADE'), nullable=False)
    text = Column(Text, nullable=False, default='')
    file_uuid = Column(ForeignKey(Storage.uuid), nullable=True)
    created = Column(TIMESTAMP, server_default=func.now())
    user = relationship('User', back_populates='posts')
