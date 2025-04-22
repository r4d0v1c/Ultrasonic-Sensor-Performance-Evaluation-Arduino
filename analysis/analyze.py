import serial
import time
import csv
import matplotlib.pyplot as plt

arduino = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
cnt = 0

def read_data():
    try:
        data = arduino.readline().decode('utf-8', errors='ignore').strip()
        return data
    except UnicodeDecodeError as e:
        print(f"Decoding error: {e}")
        return ""

def save_to_csv(filename, distance, time_value):
    with open(filename, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([distance, time_value])

def plot_data(filename):
    distances = []
    times = []
    with open(filename, mode='r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        for row in reader:
            try:
                distances.append(float(row[0]))
                times.append(float(row[1]))
            except ValueError:
                continue

    plt.figure(figsize=(10, 6))
    scatter = plt.scatter(times, distances, c=distances, cmap='viridis', edgecolor='k', s=100)
    plt.colorbar(scatter, label='Distance (cm)')
    plt.xlabel('Time (µs)', fontsize=12)
    plt.ylabel('Distance (cm)', fontsize=12)
    plt.title('Response Time vs Distance', fontsize=14)
    plt.grid(visible=True, linestyle='--', alpha=0.7)
    plt.legend(['Measurements'], loc='upper left')
    plt.tight_layout()
    plt.show()

def main():
    global cnt  # Declare cnt as global
    csv_file = "measurements.csv"
    with open(csv_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Distance (cm)", "Time (µs)"])  # Write header

    while cnt < 10:
        data = read_data()
        if data:
            try:
                distance, time_value = data.split(',')
                print(f"Distance: {distance} cm, Time: {time_value} µs")
                save_to_csv(csv_file, distance, time_value)
            except ValueError:
                print(f"Invalid data format: {data}")
        time.sleep(1)
        cnt += 1
    print("Data collection complete.")
    plot_data(csv_file)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Program terminated.")
        plot_data("measurements.csv")
    finally:
        arduino.close()