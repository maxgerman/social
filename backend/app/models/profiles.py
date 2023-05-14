import logging

from sqlalchemy import Column, Integer, String, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from db.base_class import Base
from models.likes import Like

logger = logging.getLogger(__name__)


class Profile(Base):
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=True)
    name = Column(String, nullable=False, default='')
    image_id = Column(UUID(as_uuid=True), nullable=True)
    gender = Column(String, Enum('MALE', 'FEMALE'), nullable=True)
    bio = Column(String, nullable=False, default='')

    user = relationship('User', back_populates='profile')
    posts = relationship('Post', back_populates='profile')
    likes_made = relationship('Like', back_populates='profile', foreign_keys=[Like.profile_id])
    following = relationship('Following', back_populates='profile_by', foreign_keys='Following.profile_by_id')
    subscribers = relationship('Following', back_populates='profile_whom', foreign_keys='Following.profile_whom_id')

    def __repr__(self):
        return f'<Profile {self.id} {self.name}>'
