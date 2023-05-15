import shutil
from pathlib import Path
from uuid import uuid4, UUID

from fastapi import APIRouter, UploadFile
from sqlalchemy.orm import Session

from core.config import settings
from models import Storage

router = APIRouter()


def storage_save(db: Session,
                 user_id: int,
                 file: UploadFile) -> UUID:
    """Store files from profiles"""
    settings.UPLOADS_PATH.mkdir(exist_ok=True)
    filename = get_unique_filename(file.filename)

    with open(settings.UPLOADS_PATH / filename, 'wb') as f:
        shutil.copyfileobj(file.file, f)

    file_db = Storage(filename=filename, content_type=file.content_type, user_id=user_id)
    db.add(file_db)
    db.commit()
    db.refresh(file_db)
    return file_db.uuid


def get_unique_filename(filename: str, path: Path = settings.UPLOADS_PATH) -> str:
    """Get unique filenames based on original filename"""
    fp = Path(filename)
    while (path / filename).exists():
        uuid_rand = uuid4().hex[:10]
        filename = Path(filename).stem + '_' + uuid_rand + Path(filename).suffix
    return filename
