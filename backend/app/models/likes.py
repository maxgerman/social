from sqlalchemy import Column, Integer, ForeignKey, Boolean, TIMESTAMP, func
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Like(Base):
    id = Column(Integer, primary_key=True, index=True)
    profile_id = Column(Integer, ForeignKey('profile.id'))
    liked_profile_id = Column(Integer, ForeignKey('profile.id'), primary_key=True)
    created = Column(TIMESTAMP, server_default=func.now())

    profile = relationship('Profile', back_populates='likes_made', foreign_keys=[profile_id])
    liked_profile = relationship('Profile', back_populates='likes_got', foreign_keys=[liked_profile_id])
