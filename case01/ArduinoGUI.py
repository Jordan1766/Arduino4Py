'''
https://drive.google.com/file/d/1R2Sj9pbvoklY1w3RZNF_EJ-KdsciafPv/view?usp=sharing
+-----------------+
| ___3___   傳送   |
| 344,30.90,71.00 |
+-----------------+
'''
import time
import tkinter
from tkinter import font
import serial  # 引用 pySerial 模組
import threading
import sqlite3
import case01.OpenWeather as ow
import face_recognizer_lab1.Face_recognition as recogn
import cv2
from face_recognizer_lab1 import Config
from io import BytesIO
from PIL import Image, ImageTk
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import matplotlib.pyplot as plt

cred = credentials.Certificate('../firebase/key.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://android-iot-2021-default-rtdb.firebaseio.com/'
})

COM_PORT = 'COM10'       # 指定通訊埠
BAUD_RATES = 115200     # 設定傳輸速率(鮑率)
ser = None
play = True
state_flag = 0
timer_count = 0
cds_rows = []
temp_rows = []
humi_rows = []
ts_rows = []


def updataFirebase(data):
    values = data.split(",")
    # ----------------------------------------------
    # firebase set log
    db.reference('/log/data').set(data)
    db.reference('/log/time/str').set(time.ctime())
    db.reference('/log/time/long').set(time.time())
    # firebase set 結構化資料
    db.reference('/cds').set(values[0])
    db.reference('/DHT/temp').set(values[1])
    db.reference('/DHT/humi').set(values[2])
    # global state_flag
    # if state_flag & 3:
    #     tmp_flag = state_flag & 3
    #     db.reference('/led').set(tmp_flag)
    # else:
    #     tmp_flag = state_flag & 3
    #     db.reference('/led').set(tmp_flag)
    # if state_flag & 4:
    #     db.reference('/door').set(1)
    # else:
    #     db.reference('/door').set(0)
    # if state_flag & 16:
    #     db.reference('/buzeer').set(1)
    # else:
    #     db.reference('/buzeer').set(0)


def face_():
    if state_flag & 4:
        sendData('4')
    else:
        score = recogn.recognizer()
        if score <= Config.POSITIVE_THRESHOLD:
            sendData('4')


def faceListsner(event):
    if (event.data == 1):
        face_()
        db.reference('/face').set(0)


def createTable():
    conn = sqlite3.connect('iot.db')
    sql = 'create table if not exists Env(' \
          'id integer not null primary key autoincrement,' \
          'cds real,' \
          'temp real,' \
          'humi real,' \
          'ts timestamp default current_timestamp' \
          ')'
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()


def insertData():
    conn = sqlite3.connect('iot.db')
    sql = "INSERT INTO Env(cds, temp, humi)"\
        "VALUES (%d, %.1f, %.1f)" % \
          (int(cdsValue.get().split(" ")[0]), float(tempValue.get().split(" ")[0]), float(humiValue.get().split(" ")[0]))
    cursor = conn.cursor()
    cursor.execute(sql)
    print('last insert record id :', cursor.lastrowid)
    conn.commit()
    conn.close()

def getDataBase():
    conn = sqlite3.connect('iot.db')
    sql = "select cds, temp, humi, ts from Env " \
          "order by ts desc limit 10"
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()
    rows = cursor.fetchall()
    conn.close()
    global cds_rows, temp_rows, humi_rows, ts_rows
    cds_rows = []
    temp_rows = []
    humi_rows = []
    ts_rows = []
    for r in rows:
        cds_rows.append(int(r[0]))
        temp_rows.append(float(r[1]))
        humi_rows.append(float(r[2]))
        ts_rows.append(str(r[3][11::]))

    cds_rows.reverse()
    temp_rows.reverse()
    humi_rows.reverse()
    ts_rows.reverse()
    return rows

def sendData(n):
    data_row = n + '\n'  # "#" 代表結束符號
    data = data_row.encode()
    ser.write(data)
    print("send: ", data_row, data)

