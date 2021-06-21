import serial  # 引用 pySerial 模組

COM_PORT = 'COM4'       # 指定通訊埠
BAUD_RATES = 115200     # 設定傳輸速率(鮑率)
ser = None

try:
    ser = serial.Serial(COM_PORT, BAUD_RATES)   # 初始化通訊埠
    while True:
        while ser.in_waiting:           # 若有收到序列資料 (Arduino 的 Serial.available())
            data_row = ser.readline()   # 讀取一行(含斷行符號\r\n)原始資料
            data = data_row.decode()    # 預設是用 UTF-8 解碼
            data = data.strip('\r').strip('\n')     # 除去換行符號
            print(data)
except serial.SerialException:
    print('通訊埠無法建立, 請確認:\n1.通訊埠名稱\n2.傳輸速率(鮑率)\n3.是否關閉 Arduino IDE 通訊埠視窗')
    print('exit')
except KeyboardInterrupt:
    if ser is not None:
        ser.close()  # 關閉通訊埠
    print('bye!')
except:
    print('其他錯誤')
