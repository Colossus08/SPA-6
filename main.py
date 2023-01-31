import mysql.connector
from pydantic import BaseModel
from fastapi import FastAPI
import os

# password has been set as an environment variable
database_password=os.environ['Password']

app = FastAPI()

# Setup database connection
cnx = mysql.connector.connect(
    host="localhost",
    user="root",
    password=database_password,
    database="api"
)

# this may seem useless but its useful to validate the data that is being entered. may prove to be useful when using post
class Item(BaseModel):
    time: str
    monday:str
    tuesday:str

# get request returns entire database for now
@app.get("/")
def read_root():
    cursor = cnx.cursor()
    cursor.execute("SELECT * FROM timetable")
    result = cursor.fetchall()
    return result
