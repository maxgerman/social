
from pydantic import BaseModel
from pydantic import EmailStr


class EmailNotificationSchema(BaseModel):
    email: EmailStr
    subject: str = ''
    title: str = ''
    text: str = ''
    url: str = ''
    button_caption: str = ''
