from machine import RTC, Pin, SPI
import time
import ntptime1 as ntptime
import st7789py as st7789
from st7789py import color565
import vga2_bold_16x16 as font
import vga1_bold_16x32 as font1
import vga1_8x8 as font2
import vga1_8x16 as font3
import NotoSans as mainfont

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

#initialize the display
try:
    display.init()

except:
    pass

#function to display the main watch face
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


#put this is a while loop to constantly update the time on screen
watch_face()