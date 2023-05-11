import logging

import sqlalchemy.exc
from sqlalchemy import Column, Integer, String, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.base_class import Base
from app.models.likes import Like

logger = logging.getLogger(__name__)


class Profile(Base):
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=True)
    name = Column(String, nullable=False, default='')
    image_id = Column(UUID(as_uuid=True), nullable=True)
    gender = Column(String, Enum('MALE', 'FEMALE'), nullable=True)
    bio = Column(String, nullable=False, default='')
    user = relationship('User', back_populates='profile')
    likes_got = relationship('Like', back_populates='liked_profile', foreign_keys=[Like.liked_profile_id])
    likes_made = relationship('Like', back_populates='profile', foreign_keys=[Like.profile_id])

    # async def like_by(self, liker: 'Profile'):
    #     """Like this profile by another profile """
    #     from db.session import SessionLocal
    #     from models.likes import Like
    #     with SessionLocal() as db:
    #         like = Like(member_id=liker.id, liked_member_id=self.id, is_new=True)
    #         db.add(like)
    #         try:
    #             db.commit()
    #         except sqlalchemy.exc.IntegrityError as err:
    #             logger.warning(f'Like already exists for {self.id} by member {liker.id}')
    #             return
    #         logger.debug(f'Like created: by member {liker.id=} for member {self.id}')
    #     return like
