from fastapi import FastAPI
from app.api.v1.user import user_router
from app.api.v1.post import post_router


app = FastAPI(title="Social_Media API", version="1.0.0")

app.include_router(user_router, prefix="/user", tags=["Users"])
app.include_router(post_router, prefix="/posts", tags=["Posts"])

