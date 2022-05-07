from fastapi import FastAPI, Body
from pydantic import BaseModel, StrictStr, EmailStr
from pydantic import constr, validator, ValidationError
from random import seed
from random import random

app = FastAPI()

GENDERS = ["female","male","undisclosed"]

class User(BaseModel):
    active: bool
    balance: float = 0.0
    email: EmailStr
    age: int
    name: constr(min_length=4, strip_whitespace=True)
    gender: StrictStr

    @validator('gender')
    def check_gender(cls, gen):
        if gen.lower() not in GENDERS:
            raise ValidationError(f"{gen} is not a gender")
        return gen

@app.get("/")
async def root():
    return {"message": "Application is running"}

@app.post("/validate_data", response_model=User)
async def validate_data(user: User = Body(..., embed=True)):
    return user.dict()

# predicción POST
@app.post("/prediction")
async def validate_data(user: User = Body(..., embed=True)):
    if (user.age):
        seed(user.age)
    else:
        seed(int(random()*100))
    return {"prediction": random()}

# info sobre el API
user = {"user" : {
        "active": True,
        "balance": 1564.48,
        "email": "leanne.perry@gmail.com",
        "age": 21,
        "name": "Leanne Perry",
        "gender": "female"
        }
    }


@app.get("/info")
async def info():
    return {
        "message": "DummyML App, needs to send a user via POST method",
        "data_example": user
        }

