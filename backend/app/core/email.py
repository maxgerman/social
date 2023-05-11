import logging

import fastapi_mail.errors
from fastapi_mail import MessageSchema, FastMail, schemas
from starlette.background import BackgroundTasks

from app.core.config import settings
from app.schemas.notifications import EmailNotificationSchema

logger = logging.getLogger(__name__)


def send_email_in_background(email_notification: EmailNotificationSchema, background_tasks: BackgroundTasks):
    """Send email with content of the NotificationAddSchema in background"""
    message_schema = MessageSchema(
        recipients=[email_notification.email],
        subject=email_notification.subject,
        template_body=email_notification.dict(),
        subtype=schemas.MessageType.html,
    )
    try:
        fm = FastMail(settings.email_conf)
        background_tasks.add_task(fm.send_message, message_schema, 'generic_email.html')
        logger.debug(
            'Sent email to: ' + str(message_schema.recipients) + ' with body: ' + str(email_notification.dict()))
    except fastapi_mail.errors.ConnectionErrors as e:
        logger.error('Error sending email to: ' + str(message_schema.recipients) + ' with body: '
                     + str(email_notification.dict()))
        logger.error(e, stack_info=True, exc_info=True)
