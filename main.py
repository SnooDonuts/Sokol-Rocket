

import serial
import serial.tools.list_ports
import time
import asyncio
import os
import logging
import signal
import sys
import receiverReader
from functools import wraps
import csv  # Import the csv module
import re   # Import the regular expression module
from dashboard import run_dashboard

# Set up logging
startTime: int = time.time_ns()
log_file = f"./logs/{time.strftime('%Y-%m-%d;%H:%M:%S', time.localtime())}-rocket.log"

# Create a custom logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)  # Set the logging level

# Create handlers
file_handler = logging.FileHandler(log_file)
console_handler = logging.StreamHandler()

# Set levels for handlers
file_handler.setLevel(logging.DEBUG)
console_handler.setLevel(logging.INFO)

# Create a logging format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Add handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)

# Define the CSV file path
csv_file_path = './rocket_data.csv'

# Open the CSV file in append mode and set up the writer
csv_file = open(csv_file_path, mode='a', newline='')
csv_writer = csv.writer(csv_file)

# Write the header row if the file is empty
if os.stat(csv_file_path).st_size == 0:
    csv_writer.writerow(['Timestamp', 'Longitude', 'Latitude', 'AccelX', 'AccelY', 'AccelZ', 'GyroX', 'GyroY', 'GyroZ', 'Parachute'])

def flush_logs_decorator(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        result = await func(*args, **kwargs)
        for handler in logging.getLogger().handlers:
            handler.flush()
        return result

    return wrapper

def shutdown(signal, frame) -> None:
    logger.info("Shutting down...")
    csv_file.close()  # Ensure the CSV file is closed on shutdown
    logging.shutdown()
    sys.exit(0)

# Attach the shutdown handler to SIGINT (Ctrl+C)
signal.signal(signal.SIGINT, shutdown)

def validate_data(data: str) -> bool:
    # Define the expected pattern using a regular expression
    pattern = re.compile(
        r'^Longitude: (-?\d+\.\d+), Latitude: (-?\d+\.\d+), '
        r'AccelX: (-?\d+\.\d+), AccelY: (-?\d+\.\d+), AccelZ: (-?\d+\.\d+), '
        r'GyroX: (-?\d+\.\d+), GyroY: (-?\d+\.\d+), GyroZ: (-?\d+\.\d+), '
        r'Parachute: (\d+)$'
    )
    
    match_obj = pattern.match(data)
    if not match_obj:
        logger.warning(f"Invalid data format: {data}")
        return False
    
    # Extract the matched groups and convert them to appropriate types
    try:
        longitude, latitude = float(match_obj.group(1)), float(match_obj.group(2))
        accelX, accelY, accelZ = float(match_obj.group(3)), float(match_obj.group(4)), float(match_obj.group(5))
        gyroX, gyroY, gyroZ = float(match_obj.group(6)), float(match_obj.group(7)), float(match_obj.group(8))
        parachute = int(match_obj.group(9))
        
        # Check if the values are within expected ranges
        if not (-180 <= longitude <= 180):
            logger.error(f"Longitude out of range: {longitude}")
            return False
        if not (-90 <= latitude <= 90):
            logger.error(f"Latitude out of range: {latitude}")
            return False
        if not (-16 <= accelX <= 16 and -16 <= accelY <= 16 and -16 <= accelZ <= 16):
            logger.error(f"Acceleration out of range: X={accelX}, Y={accelY}, Z={accelZ}")
            return False
        if not (-2000 <= gyroX <= 2000 and -2000 <= gyroY <= 2000 and -2000 <= gyroZ <= 2000):
            logger.error(f"Gyroscope out of range: X={gyroX}, Y={gyroY}, Z={gyroZ}")
            return False
        if parachute not in [0, 1]:
            logger.error(f"Invalid parachute value: {parachute}")
            return False

    except ValueError as e:
        logger.warning(f"Data conversion error: {e}")
        return False

    return True

@flush_logs_decorator
async def readData() -> None:
    receiver_port = receiverReader.attemptConnection()

    if receiver_port:
        try:
            ser = serial.Serial(receiver_port, 9600)
            logger.info(f"Connected to receiver on port {receiver_port}")
            
            while True:
                if ser.in_waiting > 0:
                    try:
                        data = ser.readline().decode('utf-8').rstrip()
                    except Exception as e:
                        logger.error(f"Error decoding to utf-8: {e}")
                                        
                    # Validate the received data
                    if validate_data(data):
                        # Write the data to the CSV file with the current timestamp
                        parsed_data = [time.strftime('%Y-%m-%d %H:%M:%S')] + [x.split(": ")[1] for x in data.split(", ")]
                        csv_writer.writerow(parsed_data)
                        logger.info(f"Valid data written to CSV: {data}")

        except serial.SerialException as e:
            logger.error(f"Error opening serial port {receiver_port}: {e}")
    
    else:
        logger.error("Exiting program due to failure to connect to Arduino.")

async def start_dashboard():
    # Running the Dash server in the event loop
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, run_dashboard)

# Main function to run the tasks
async def main():
    # Start the dashboard and the data reading concurrently
    dashboard_task = asyncio.create_task(start_dashboard())
    read_data_task = asyncio.create_task(readData())

    # Wait for both tasks to complete
    await asyncio.gather(dashboard_task, read_data_task)

if __name__ == "__main__":
    asyncio.run(main())

