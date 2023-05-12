from os import PathLike
from typing import Optional
from uuid import UUID

from sqlalchemy.orm import Session

from models import Storage


def get_filepath_by_uuid(db: Session, uuid: UUID) -> Optional[PathLike]:
    """Return filepath by uuid"""
    storage = db.query(Storage).filter(Storage.uuid == uuid).first()
    return storage
