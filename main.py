import databases, sqlalchemy, datetime, uuid
from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import List

# to hash a password
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

## Postgress Database
#first postgress is for username and second is for the password
DATABASE_URL = "postgresql://postgres:postgres@127.0.0.1:5432/mydb"
database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()

# This will create a new table in the database called py_test
users = sqlalchemy.Table(
    "py_users",
    metadata,
    sqlalchemy.Column("id"        ,sqlalchemy.String, primary_key=True),
    sqlalchemy.Column("username"  , sqlalchemy.String),
    sqlalchemy.Column("password"  , sqlalchemy.String),
    sqlalchemy.Column("first_name", sqlalchemy.String),
    sqlalchemy.Column("last_name" , sqlalchemy.String),
    sqlalchemy.Column("gender"    , sqlalchemy.CHAR  ),
    sqlalchemy.Column("create_at" , sqlalchemy.String),
    sqlalchemy.Column("status"    , sqlalchemy.CHAR  ),
)

engine = sqlalchemy.create_engine(
    DATABASE_URL
)
metadata.create_all(engine)

# Class to create a model
class UserList(BaseModel):
    id: str
    username  : str
    password  : str
    first_name: str
    last_name : str
    gender    : str
    create_at : str
    status    : str

# This will be used as examples in http://localhost:8000/docs for POST
class UserEntry(BaseModel):
    username  : str = Field(..., example="nigelreign")
    password  : str = Field(..., example="ilovejesus")
    first_name: str = Field(..., example="Nigel")
    last_name : str = Field(..., example="Zulu")
    gender    : str = Field(..., example="M")

# This will be used as examples in http://localhost:8000/docs for UPDATE
class UserUpdate(BaseModel):
    id        : str = Field(..., example="enter your ID")
    first_name: str = Field(..., example="Nigel")
    last_name : str = Field(..., example="Zulu")
    gender    : str = Field(..., example="M")
    status    : str = Field(..., example="1")

# This will be used as examples in http://localhost:8000/docs for DELETE
class UserDelete(BaseModel):
    id        : str = Field(..., example="enter your ID")

app = FastAPI()

# starting the database
@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

# GET request to get all users from the db
@app.get("/users", response_model=List[UserList])
async def find_all_users():
    query = users.select()
    return await database.fetch_all(query)

#POST request to add user to the database
@app.post("/users", response_model=UserList)
async def register_user(user: UserEntry):
    gID   = str(uuid.uuid1())
    gDate = str(datetime.datetime.now())
    query = users.insert().values(
        id         = gID,
        username   = user.username,
        first_name = user.first_name,
        last_name  = user.last_name,
        # hash password
        password   = pwd_context.hash(user.password),
        gender     = user.gender,
        create_at  = gDate,
        status     = "1"
    )

    await database.execute(query)
    return {
        "id": gID,
        **user.dict(),
        "create_at": gDate,
        "status": "1"
    }

@app.get("/users/{user_id}", response_model=UserList)
async def find_user_by_id(user_id: str):
    query = users.select().where(users.c.id == user_id)
    return await database.fetch_one(query)


# UPDATE request
@app.put("/users", response_model=UserList)
async def update_user(user: UserUpdate):
    gDate = str(datetime.datetime.now())
    query = users.update().\
        where(users.c.id == user.id).\
        values(
            first_name = user.first_name,
            last_name  = user.last_name,
            gender     = user.gender,
            create_at  = gDate,
            status     = user.status
        )

    await database.execute(query)

    return await find_user_by_id(user.id)


@app.delete("/users")
async def delete_user(user: UserDelete):
    query = users.delete().where(users.c.id == user.id)
    await database.execute(query)

    return {
        "status": True,
        "message": "User deleted successfully"
    }
