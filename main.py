#machine and time related imports
from machine import RTC, Pin, SPI
import time
import ntptime1 as ntptime

#driver imports
import st7789py as st7789
from st7789py import color565

#font imports
import vga2_bold_16x16 as font
import vga1_bold_16x32 as font1
import vga1_8x8 as font2
import vga1_8x16 as font3
import NotoSans as mainfont

#wifi imports
import urequests as requests
import network


#connect to wifi
sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)
wifi_connected = sta_if.isconnected()

while True:
    try:
        sta_if.connect('lan_the_man','simplepassword')
    except OSError as e:
        print(e)
        sta_if.disconnect()
    time.sleep(0.5)
    if wifi_connected:
        print("Connected")
        break


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

#pins for buttons
up_button = Pin(26, Pin.IN)
down_button = Pin(27, Pin.IN)
select_button = Pin(13, Pin.IN)
home_button = Pin(12, Pin.IN)

#clock
rtc = RTC()

#This line of code only needs to be run once when the device runs this code the very first time ever
#After which the rtc of the board will be set correctly and can be called directly to get accurate information
ntptime.time()

h_time = ""
m_time = ""
s_time = ""

year = ""
month = ""
day = ""
dof = ""

#adds 0 in front of single digit numbers
def format_time(time_string):
  if len(time_string) == 1:
    return (f"0{time_string}")
  else:
    return time_string

#adds space after number if it is single digit
def format_hour(hour_string):
    if len(hour_string) == 1:
        return (f"{hour_string} ")
    else:
        return hour_string

#adds the suffix to dates
def format_date(date_string):
  if date_string == "1":
    return date_string + "st"
  elif date_string == "2":
    return date_string + "nd"
  elif date_string == "3":
    return date_string + "rd"
  else:
    return date_string + "th"

#take the integer input from rtc.datetime() and convert to corresponding string
def format_day(day_int):
  if day_int == 0:
    return "Monday"
  elif day_int == 1:
    return "Tuesday"
  elif day_int == 2:
    return "Wednesday"
  elif day_int == 3:
    return "Thursday"
  elif day_int == 4:
    return "Friday"
  elif day_int == 5:
    return "Saturday"
  elif day_int == 6:
    return "Sunday"

#take the integer input from rtc.datetime() and convert to corresponding string
def format_month(month_int):
  if month_int == 1:
    return "Jan"
  elif month_int == 2:
    return "Feb"
  elif month_int == 3:
    return "Mar"
  elif month_int == 4:
    return "Apr"
  elif month_int == 5:
    return "May"
  elif month_int == 6:
    return "Jun"
  elif month_int == 7:
    return "Jul"
  elif month_int == 8:
    return "Aug"
  elif month_int == 9:
    return "Sep"
  elif month_int == 10:
    return "Oct"
  elif month_int == 11:
    return "Nov"
  elif month_int == 12:
    return "Dec"

try:
    display.init()
except:
    pass

def watch_face():
    #format the hour, minute and seconds strings
    h_time = format_hour(str(rtc.datetime()[4]))
    m_time = format_time(str(rtc.datetime()[5]))
    s_time = format_time(str(rtc.datetime()[6]))

    #format the year, month, date and day strings
    year = str(rtc.datetime()[0])
    month = format_month(rtc.datetime()[1])
    date = str(rtc.datetime()[2])
    day = format_day(rtc.datetime()[3])
    
    #output the hour and minute
    display.write(mainfont, h_time + ": " + m_time, 145, 97, color565(200, 200, 200))

    #output the seconds
    display.text(font3, s_time, 215, 80, color565(170, 170, 255))
    
    #output the day, month and date
    display.text(font1, day, 10, 10, color565(180, 180, 180))
    display.text(font, month, 50, 110, color565(200, 200, 200))
    display.write(mainfont, date, 7, 97, color565(170, 170, 255))

#apps
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
   response = requests.post(url,json=payload,headers = headers)
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
         temp_string += f'{(TASK_NAME)}: {COMMENTS}'
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


#To check if screen is currently displaying menu or app
ismenu = False
isapp = False

#current app in focus and current element within app in focus
app_index = 0
within_app_index = 0

#list of all available apps and list of all available elements within app
app_list = [notion_api_call, announcement_api_call, timetable_api_call]
within_app_list = []

#list of all app positions on screen
app_positions = ((20, 7, 50, 50), (85, 7, 50, 50), (20, 77, 50, 50))

def up():
    global ismenu
    global isapp
    global app_index
    global app_list
    global within_app_index
    global within_app_list

    if ismenu:
        if app_index < len(app_list):
            app_index += 1
            show_menu()
        else:
            app_index = 0
            show_menu()

    if isapp:
        if within_app_index < len(within_app_list):
            display.clear()
            within_app_index += 1
            show_app_item()
        else:
            pass

    elif not ismenu and not isapp:
        ismenu = True
        display.clear()
        show_menu()

def down():
    global ismenu
    global isapp
    global app_index
    global within_app_index

    if ismenu:
        if app_index > 0:
            app_index -= 1
            show_menu()
        else:
            pass

    if isapp:
        if within_app_index > 0:
            display.clear()
            within_app_index -= 1
            show_app_item()
        else:
            pass

    elif not ismenu and not isapp:
        ismenu = True
        display.clear()
        show_menu()

def select():
    global ismenu
    global isapp
    global within_app_list
    global app_list
    global app_index

    if ismenu:
        ismenu = False
        isapp = True
        #list of strings returned from app function is stored
        within_app_list = app_list[app_index]()
        display.clear()
        show_app_item()

    if isapp:
        pass

    elif not ismenu and not isapp:
        ismenu = True
        display.clear()
        show_menu()

def home():
    global ismenu
    global isapp
    global app_index
    global within_app_index

    if ismenu or isapp:
        ismenu = False
        isapp = False
        app_index = 0
        within_app_index = 0
        display.clear()

    elif not ismenu and not isapp:
        ismenu = True
        display.clear()
        show_menu()


def show_menu():
    global app_positions
    global app_index
    
    #draw all apps
    display.rect(app_positions[0][0], app_positions[0][1], app_positions[0][2], app_positions[0][3], color565(170, 170, 170))
    display.rect(app_positions[1][0], app_positions[1][1], app_positions[1][2], app_positions[1][3], color565(170, 170, 170))
    display.rect(app_positions[2][0], app_positions[2][1], app_positions[2][2], app_positions[2][3], color565(170, 170, 170))

    #draw cursor
    display.rect(app_positions[app_index][0], app_positions[app_index][1], app_positions[app_index][2], app_positions[app_index][3], color565(0, 200, 0))

def show_app_item():
    global within_app_index
    global within_app_list

    display.text(font, within_app_list[within_app_index], 0, 0, color565(200, 200, 200))

#main while loop
while True:
    #checks and rejects long press
    up_first = up_button.value()
    down_first = down_button.value()
    select_first = select_button.value()
    home_first = home_button.value()
  
    time.sleep(0.1)

    up_second = up_button.value()
    down_second = down_button.value()
    select_second = select_button.value()
    home_second = home_button.value()
    
    #checks for inputs
    if up_first and not up_second:
        print("Up")
        up()

    if down_first and not down_second:
        print("Down")
        down()

    if select_first and not select_second:
        print("Select")
        select()

    if home_first and not home_second:
        print("Home")
        home()
        
    elif not ismenu and not isapp:
        watch_face()
