from sqlalchemy import Column, Integer, ForeignKey, TIMESTAMP, func, Text
from sqlalchemy.orm import relationship

from db.base_class import Base
from models import Storage


class Post(Base):
    id = Column(Integer, primary_key=True, index=True)
    profile_id = Column(Integer, ForeignKey('profile.id', ondelete='CASCADE'), nullable=False)
    text = Column(Text, nullable=False, default='')
    file_uuid = Column(ForeignKey(Storage.uuid), nullable=True)
    created = Column(TIMESTAMP, server_default=func.now())

    profile = relationship('Profile', back_populates='posts')
    likes = relationship('Like', back_populates='post', cascade='all, delete-orphan')
