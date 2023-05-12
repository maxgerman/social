# Social app test task

### By Maksym German

[Original task description link](https://drive.google.com/file/d/1lRoKVkBTtQDdNB1Zwaa0tyJS0wkR7iT1/view)


# Features:

- Users registration, profiles created automatically
- JWT-tokens authentication
- Email notifications in background with fast responses
- Users can Post, Like, Follow, Unfollow
- Posts can include images
- Post and Profile images are stored in the storage, accessible by file UUID
- admin can update users: 
    ○ email with uniqueness checks and error handling
    ○ superuser status
    ○ password (with hashing)
- getting Profiles with ability to sort (the most posts made, the most recently added)
- user can see Profiles all or filtered by: subs only / followers only
- pagination (size, page, total_pages)
- posts viewing - sort by new or likes count, view all or 'feed' (from own subscriptions)
- posts can be accessed from posts endpoint as well as /profiles/<profile_id>/posts[/id]
  - if accessed from profiles route only this profile's posts can be retrieved
- view one's own likes with info about who liked which post and when (nested objects with joinedload), starting from newest (also paginated)
- .env settings include config vars to generate first admin_user and sample content:
    - init_db script creates users, profiles, posts, randomly likes them
- like analytics endpoint (likes count in a date range grouped by day), date format is YYYY-MM-DD