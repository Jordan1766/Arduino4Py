
'''
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

COM_PORT = 'COM4'       # 指定通訊埠
BAUD_RATES = 115200     # 設定傳輸速率(鮑率)
ser = None
play = True


def clickBTN0():
    data_row = '0\n'
    data = data_row.encode()
    ser.write(data)


def clickBTN1():
    data_row = '1\n'
    data = data_row.encode()
    ser.write(data)


def clickBTN2():
    data_row = '2\n'
    data = data_row.encode()
    ser.write(data)


def clickBTN3():
    data_row = '3\n'
    data = data_row.encode()
    ser.write(data)


def clickBTN4():
    data_row = '4\n'
    data = data_row.encode()
    ser.write(data)


def clickBTN8():
    data_row = '8\n'
    data = data_row.encode()
    ser.write(data)


def sendData(n):
    data_row = n + "#" # "#" 代表結束符號
    data = data_row.encode()
    ser.write(data)
    print("send: ", data_row, data)


def checkComPort():
    try:
        global ser
        ser = serial.Serial(COM_PORT, BAUD_RATES)  # 初始化通訊埠
    except Exception as e:
        ser = None
        print('Serial exception: ', e)


def receiveData():
    while play:
        try:
            data_row = ser.readline()  # 讀取一行(含斷行符號\r\n)原始資料
            data = data_row.decode()  # 預設是用 UTF-8 解碼
            data = data.strip('\r').strip('\n')  # 除去換行符號
            print(data)
            respText.set(data)
            try:
                values = data.split(",")
                cdsValue.set(values[0])
                tempValue.set(values[1])
                humiValue.set(values[2])
            except:
                pass
        except Exception as e:
            print('Serial close...', e)
            respText.set('Serial close')
            checkComPort()
            time.sleep(1)
            # break


if __name__ == '__main__':

    checkComPort()

    root = tkinter.Tk()
    root.geometry("600x400")
    root.title('Arduino GUI')

    myfont1 = font.Font(family='Helvetica', size=36, weight='bold')
    myfont2 = font.Font(family='Helvetica', size=24)

    cdsValue = tkinter.StringVar()
    cdsValue.set('0')

    tempValue = tkinter.StringVar()
    tempValue.set('0.0')

    humiValue = tkinter.StringVar()
    humiValue.set('0.0')

    respText = tkinter.StringVar()
    respText.set("0,0.0,0.0")

    sendButton0 = tkinter.Button(text='0', command=lambda: sendData('0'), font=myfont2)
    sendButton1 = tkinter.Button(text='1', command=lambda: sendData('1'), font=myfont2)
    sendButton2 = tkinter.Button(text='2', command=lambda: sendData('2'), font=myfont2)
    sendButton3 = tkinter.Button(text='3', command=lambda: sendData('3'), font=myfont2)
    sendButton4 = tkinter.Button(text='4', command=lambda: sendData('4'), font=myfont2)
    sendButton8 = tkinter.Button(text='8', command=lambda: sendData('8'), font=myfont2)
    cdsLabel = tkinter.Label(root, textvariable=cdsValue, font=myfont1, fg='#ff0000')
    tempLabel = tkinter.Label(root, textvariable=tempValue, font=myfont1, fg='#005100')
    humiLabel = tkinter.Label(root, textvariable=humiValue, font=myfont2, fg='#00f')
    receiveLabel = tkinter.Label(root, textvariable=respText)

    root.rowconfigure((0, 1), weight=1)  # 列 0, 列 1 同步放大縮小
    root.columnconfigure((0, 1, 2, 3, 4, 5), weight=1)  # 欄 0, 欄 1, 欄 2 ...同步放大縮小

    sendButton0.grid(row=0,  column=0, columnspan=1, sticky='EWNS')
    sendButton1.grid(row=0,  column=1, columnspan=1, sticky='EWNS')
    sendButton2.grid(row=0,  column=2, columnspan=1, sticky='EWNS')
    sendButton3.grid(row=0,  column=3, columnspan=1, sticky='EWNS')
    sendButton4.grid(row=0,  column=4, columnspan=1, sticky='EWNS')
    sendButton8.grid(row=0,  column=5, columnspan=1, sticky='EWNS')
    cdsLabel.grid(row=1, column=0, columnspan=2, sticky='EWNS')
    tempLabel.grid(row=1, column=2, columnspan=2, sticky='EWNS')
    humiLabel.grid(row=1, column=4, columnspan=2, sticky='EWNS')
    receiveLabel.grid(row=2, column=0, columnspan=6, sticky='EWNS')

    t1 = threading.Thread(target=receiveData)
    t1.start()

    root.mainloop()
