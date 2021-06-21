import serial  # 引用 pySerial 模組
import time

# COM_PORT = 'COM4'       # 指定通訊埠
COM_PORT = 'COM4'       # 指定藍芽通訊埠
BAUD_RATES = 115200     # 設定傳輸速率(鮑率)
ser = None

try:
    ser = serial.Serial(COM_PORT, BAUD_RATES)   # 初始化通訊埠
    while True:
        # data_row = str(input('請輸入欲傳送的數字:')) + '#' # '#'表示結束符號
        data_row = str(input('請輸入欲傳送的數字:')) + '\n'  # '\n'表示結束符號

        data = data_row.encode()
        ser.write(data)
        print('Send: ', data_row, data)
        time.sleep(0.5)

except serial.SerialException:
    print('通訊埠無法建立, 請確認:\n1.通訊埠名稱\n2.傳輸速率(鮑率)\n3.是否關閉 Arduino IDE 通訊埠視窗')
    print('exit')
except KeyboardInterrupt:
    if ser is not None:
        ser.close()  # 關閉通訊埠
    print('bye!')
except:
    print('其他錯誤')
