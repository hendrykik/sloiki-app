from datetime import datetime, timedelta

import bcrypt
import psycopg2
from fastapi import FastAPI, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
import jwt

from .config import settings

settings = settings()

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/login")
async def login(login: str, password: str) -> dict:
    if not await auth_user(login, password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )
    return {"access_token": create_access_token(login), "token_type": "bearer"}


async def get_current_user(token: str = Depends(oauth2_scheme)) -> str:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token"
        )
    return payload["sub"]


@app.get("/get_user")
async def get_user(login: str) -> bool:
    connection = psycopg2.connect(
        database="DB", user="postgres", password="postgres", host="db", port=5432
    )
    cursor = connection.cursor()
    cursor.execute("SELECT * from users;")
    users = cursor.fetchall()

    for user in users:
        if user[1] == login:
            return True
    return False


def create_access_token(login: str) -> str:
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    return jwt.encode({"sub": login, "exp": expire}, SECRET_KEY, algorithm=ALGORITHM)


# @app.get("/auth_user")
async def auth_user(login: str, password: str) -> bool:
    connection = psycopg2.connect(
        database="DB", user="postgres", password="postgres", host="db", port=5432
    )
    cursor = connection.cursor()
    cursor.execute("SELECT * from users;")
    users = cursor.fetchall()

    for user in users:
        if user[1] == login and bcrypt.checkpw(
            password.encode("utf-8"), user[2].encode("utf-8")
        ):
            return True
    return False


@app.post("/add_user")
async def add_user(login: str, password: str) -> bool:
    connection = psycopg2.connect(
        database="DB", user="postgres", password="postgres", host="db", port=5432
    )
    cursor = connection.cursor()
    password_hash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode(
        "utf-8"
    )
    try:
        cursor.execute(
            "INSERT INTO users (login, password) VALUES (%s, %s);",
            (login, password_hash),
        )
        connection.commit()
        return True
    except psycopg2.IntegrityError as e:
        print("add_user failed:", e)
        return False


@app.get("/get_calendar_events")
async def get_calendar_events(current_user: str = Depends(get_current_user)):
    connection = psycopg2.connect(
        database="DB", user="postgres", password="postgres", host="db", port=5432
    )
    cursor = connection.cursor()
    try:
        cursor.execute(
            "SELECT calendar_events.id, calendar_events.date, calendar_events.title, calendar_events.description "
            "FROM calendar_events JOIN users AS us ON id_user = us.id WHERE us.login = %s;",
            (current_user,),
        )
        return cursor.fetchall()
    except psycopg2.Error as e:
        return str(e)


@app.get("/current_date")
async def get_current_date():
    return datetime.today()


@app.get("/last_week")
async def get_last_week():
    return datetime.today() - timedelta(days=7)
