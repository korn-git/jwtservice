import datetime
import jwt
from fastapi import FastAPI, Response, status
from fastapi.middleware.cors import CORSMiddleware
import requests
import pyrebase
from pydantic import BaseModel

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

config = {
    "apiKey": "AIzaSyDAQuB3pKyB3M9VFZESKNFUpANNUBYFaN8",
    "authDomain": "user-password-storage.firebaseapp.com",
    "projectId": "user-password-storage",
    "storageBucket": "user-password-storage.appspot.com",
    "messagingSenderId": "593789962772",
    "databaseURL": "",
    "appId": "1:593789962772:web:852d387622ddd7dc6cb501"
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()


class Account(BaseModel):
    email: str
    password: str


@app.post("/api/getToken/")
async def create_token(account: Account, response: Response):
    def get_expired_datetime():
        """Generate expired datetime for JWT token
            return: expired datetime in unix timestamp"""
        expired_time = datetime.datetime.now()+datetime.timedelta(days=180)
        unix_expired_time = datetime.datetime.timestamp(expired_time)
        return(unix_expired_time)

    """Firebase username password validation"""
    try:
        auth.sign_in_with_email_and_password(account.email, account.password)
        """request key and secret using email"""
        response = requests.post(
            f'http://kong:8001/consumers/{account.email}/jwt')

        key = response.json().get('key')
        secret = response.json().get('secret')
        """Generate Token"""
        expired_datetime = get_expired_datetime()
        encoded = jwt.encode(
            {"exp": expired_datetime},
            secret,
            algorithm="HS256",
            headers={"iss": key},
        )
        response.status_code = status.HTTP_200_OK
        return {
            "token": encoded
        }
    except Exception as e:
        if str(e) == "sign_in_with_email_and_password() missing 1 required positional argument: 'password'":
            response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
            return {
                "message": "Email or password is missing"
            }
        else:
            response.status_code = status.HTTP_401_UNAUTHORIZED
            return {
                "message": "Wrong email or password"
            }
