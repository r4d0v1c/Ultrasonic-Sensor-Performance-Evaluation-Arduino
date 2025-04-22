import serial
import time


arduino = serial.Serial('/dev/ttyACM0', 9600, timeout=1)

def read_data():
    try:
        data = arduino.readline().decode('utf-8', errors='ignore').strip()
        return data
    except UnicodeDecodeError as e:
        print(f"Decoding error: {e}")
        return ""

def main():
    while True:
        data = read_data()
        if data:
            try:
                distance, time_value = data.split(',')
                print(f"Distance: {distance} cm, Time: {time_value} µs")
            except ValueError:
                print(f"Invalid data format: {data}")
        time.sleep(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Program terminated.")
    finally:
        arduino.close()