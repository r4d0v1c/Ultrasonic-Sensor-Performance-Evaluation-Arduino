import serial
import time
import csv
import matplotlib.pyplot as plt
import os  # Add import for creating directories

arduino = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
cnt = 0

def read_data():
    try:
        data = arduino.readline().decode('utf-8', errors='ignore').strip()
        return data
    except UnicodeDecodeError as e:
        print(f"Decoding error: {e}")
        return ""
    except serial.SerialException as e:
        print(f"Serial error: {e}. Check if the device is connected or if the port is in use.")
        return None

def save_to_csv(filename, distance, time_value, temperature):
    with open(filename, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([distance, time_value, temperature])

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
    plt.axhline(y=100, color='r', linestyle='--', label='Actual Distance (100 cm)')
    plt.colorbar(scatter, label='Distance (cm)')
    plt.xlabel('Time (µs)', fontsize=12)
    plt.ylabel('Distance (cm)', fontsize=12)
    plt.title('Response Time vs Distance', fontsize=14)
    plt.grid(visible=True, linestyle='--', alpha=0.7)
    plt.legend(['Measurements', 'Actual Distance'], loc='upper left')
    plt.tight_layout()

    # Save the plot
    output_path = "../plots/overview/avg_response_vs_dist_100cm.png"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path)
    plt.close()
    print(f"Plot saved at {output_path}")

def plot_response_time_histogram(filename):
    times = []
    with open(filename, mode='r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        for row in reader:
            try:
                times.append(float(row[1]))
            except ValueError:
                continue

    plt.figure(figsize=(10, 6))
    plt.hist(times, bins=15, color='blue', edgecolor='black', alpha=0.7)
    plt.xlabel('Response Time (µs)', fontsize=12)
    plt.ylabel('Frequency', fontsize=12)
    plt.title('Response Time Histogram', fontsize=14)
    plt.grid(visible=True, linestyle='--', alpha=0.7)

    output_path = "../plots/latency/response_time_histogram_100cm.png"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path)
    plt.close()
    print(f"Response time histogram saved at {output_path}")

def plot_response_time_by_distance(filename):
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
    plt.plot(distances, times, marker='o', linestyle='-', color='green')
    plt.xlabel('Distance (cm)', fontsize=12)
    plt.ylabel('Response Time (µs)', fontsize=12)
    plt.title('Response Time by Distance', fontsize=14)
    plt.grid(visible=True, linestyle='--', alpha=0.7)

    output_path = "../plots/latency/response_time_by_distance_100cm.png"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path)
    plt.close()
    print(f"Response time by distance plot saved at {output_path}")

def plot_histogram_per_distance(filename):
    times = []
    with open(filename, mode='r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        for row in reader:
            try:
                times.append(float(row[1]))
            except ValueError:
                continue

    plt.figure(figsize=(10, 6))
    plt.hist(times, bins=15, color='orange', edgecolor='black', alpha=0.7)
    plt.xlabel('Response Time (µs)', fontsize=12)
    plt.ylabel('Frequency', fontsize=12)
    plt.title('Response Time Histogram (100 cm)', fontsize=14)
    plt.grid(visible=True, linestyle='--', alpha=0.7)

    output_path = "../plots/per_distance/100cm_hist_response.png"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path)
    plt.close()
    print(f"25 cm response time histogram saved at {output_path}")

def plot_time_series_per_distance(filename):
    times = []
    with open(filename, mode='r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        for row in reader:
            try:
                times.append(float(row[1]))
            except ValueError:
                continue

    plt.figure(figsize=(10, 6))
    plt.plot(range(len(times)), times, marker='o', linestyle='-', color='purple')
    plt.xlabel('Measurement Index', fontsize=12)
    plt.ylabel('Response Time (µs)', fontsize=12)
    plt.title('Response Time Time Series (100 cm)', fontsize=14)
    plt.grid(visible=True, linestyle='--', alpha=0.7)

    output_path = "../plots/per_distance/100cm_time_series.png"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path)
    plt.close()
    print(f"25 cm response time time series saved at {output_path}")

def main():
    global cnt  # Declare cnt as global
    csv_file = "../data/100cm.csv"
    current_temperature = 23  # Current temperature in °C
    with open(csv_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Distance (cm)", "Time (µs)", "Temperature (°C)"])  # Write header

    while cnt < 15:
        data = read_data()
        if data is None:  # Handle case where read_data returns None
            print("No data received. Exiting...")
            break
        if data:
            try:
                distance, time_value = data.split(',')
                print(f"Distance: {distance} cm, Time: {time_value} µs, Temperature: {current_temperature} °C")
                save_to_csv(csv_file, distance, time_value, current_temperature)
            except ValueError:
                print(f"Invalid data format: {data}")
        time.sleep(1)
        cnt += 1
    print("Data collection complete.")
    plot_data(csv_file)
    plot_response_time_histogram(csv_file)
    plot_response_time_by_distance(csv_file)
    plot_histogram_per_distance(csv_file)
    plot_time_series_per_distance(csv_file)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Program terminated.")
    finally:
        arduino.close()