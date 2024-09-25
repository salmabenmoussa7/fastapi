from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import requests # il faut pas utiliser htppx mais requests

app = FastAPI()

# Modèle de données
class Data(BaseModel):
    name: str
    age: int

# In-memory storage for the sake of this example
data_store: List[Data] = []

@app.post('/data')
async def submit_data(new_data: Data):
    # Add the new data to our data store
    data_store.append(new_data)
    return {"message": "Data submitted successfully!"}

@app.get('/data', response_model=List[Data])
async def get_data():
    # Return the stored data
    return data_store

@app.get('/health_check')
async def health_check():
    return {"status": "up"}

# Nouveau endpoint pour appeler l'API externe
@app.get('/call_external_api')
async def call_external_api():
    url = 'https://impactco2.fr/api/v1/chauffage'  # Remplacez cette URL par l'API que vous souhaitez appeler
    return requests.get(url).json()

# Lancer le serveur avec uvicorn depuis la ligne de commande :
# uvicorn app:app --reload
