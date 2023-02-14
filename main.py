from machine import RTC, Pin, SPI
import time
import ntptime1 as ntptime
import st7789py as st7789
from st7789py import color565
import vga2_bold_16x16 as font

# Wi Fi Codes
import urequests as requests
import network
sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)
sta_if.connect('lan_the_man','simplepassword')

wifi_connected = sta_if.isconnected()

print(wifi_connected)



#initialize display
spi = SPI(2, baudrate=30000000, polarity=1, phase=1, sck=Pin(18), mosi=Pin(23), miso=Pin(14))

display = st7789.ST7789(
    spi, 135, 240,
    reset     = Pin(4, Pin.OUT),
    cs        = Pin(15,  Pin.OUT),
    dc        = Pin(2, Pin.OUT),
    backlight = Pin(19,  Pin.OUT),
    rotation  = 1
    )

#pins
up_button = Pin(26, Pin.IN)
down_button = Pin(27, Pin.IN)
select_button = Pin(13, Pin.IN)
home_button = Pin(12, Pin.IN)

try:
    display.init()

except:
    pass

# APPS
def get_pages():
   # this is the custom api token that we got through the link below
   #  https://www.notion.com/my-integrations
   NOTION_TOKEN = "secret_IfNAsDWU0ZzesaP2R4sI17JkCzs0HwR5zTiJcVQb5nR"

   # after getting the database ID from the notion page
   # which is after adding the configuration page

   # https://www.notion.so/5f5214d6bedb4b0e9a6302ef1165b14a?v=291113451bd1482e84ac28fe8faa6b56&pvs=4
   # everything before the question mark
   DATABASE_ID = "5f5214d6bedb4b0e9a6302ef1165b14a"

   headers = {
      "Authorization": "Bearer " + NOTION_TOKEN,
      "Content-Type": "application/json",
      "Notion-Version": "2022-06-28", 
   }

   url = f'https://api.notion.com/v1/databases/{DATABASE_ID}/query'

   # payload pages can be varied
   payload = {"page_size": 100}
   # fetched data
   # making a query to the database
   response = urequests.post(url,json=payload,headers = headers)
   # getting response in json format
   data = response.json()

   # dumping data to a file for display
   import json
   with open('db.json','w',encoding='utf8') as f:
      json.dump(data,f)

   # getting results from the objects 
   # and returing the final result in the form of a list
   results = data["results"]
   return results

def notion_api_call():
   results = []
   pages = get_pages()
   for page in pages:
      TASK_NAME = page['properties']['TASK']['title'][0]['text']['content']

      COMMENTS = page['properties']['COMMENTS']['rich_text'][0]['text']['content']

      TASK_STATUS = page['properties']['TASK STATUS']['select']['name']

      # preparing the list of dictionaries for the result
      temp_string = f''
      if TASK_STATUS == 'DONE':
         temp_string += f'{strike(TASK_NAME)}: {COMMENTS}'
      else:
         temp_string += f'{TASK_NAME}: {COMMENTS}'
      results.append(temp_string)

   for result in results:
      print(result)
   return results

def announcement_api_call():
    endpoint = 'https://192.168.137.1:8000/latest_announcement/CSE/2'
    res = requests.get(endpoint)
    res_json = res.text['announcements']

    ret_list = []
    for ann in res_json:
      string = f"{ann['content']}\n{ann['priority']} Priority\n{ann['authority']}"
      ret_list.append(string)    
    return res_json
    
def timetable_api_call():
    pass

app_list = [notion_api_call,announcement_api_call,timetable_api_call]


#app positions
app1 = (20, 7, 50, 50)
app2 = (85, 7, 50, 50)
app3 = (20, 77, 50, 50)
app4 = (85, 77, 50, 50)

#all available cursor position list
cursor_focus = (app1, app2, app3, app4)

#current cursor position
app_num = 0

#Virenn's Mod's
within_app_index = 0
within_app_list = []
#bool to check if the display is currently displaying the menu
ismenu = True

#button functionality for next/up
def up():
  global app_num
  global within_app_index
  if ismenu:
    if app_num < 3:
      app_num += 1
      menu()
    else:
      app_num = 0
      menu()
  else:

    if within_app_index < len(within_app_list) - 1:
      within_app_index += 1
    else:
      pass


#button functionality for previous/down
def down():
  global app_num
  if ismenu:
    if app_num <= 0:
      app_num = 0
    else:
      app_num -= 1
      menu()
  else:
    if within_app_index > 0:
      within_app_index -= 1
    else:
      pass

 #button functionality to select    

def select():
  global app_num
  global ismenu

  global within_app_index
  global within_app_list

  if not ismenu:
    within_app_list = app_list[app_num]()

def show_item():
  global within_app_index
  global within_app_list

  display.clear()
  display.text(font,within_app_list[within_app_index],5,50,color565(255, 255, 255))
  

    
#button functionality to go back to main menu
def home():
  global ismenu

  display.clear()
  ismenu = True
  menu()

#main menu function
def menu():
  global ismenu
  global app1
  global app2
  global app3
  global app4
  global cursor_focus

  ismenu = True

  #draws all the apps
  display.rect(app1[0], app1[1], app1[2], app1[3], color565(170, 170, 170))
  display.rect(app2[0], app2[1], app2[2], app2[3], color565(170, 170, 170))
  display.rect(app3[0], app3[1], app3[2], app3[3], color565(170, 170, 170))
  display.rect(app4[0], app4[1], app4[2], app4[3], color565(170, 170, 170))

  #draws the cursor
  display.rect(cursor_focus[app_num][0], cursor_focus[app_num][1], cursor_focus[app_num][2], cursor_focus[app_num][3], color565(0, 200, 0))

menu()

while True:
    #checks input
    first = up_button.value()
    first1 = down_button.value()
    first2 = select_button.value()
    first3 = home_button.value()
  
    time.sleep(0.1)

    second = up_button.value()
    second1 = down_button.value()
    second2 = select_button.value()
    second3 = home_button.value()

    if first and not second:
        print("Up")
        up()

    if first1 and not second1:
        print("Down")
        down()

    if first2 and not second2:
        print("Select")
        select()

    if first3 and not second3:
        print("Home")
        home()
