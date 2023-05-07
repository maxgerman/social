import sqlalchemy
from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP, func
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

from db.base_class import Base


class Storage(Base):
    uuid = Column(UUID(as_uuid=True), primary_key=True, index=True, server_default=sqlalchemy.text('gen_random_uuid()'))
    user_id = Column(Integer, ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    filename = Column(String, nullable=False)
    content_type = Column(String, nullable=False)
    created = Column(TIMESTAMP, server_default=func.now())
    user = relationship('User', back_populates='storage')


