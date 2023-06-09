import logging
from datetime import datetime

from fastapi import Depends, HTTPException, APIRouter, Path, Body
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.encoders import jsonable_encoder
from jose import JWTError
from sqlalchemy.orm.session import Session
from starlette.background import BackgroundTasks
from starlette.responses import JSONResponse

import crud
from api.v1.dependencies import get_current_user
from core.auth import authenticate, create_access_token, jwt_decode, verify_last_login
from core.auth import create_pwd_reset_token
from core.config import settings
from core.email import send_email_notification
from core.security import get_password_hash
from db.session import get_db
from models.users import User
from schemas.notifications import EmailNotificationSchema
from schemas.users import UserLoginSchema, UserRegisterSchema, UserOutWithProfileIdSchema, \
    UserOutWithTokenAndProfileIdSchema, UserOutSchema, UserOutWithTokenSchema

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post('/register', response_model=UserOutSchema, status_code=201)
def user_register(*, db: Session = Depends(get_db),
                  user_in: UserRegisterSchema,
                  background_tasks: BackgroundTasks):
    user = db.query(User).filter(User.email == user_in.email).first()
    if user:
        raise HTTPException(status_code=400, detail='Email already registered')
    user_db = crud.create_user_and_profile(db, user_in)

    email_notification = EmailNotificationSchema(
        email=user_in.email,
        subject='Welcome in the Social project',
        title='Welcome',
        text='You have successfully registered in the Social project',
        url=f'{settings.FRONTEND_URL}',
        button_caption='Go to the site')

    background_tasks.add_task(send_email_notification, email_notification)
    return user_db


@router.post('/login', response_model=UserOutWithTokenAndProfileIdSchema)
def login(*, db: Session = Depends(get_db), user_in: UserLoginSchema):
    user = authenticate(email=user_in.email, password=user_in.password, db=db)
    if not user or not user.is_active:
        raise HTTPException(status_code=401, detail='Incorrect email or password')
    token = create_access_token(sub=user.id, remember=user_in.remember)
    user.last_login = datetime.now()
    user.last_activity = datetime.now()
    db.commit()
    user_out = UserOutWithTokenAndProfileIdSchema.from_orm(user)
    user_out.access_token = token
    user_out.profile_id = user.profile.id if user.profile else None
    return JSONResponse(jsonable_encoder(user_out.dict()))


@router.post('/login_docs', response_model=UserOutWithTokenSchema)
def login_docs(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate(email=form_data.username, password=form_data.password, db=db)
    if not user or not user.is_active:
        raise HTTPException(status_code=400, detail='Incorrect username or password')
    token = create_access_token(sub=user.id)
    user.last_login = datetime.now()
    user.last_activity = datetime.now()
    db.commit()
    user_out = UserOutWithTokenSchema.from_orm(user)
    user_out.access_token = token
    return JSONResponse(jsonable_encoder(user_out.dict()))


@router.get('/me', response_model=UserOutWithProfileIdSchema)
def me(user: User = Depends(get_current_user)):
    """Get info about current user."""
    user_out = UserOutWithProfileIdSchema.from_orm(user)
    user_out.profile_id = user.profile.id if user.profile else None
    return JSONResponse(jsonable_encoder(user_out.dict()))


@router.get('/forgot-password/{email}')
async def forgot_password(*, email: str = Path(..., min_length=1, max_length=100),
                    db: Session = Depends(get_db),
                    background_tasks: BackgroundTasks):
    """Check if email exists and send the password reset link to email"""
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    reset_token = create_pwd_reset_token(str(user.id),
                                         extra={'jti': str(user.last_login)})

    email_notification = EmailNotificationSchema(
        email=user.email,
        subject='Password recovery in the Social project',
        title='Password recovery',
        text='You have requested to change password.',
        url=f'{settings.FRONTEND_URL}/reset-password/{reset_token}',
        button_caption='Reset password on site')

    background_tasks.add_task(send_email_notification, email_notification)

    return {'enqueued_email_to': user.email}


@router.post('/reset-password/{token}')
def change_password(token: str = Path(..., max_length=300),
                    db: Session = Depends(get_db),
                    new_password: str = Body(...),
                    repeat_password: str = Body(...)):
    """Change password after token verification"""
    try:
        token_data = jwt_decode(token)
    except JWTError:
        raise HTTPException(status_code=400, detail="Invalid or expired token")
    user = crud.get_user_by_id(db, token_data['sub'])
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # verify that last login time is the same as in token
    if not verify_last_login(token_data, str(user.last_login)):
        raise HTTPException(status_code=400, detail="Invalid token")
    if not new_password or not repeat_password:
        raise HTTPException(status_code=400, detail="New password and repeat are required")
    if new_password != repeat_password:
        raise HTTPException(status_code=400, detail="New passwords do not match")

    user.password = get_password_hash(new_password)
    # invalidate reset token
    user.last_login = datetime.now()
    db.commit()
    return {'password_changed_user_id': user.id}

