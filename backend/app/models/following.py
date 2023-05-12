from sqlalchemy import Column, Integer, ForeignKey, Boolean, TIMESTAMP, func, UniqueConstraint
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Following(Base):
    id = Column(Integer, primary_key=True, index=True)
    profile_by_id = Column(Integer, ForeignKey('profile.id'))
    profile_whom_id = Column(Integer, ForeignKey('profile.id'))
    created = Column(TIMESTAMP, server_default=func.now())

    profile_by = relationship('Profile', back_populates='following', foreign_keys=[profile_by_id])
    profile_whom = relationship('Profile', back_populates='subscribers', foreign_keys=[profile_whom_id])

    __table_args__ = (
        UniqueConstraint('profile_by_id', 'profile_whom_id', name='unique_following'),
    )
