import datetime
import jwt
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ["http://localhost:3000",
           "https://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/")
async def create_token(key: str, secret: str):
    def get_expired_datetime():
        """Generate expired datetime for JWT token
            return: expired datetime in unix timestamp"""
        expired_time = datetime.datetime.now()+datetime.timedelta(days=180)
        unix_expired_time = datetime.datetime.timestamp(expired_time)
        return(unix_expired_time)

    expired_datetime = get_expired_datetime()
    key = key
    secret = secret
    encoded = jwt.encode(
        {"exp": expired_datetime},
        secret,
        algorithm="HS256",
        headers={"iss": key},

    )
    return {"token": encoded}
