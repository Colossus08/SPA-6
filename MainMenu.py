from machine import RTC, Pin, SPI
import time
import ntptime1 as ntptime
import st7789py as st7789
from st7789py import color565
import vga2_bold_16x16 as font

# Wi Fi Code
import network
sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)
sta_if.connect(ssid='lan_the_man',key='simplepassword')




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

#app positions
app1 = (20, 7, 50, 50)
app2 = (85, 7, 50, 50)
app3 = (20, 77, 50, 50)
app4 = (85, 77, 50, 50)

#all available cursor position list
cursor_focus = (app1, app2, app3, app4)

#current cursor position
app_num = 0

#bool to check if the display is currently displaying the menu
ismenu = True

#button functionality for next/up
def up():
  global app_num
  if app_num < 3:
    app_num += 1
    menu()
  else:
    app_num = 0
    menu()

#button functionality for previous/down
def down():
  global app_num
  if app_num <= 0:
    app_num = 0
  else:
    app_num -= 1
    menu()

 #button functionality to select    
def select():
  global app_num
  global ismenu

  #checks if the menu is on screen of not
  if ismenu:
    if app_num == 0:
      ismenu = False
      display.clear()

      #These text statements can be replaced with the actual code
      display.text(font, "Notion", 50, 50, color565(255, 255, 255))

    elif app_num == 1:
      ismenu = False
      display.clear()

      #These text statements can be replaced with the actual code
      display.text(font, "Announcement", 10, 50, color565(255, 255, 255))

    elif app_num == 2:
      ismenu = False
      display.clear()

      #These text statements can be replaced with the actual code
      display.text(font, "Time table", 5, 50, color565(255, 255, 255))

    elif app_num == 3:
      ismenu = False
      display.clear()

      #These text statements can be replaced with the actual code
      display.text(font, "IDK lol", 20, 50, color565(255, 255, 255))
    
  else:
    print("app specific function")
    
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