# main.py
from fastapi import FastAPI
from supabase import create_client, Client
import os
from dotenv import load_dotenv
import json

app = FastAPI()
load_dotenv()
my_url = os.getenv("SUPABASE_URL")
my_key = os.getenv("SUPABASE_KEY")

@app.get("/")
async def root():
    url: str = my_url
    key: str = my_key
    supabase: Client = create_client(url, key)
    data = supabase.table("Apagon").select("JsonData").execute()
    # Assert we pulled real data.
    assert len(data.data) > 0
    return json.loads(data.data[0].get('JsonData'))