def getOpenWeatherData():
    status_code, main, icon, temp, feels_like, humidity = ow.openWeather()
    if status_code == 200:
        owmainValue.set(main)

        # 取得 icon 圖片 bytes 資料
        raw_data = ow.openWeatherIcon(icon)
        # 轉成 image 格式
        im = Image.open(BytesIO(raw_data))
        # 轉成 Tk 的 photo 格式
        photo = ImageTk.PhotoImage(im)
        # 配置到目標區域(owiconLabel)
        owiconLabel.config(image=photo)
        owiconLabel.image = photo
        sd_temp = temp - 273.15
        owtempValue.set('%.1f °C' % sd_temp)
        owfeelsLikeValue.set('%.1f °C' % (feels_like - 273.15))
        owhumidityValue.set('%.1f %%' % humidity)

        data_row = str('temp%.2f' % sd_temp) + "#" + str('humi%.2f' % humidity) + "#"  # "#" 代表結束符號
        data = data_row.encode()
        ser.write(data)
        print("send: ", data_row, data)
    else:
        owmainValue.set('Error Code: %d' % status_code)

def checkComPort():
    try:
        global ser
        ser = serial.Serial(COM_PORT, BAUD_RATES)  # 初始化通訊埠
    except Exception as e:
        ser = None
        print('Serial exception: ', e)


def changeBTN_Image():
    if state_flag & 16:
        sendButton0.config(image=buzeerOpen_photo)
        sendButton0.image = buzeerOpen_photo
    else:
        sendButton0.config(image=buzeerClose_photo)
        sendButton0.image = buzeerClose_photo
    if state_flag & 1:
        sendButton1.config(image=red_photo)
        sendButton1.image = red_photo
    else:
        sendButton1.config(image=groy_photo)
        sendButton1.image = groy_photo
    if state_flag & 2:
        sendButton2.config(image=green_photo)
        sendButton2.image = green_photo
    else:
        sendButton2.config(image=groy_photo)
        sendButton2.image = groy_photo
    if (state_flag & 1) and (state_flag & 2):
        sendButton3.config(image=yellow_photo)
        sendButton3.image = yellow_photo
    elif state_flag & 1:
        sendButton3.config(image=red_photo)
        sendButton3.image = red_photo
    elif state_flag & 2:
        sendButton3.config(image=green_photo)
        sendButton3.image = green_photo
    else:
        sendButton3.config(image=groy_photo)
        sendButton3.image = groy_photo
    if state_flag & 4:
        sendButton4.config(image=doorOpen_photo)
        sendButton4.image = doorOpen_photo
    else:
        sendButton4.config(image=doorClose_photo)
        sendButton4.image = doorClose_photo


def cdsDoubleClike(event):
    plt.close()
    plt.figure('Light', figsize=(10, 5))
    plt.title = 'Light'
    plt.plot(ts_rows, cds_rows)
    plt.show()


def tempDoubleClike(event):
    plt.close()
    plt.figure('Temperature', figsize=(10, 5))
    plt.title = 'Temperature'
    plt.plot(ts_rows, temp_rows)
    plt.show()


def humiDoubleClike(event):
    plt.close()
    plt.figure('Humidity', figsize=(10, 5))
    plt.title = 'Humidity'
    plt.plot(ts_rows, humi_rows)
    plt.show()

def buzzer_event(event):
    print("buzzer_event" + str(event.data))
    if event.data == 1:
        sendData('16')
        db.reference("/buzeer").set(0)

def door_event(event):
    print("door_event" + str(event.data))
    if event.data == 1:
        sendData('4')
        db.reference("/door").set(0)

def LED_event(event):
    if event.data == 1:
        sendData('1')
    elif event.data == 2:
        sendData('2')
    elif event.data == 3:
        sendData('3')
    db.reference("/led").set(0)


