# Social app test task

### By Maksym German

# Demo:
The live demo is running and has some data generated.



# Features:

- the project is using FastAPI, SQLAlchemy, Alembic, PostgreSQL, pytest, Mailhog, Docker Compose
- Users registration (profiles created automatically)
- JWT-tokens authentication
- Users can post, like posts, follow/unfollow other profiles
- Posts can include images
- Post and Profile images are stored in the storage, accessible by file UUID
- posts viewing - sort by new or likes count, view all or 'feed' (from own subscriptions)
- posts can be accessed from posts endpoint as well as /profiles/<profile_id>/posts[/id]
    - if accessed from profiles route only this profile's posts can be retrieved
- getting Profiles with ability to sort (the most posts made, the most recently added)
- user can see Profiles all or filtered by: subs only / followers only
- view one's own likes with info about who liked which post and when (nested objects with joinedload), starting from newest
- pagination (size, page, total, total_pages, current_page)
- email notifications on actions like registration, password reset (sent in background)
- all outgoing email for a session can be seen in Mailhog web interface (http://31.131.24.222:8025)
- admin can update users: 
    - email with uniqueness checks and error handling
    - superuser status
    - password (with hashing)
- .env settings include config vars to generate first admin user and sample content:
    - init_db script creates one admin user, ordinary users, profiles, posts, randomly likes them according to the settings NUMBER_OF_USERS,
    MAX_POSTS_PER_USER, MAX_LIKES_PER_USER 
- like analytics endpoint (likes count in a date range grouped by day), date format is YYYY-MM-DD
- Swagger docs with auth support
- automatically applies all migrations when started by docker-compose
- tests with pytest
