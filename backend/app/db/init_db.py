import logging
import random
import string

import sqlalchemy.exc
from faker import Faker

from app import crud
from app.core.config import settings
from app.db.session import SessionLocal
from schemas.users import UserRegisterSchema

fake = Faker()

logger = logging.getLogger('init_db')



def init_db():
    db = SessionLocal()
    if settings.FIRST_SUPERUSER_EMAIL:
        logger.info('Creating superuser')
        user = crud.get_user_by_email(db, email=settings.FIRST_SUPERUSER_EMAIL)
        if not user:
            user = crud.create_user_and_profile(db, UserRegisterSchema(
                email=settings.FIRST_SUPERUSER_EMAIL,
                password=settings.FIRST_SUPERUSER_PASSWORD,
                repeat_password=settings.FIRST_SUPERUSER_PASSWORD,
            ))
            user.is_superuser = True
            db.add(user)
            db.commit()
            logger.info('Superuser created')
        else:
            logger.info('Superuser already exists')
    else:
        logger.info('Superuser not created')

    logger.info(f'Creating users and profiles: {settings.NUMBER_OF_USERS}')
    users = []
    profiles = []
    for i in range(1, settings.NUMBER_OF_USERS + 1):
        random_str = ''.join(random.choices(string.ascii_letters, k=8))
        email = 'user_' + random_str + '@mail.com'
        try:
            user = crud.create_user_and_profile(db, UserRegisterSchema(
                email=email,
                password=settings.DEFAULT_USER_PASSWORD,
                repeat_password=settings.DEFAULT_USER_PASSWORD,
            ))
            user.profile.name = fake.name()
            user.profile.bio = fake.text()
            user.profile.gender = random.choice(['MALE', 'FEMALE'])
            db.add(user)
            db.commit()
        except sqlalchemy.exc.IntegrityError:
            logger.info(f'User with email {email} already exists')
            continue
        logger.info(f'Users and profiles created: {i}')
        users.append(user)
        profiles.append(user.profile)

    logger.info('Creating posts')
    posts = []
    for profile in profiles:
        for _ in range(random.randrange(settings.MAX_POSTS_PER_USER // 2, settings.MAX_POSTS_PER_USER)):
            post = crud.create_post(db, profile.id, fake.text())
            posts.append(post)
        logger.info(f'Created posts for {profile=}')
    logger.info(f'Created total posts: {len(posts)}')

    logger.info('Creating likes')
    likes_count = 0
    for profile in profiles:
        for _ in range(settings.MAX_LIKES_PER_USER):
            post = random.choice(posts)
            if crud.like_post(db, post.id, profile.id):
                likes_count += 1
        logger.info(f'Created likes for {profile=}')
    logger.info(f'Created total likes: {likes_count}')


if __name__ == '__main__':
    init_db()
