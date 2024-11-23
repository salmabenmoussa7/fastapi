from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from typing import List
import requests
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import numpy as np
import time
import jwt


app = FastAPI()
SECRET_KEY = "mysecretkey"
data_store = []
security = HTTPBearer()


class UserModel(BaseModel):
    username: str
    password: str

@app.post('/token')
async def generate_token(user: UserModel):
    if user.username == "salma" and user.password == "xxxx":
        payload = {
            "username": user.username,
            "exp": time.time() + 600
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
        return {"token": token}
    raise HTTPException(status_code=401, detail="Invalid username or password")


def verify_jwt(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return decoded_token
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")


@app.get('/secured-data', dependencies=[Depends(verify_jwt)])
async def secured_data():
    return {"message": "This is secured data, only accessible with a valid token"}

class PredictionInput(BaseModel):
    features: List[float]

@app.post('/predict')
async def predict(input_data: PredictionInput):
    coefficients = np.array([2.5, -1.2, 3.7]) 
    bias = 4.0
    if len(input_data.features) != len(coefficients):
        raise HTTPException(status_code=400, detail="Invalid number of features")
    features = np.array(input_data.features)
    prediction = np.dot(features, coefficients) + bias

    return {"prediction": prediction}

@app.post('/data')
async def submit_data(new_data: dict):
    data_store.append(new_data)
    return {"message": "Data submitted successfully!"}

@app.get('/data')
async def get_data():
    return data_store

@app.get('/health_check')
async def health_check():
    return {"status": "up"}

@app.get('/call_external_api')
async def call_external_api():
    url = 'https://impactco2.fr/api/v1/chauffage'  
    response = requests.get(url)
    return response.json()

