from fastapi import FastAPI
from fastapi_paginate import add_pagination
from starlette.middleware.cors import CORSMiddleware

from core.config import settings


app = FastAPI(title=settings.PROJECT_TITLE, version=settings.PROJECT_VERSION)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "*",
        "http://localhost",
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

add_pagination(app)


@app.get('/')
def hello_api():
    return {"detail": 'hello!!'}


if __name__ == '__main__':
    # for local debugging
    import uvicorn
    uvicorn.run(app, host='127.0.0.1', port=8000)
