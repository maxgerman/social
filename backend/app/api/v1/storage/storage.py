import pathlib
from pathlib import Path
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

import crud
from api.v1.dependencies import get_current_user
from core.config import settings
from db.session import get_db
from models import User

router = APIRouter()


@router.get('/{uuid}')
def storage_get(db: Session = Depends(get_db), uuid: UUID = Path(default=...),
                user: User = Depends(get_current_user)):
    """Get uploaded file by uuid. Available for all authenticated users"""
    file = crud.get_filepath_by_uuid(db, uuid)
    if not file or not pathlib.Path(settings.UPLOADS_PATH / file.filename).exists():
        raise HTTPException(status_code=404, detail='File not found')
    return FileResponse(settings.UPLOADS_PATH / file.filename, media_type=file.content_type)
