from fastapi import APIRouter, Response, status
from typing import List
from config.db import conn 
from schemas.user import userEntity, usersEntity
from models.user import User 
from passlib.hash import sha256_crypt
from bson import ObjectId
from starlette.status import HTTP_204_NO_CONTENT


user = APIRouter()
 
@user.get('/users', response_model=List[User], tags=["Users"])
def getAll_Users():
    return usersEntity(conn.local.user.find())

@user.post('/users', response_model=User, tags=["Users"])
def create_User(user: User):
    newUser = dict(user)
    newUser["password"] = sha256_crypt.encrypt(newUser["password"]) 
    del newUser["id"]
    id = conn.local.user.insert_one(newUser).inserted_id
    user = conn.local.user.find_one({"_id": id})
    return userEntity(user)

@user.get('/users/{id}', response_model=User, tags=["Users"])
def get_User(id: str):
    return userEntity(conn.local.user.find_one({"_id": ObjectId(id) }))

@user.put('/users/{id}', response_model=User, tags=["Users"])
def update_User(id: str, user: User):
    conn.local.user.find_one_and_update(
        {"_id": ObjectId(id)}, {"$set": dict(user)}
    )
    return userEntity(conn.local.user.find_one({"_id": ObjectId(id)}))


@user.delete('/users/{id}', status_code=status.HTTP_204_NO_CONTENT, tags=["Users"])
def delete_User(id: str):
    userEntity(conn.local.user.find_one_and_delete({"_id": ObjectId(id)}))
    return  Response(status_code=HTTP_204_NO_CONTENT)
 