def saveData():
    global timer_count
    while True:
        getDataBase()
        time.sleep(10)
        timer_count += 1
        insertData()
        if timer_count >= 360:
            getOpenWeatherData()
            timer_count = 0


def dbListen():
    db.reference("/buzeer").set(0)
    db.reference("/door").set(0)
    db.reference("/led").set(0)
    db.reference("/buzeer").listen(buzzer_event)
    db.reference("/door").listen(door_event)
    db.reference("/led").listen(LED_event)


def receiveData():
    getAPI = True
    while play:
        try:
            data_row = ser.readline()  # 讀取一行(含斷行符號\r\n)原始資料
            data = data_row.decode()  # 預設是用 UTF-8 解碼
            data = data.strip('\n')  # 除去換行符號
            data = data.strip('\r')
            values = data.split(",")
            print(data)
            # ------------------------------------------------
            # 建立一條執行緒去維護 firebase 資料
            threading.Thread(target=lambda: updataFirebase(data)).start()
            # ------------------------------------------------
            respText.set(data)
            try:
                cdsValue.set('%d lu' % int(values[0]))
                tempValue.set('%.1f °C' % float(values[1]))
                humiValue.set('%.1f %%' % float(values[2]))
                tmp_flag = int(values[3])
                global state_flag
                if tmp_flag != state_flag:
                    state_flag = tmp_flag
                    changeBTN_Image()

            except:
                pass
            if getAPI:
                getOpenWeatherData()
                getAPI = False
        except Exception as e:
            print('Serial close...', e)
            respText.set('Serial close')
            checkComPort()
            time.sleep(1)
            # break


