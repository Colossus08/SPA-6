import mysql.connector
from pydantic import BaseModel
from fastapi import FastAPI
import os

# password has been set as an environment variable
database_password=os.environ['Password']
database_name='api'
table_name='timetable'

app = FastAPI()

# Setup database connection
cnx = mysql.connector.connect(
    host="localhost",
    user="root",
    password=database_password,
    database=database_name
)

# this may seem useless but its useful to validate the data that is being entered. may prove to be useful when using post
class POST(BaseModel):
    time: str
    day:str
    new:str

class GET(BaseModel):
    full: bool
    day: str

# get request returns entire database for now
@app.get("/btech/cse/sy/get")
def get_timetable():
    cursor = cnx.cursor()
    # if getting.full:
    cursor.execute("SELECT * FROM {table_name}".format(table_name=table_name))
    result = cursor.fetchall()
    return result
    # else:
    #     cursor.execute("SELECT time,{day} FROM {table_name}".format(day=getting.day,table_name=table_name))
    #     result = cursor.fetchall()
    #     return result

@app.get("/btech/cse/sy/get/{weekday}")
def get_timetable_day(weekday):
    cursor=cnx.cursor()
    cursor.execute('Select time,{day} from {table_name}'.format(table_name=table_name,day=weekday))
    result=cursor.fetchall()
    return result

@app.post('/btech/cse/sy/post')
def post_timetable(change:POST):
    cursor=cnx.cursor()
    update_query="update {table_name} set {day} = '{new}' where time={time}".format(day=change.day,table_name=table_name,time=change.time,new=change.new)
    cursor.execute(update_query)
    cnx.commit()
    cursor.execute('select * from {table_name}'.format(table_name=table_name))
    result=cursor.fetchall()
    return result
    # return ("update {table_name} set {day} = '{new}' where time={time}".format(day=change.day,table_name=table_name,time=change.time,new=change.new))