import serial
import time


arduino = serial.Serial('/dev/ttyACM0', 9600, timeout=1)

def read_data():
    data = arduino.readline().decode('utf-8').strip()
    return data

def main():
    while True:
        data = read_data()
        if data:
            print(f"Received data: {data}")
        time.sleep(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Program terminated.")
    finally:
        arduino.close()