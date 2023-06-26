
#conexion con la base de datos

class Config:
    SECRET_KEY = 'B!1w8NAt1T^%kvhUI*S^'


class DevelopmentConfig(Config):
    DEBUG = True
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = ''
    MYSQL_DB = 'Pi'


config = {
    'development': DevelopmentConfig
}

"""
import pyautogui as p
import time as t

distance = 200
p.hotkey("win", "r")
t.sleep(2)
p.write("mspaint.exe", interval=.5)
t.sleep(2)
p.press("enter")
p.moveTo(650, 400)
t.sleep(5)
while distance > 0:
    p.drag(distance, 0, duration=0.5)   # move right
    distance -= 5
    p.drag(0, distance, duration=0.5)   # move down
    p.drag(-distance, 0, duration=0.5)  # move left
    distance -= 5
    p.drag(0, -distance, duration=0.5)
"""