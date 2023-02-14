from fastapi import FastAPI, HTTPException
from enum import Enum
from pydantic import BaseModel
import mysql.connector


cnx = mysql.connector.connect(user='root',password='Passwordused1',host='localhost',database='spa_6')
cursor = cnx.cursor()
cursor.execute('USE spa_6;')
print("Connected!")

app = FastAPI()
# app.run(host='0.0.0.0')

class Priorities(str,Enum):
    highest_priority = "High"
    intermediate_priority = "Intermediate"
    low_priority = "Low"

class Batch(str,Enum):
    bdes = "BDES"
    cse = "CSE"
    biotech = "BIOTECH"

class Announcement(BaseModel):
    content: str
    priority: Priorities
    batch:Batch
    year: int
    authority : str

@app.get("/get_announcement/{degree}/{year}")
async def root(degree:Batch,year:int):

    cnx.reconnect() 
    query = f""" SELECT id,content,priority,authority FROM announcements
    WHERE
    batch="{degree}" AND year={year} AND CAST(timestamp AS date) = CAST(now() AS date)
    ORDER BY timestamp DESC,priority ASC;
    """
    print(query)
    cursor_1 = cnx.cursor()    
    cursor_1.execute(query)
    result = cursor_1.fetchall()

    response = {"announcements":[]}

    for x in result:
        print(x)
        temp = {}
        temp["id"] = x[0]
        temp["content"] = x[1]
        temp["priority"] = x[2]
        temp['authority'] = x[3]
        response['announcements'].append(temp)
    cursor_1.close()
    print(response)
    return response

@app.get('/latest_announcement/{degree}/{year}')
async def latest_announcement(degree:Batch,year:int):
    cnx.reconnect() 
    query = f""" SELECT id,content,priority,authority FROM announcements
    WHERE
    batch="{degree}" AND year={year} AND CAST(timestamp AS date) = CAST(now() AS date)
    ORDER BY timestamp DESC,priority ASC
    LIMIT 1;
    """
    print(query)
    cursor_1 = cnx.cursor()    
    cursor_1.execute(query)
    result = cursor_1.fetchall()

    response = {"announcements":[]}

    for x in result:
        print(x)
        temp = {}
        temp["id"] = x[0]
        temp["content"] = x[1]
        temp["priority"] = x[2]
        temp['authority'] = x[3]
        response['announcements'].append(temp)
    cursor_1.close()
    print(response)
    return response


@app.post('/make_announcements/')
async def make_announcement(announcement:Announcement):

    # print("In the POST request")
    cnx.reconnect() 
    cursor = cnx.cursor()
    if  1 <= announcement.year <= 4:
        
        # print("Working till here")
        query = f"""INSERT INTO announcements(content,priority,timestamp,batch,year,authority)
        VALUES
        ("{announcement.content}","{announcement.priority}",now(),"{announcement.batch}",{announcement.year},"{announcement.authority}")  
        """
        # print(query)
        cursor.execute(query)
        cursor.close()
        cnx.commit()

        # Make an SQL query to add announcem
        return announcement
    else:
        raise HTTPException(status_code=422, detail="Year out of Possible Constraints")