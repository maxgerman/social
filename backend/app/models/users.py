from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, func
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class User(Base):
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(50), nullable=False, unique=True)
    password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    is_superuser = Column(Boolean, default=False)
    last_login = Column(TIMESTAMP, server_default=func.now())
    last_activity = Column(TIMESTAMP, server_default=func.now())
    created = Column(TIMESTAMP, server_default=func.now())

    profile = relationship('Profile', back_populates='user', uselist=False)
    storage = relationship('Storage', back_populates='user')
    posts = relationship('Post', back_populates='user')