if __name__ == '__main__':
    # createTable()
    checkComPort()
    root = tkinter.Tk()
    root.geometry("800x400")
    root.title('Arduino 智慧家庭')

    myfont1 = font.Font(family='Helvetica', size=36, weight='bold')
    myfont2 = font.Font(family='Helvetica', size=24)
    red_photo = ImageTk.PhotoImage(Image.open('red_ball.png'))
    green_photo = ImageTk.PhotoImage(Image.open('green_ball.png'))
    yellow_photo = ImageTk.PhotoImage(Image.open('yellow_ball.png'))
    groy_photo = ImageTk.PhotoImage(Image.open('groy_ball.png'))
    doorOpen_photo = ImageTk.PhotoImage(Image.open('Door_open.png'))
    doorClose_photo = ImageTk.PhotoImage(Image.open('Door_close.png'))
    reload_photo = ImageTk.PhotoImage(Image.open('clear.png'))
    buzeerOpen_photo = ImageTk.PhotoImage(Image.open('buzzer_on.png'))
    buzeerClose_photo = ImageTk.PhotoImage(Image.open('buzzer_off.png'))
    person_photo = ImageTk.PhotoImage(Image.open('person.png'))
    # 爬蟲 OpenWeather-----------------------------------------------------------------------
    owmainValue = tkinter.StringVar()
    owmainValue.set('Get')

    owiconValue = tkinter.StringVar()
    owiconValue.set('')

    owtempValue = tkinter.StringVar()
    owtempValue.set('')

    owfeelsLikeValue = tkinter.StringVar()
    owfeelsLikeValue.set('')

    owhumidityValue = tkinter.StringVar()
    owhumidityValue.set('')
    # --------------------------------------------------------------------------------------
    cdsValue = tkinter.StringVar()
    cdsValue.set('0 lu')

    tempValue = tkinter.StringVar()
    tempValue.set('0.0 °C')

    humiValue = tkinter.StringVar()
    humiValue.set('0.0 %')

    respText = tkinter.StringVar()
    respText.set("0,0.0,0.0")

    sendButton0 = tkinter.Button(text='0', image=buzeerClose_photo, command=lambda: sendData('16'), font=myfont2)
    sendButton1 = tkinter.Button(text='1', image=groy_photo, command=lambda: sendData('1'), font=myfont2)
    sendButton2 = tkinter.Button(text='2', image=groy_photo, command=lambda: sendData('2'), font=myfont2)
    sendButton3 = tkinter.Button(text='3', image=groy_photo, command=lambda: sendData('3'), font=myfont2)
    sendButton4 = tkinter.Button(text='4', image=doorClose_photo, command=lambda: sendData('4'), font=myfont2)
    sendButton5 = tkinter.Button(text='5', image=person_photo, command=face_, font=myfont2)
    # sendButton8 = tkinter.Button(text='8', image=doorClose_photo, command=lambda: sendData('8'), font=myfont2)
    # 爬蟲 OpenWeather-----------------------------------------------------------------------
    owmainButton = tkinter.Button(textvariable=owmainValue, command=lambda: getOpenWeatherData(), font=myfont2)
    owiconLabel = tkinter.Label(root, image=None, bg='gray')
    owtempLabel = tkinter.Label(root, textvariable=owtempValue, font=myfont2, fg='#005100')
    owfeelsLikeLabel = tkinter.Label(root, textvariable=owfeelsLikeValue, font=myfont2, fg='#005100')
    owhumidityLabel = tkinter.Label(root, textvariable=owhumidityValue, font=myfont2, fg='#00f')
    # --------------------------------------------------------------------------------------
    cdsLabel = tkinter.Label(root, textvariable=cdsValue, font=myfont1, fg='#ff0000')
    cdsLabel.bind('<Double-Button-1>', cdsDoubleClike)
    tempLabel = tkinter.Label(root, textvariable=tempValue, font=myfont1, fg='#005100')
    tempLabel.bind('<Double-Button-1>', tempDoubleClike)
    humiLabel = tkinter.Label(root, textvariable=humiValue, font=myfont2, fg='#00f')
    humiLabel.bind('<Double-Button-1>', humiDoubleClike)
    receiveLabel = tkinter.Label(root, textvariable=respText)

    root.rowconfigure((0, 1, 2), weight=1)  # 列 0, 列 1 同步放大縮小
    root.columnconfigure((0, 1, 2, 3, 4, 5), weight=1)  # 欄 0, 欄 1, 欄 2 ...同步放大縮小

    sendButton0.grid(row=0, column=0, columnspan=1, sticky='EWNS')
    sendButton1.grid(row=0, column=1, columnspan=1, sticky='EWNS')
    sendButton2.grid(row=0, column=2, columnspan=1, sticky='EWNS')
    sendButton3.grid(row=0, column=3, columnspan=1, sticky='EWNS')
    sendButton4.grid(row=0, column=4, columnspan=1, sticky='EWNS')
    sendButton5.grid(row=0, column=5, columnspan=1, sticky='EWNS')
    # sendButton8.grid(row=0,  column=5, columnspan=1, sticky='EWNS')
    # 爬蟲 OpenWeather-----------------------------------------------------------------------
    owiconLabel.grid(row=1, column=0, columnspan=1, sticky='EWNS')
    owmainButton.grid(row=1, column=1, columnspan=2, sticky='EWNS')
    owtempLabel.grid(row=1, column=3, columnspan=1, sticky='EWNS')
    owfeelsLikeLabel.grid(row=1, column=4, columnspan=1, sticky='EWNS')
    owhumidityLabel.grid(row=1, column=5, columnspan=1, sticky='EWNS')
    # --------------------------------------------------------------------------------------
    cdsLabel.grid(row=2, column=0, columnspan=2, sticky='EWNS')
    tempLabel.grid(row=2, column=2, columnspan=2, sticky='EWNS')
    humiLabel.grid(row=2, column=4, columnspan=2, sticky='EWNS')
    receiveLabel.grid(row=3, column=0, columnspan=6, sticky='EWNS')

    # 監聽 Firebase
    dbListen()

    t1 = threading.Thread(target=receiveData)
    t1.start()
    t2 = threading.Thread(target=saveData)
    t2.start()
    root.mainloop()
