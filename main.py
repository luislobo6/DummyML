from fastapi import FastAPI, Body
from pydantic import BaseModel, StrictStr, EmailStr
from pydantic import constr, validator, ValidationError
from random import random
from models.random_generator import RandomGenerator
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter("%(asctime)s:%(levelname)s:%(name)s:%(message)s")

file_handler = logging.FileHandler("logs_DummyML.log")
file_handler.setFormatter(formatter)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(stream_handler)  # Se agrega handler para stream

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
        logger.debug(f"Gender = {gen}")
        if gen.lower() not in GENDERS:
            logger.error(f"{gen} is not a valid gender")
            raise ValidationError(f"{gen} is not a valid gender")
        return gen

@app.get("/")
async def root():
    logger.debug("Application is running")
    return {"message": "Application is running"}

@app.post("/validate_data", response_model=User)
async def validate_data(user: User = Body(..., embed=True)):
    logger.debug(f"Application in validating data with user: {user}")
    logger.info(f"{user.dict()}")
    return user.dict()

# predicción POST
@app.post("/prediction")
async def prediction(user: User = Body(..., embed=True)):
    logger.debug(f"Application making prediction with user: {user}")
    if (user.age):
        logger.debug(f"Age is not null, seed = {user.age}")
        rnd = RandomGenerator(user.age)
        rnd.set_seed(user.age)
    else:
        sd = int(random() * 100)
        logger.debug(f"Age is null, seed = {sd}")
        rnd = RandomGenerator(sd)
        rnd.set_seed(sd)
    return {"prediction": rnd.get_random_float(0.0,1.0)}

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
    logger.info("Getting to the info section")
    return {
        "message": "DummyML App, needs to send a user via POST method",
        "data_example": user
        }

