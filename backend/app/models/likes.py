from sqlalchemy import Column, Integer, ForeignKey, Boolean, TIMESTAMP, func, UniqueConstraint
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Like(Base):
    id = Column(Integer, primary_key=True, index=True)
    profile_id = Column(Integer, ForeignKey('profile.id'))
    post_id = Column(Integer, ForeignKey('post.id'))
    created = Column(TIMESTAMP, server_default=func.now())

    profile = relationship('Profile', back_populates='likes_made', foreign_keys=[profile_id])
    post = relationship('Post', back_populates='likes', foreign_keys=[post_id])

    __table_args__ = (
        UniqueConstraint('profile_id', 'post_id', name='unique_like'),
    )
