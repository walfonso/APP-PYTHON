from fastapi import FastAPI 
from routes.user import user
from docs import tags_metadata


app = FastAPI(
    title= "REST API with FastAPI and MongoDB",
    description= "This is simple REST API using FastAPI and MongoDB ",
    version="1.0.0",
    openapi_tags=tags_metadata 
) 
app.include_router(user)
