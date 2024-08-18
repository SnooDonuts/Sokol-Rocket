
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
    logging.shutdown()
    sys.exit(0)

# Attach the shutdown handler to SIGINT (Ctrl+C)
signal.signal(signal.SIGINT, shutdown)

@flush_logs_decorator
async def readData() -> None:
    receiver_port = receiverReader.attemptConnection()

    if receiver_port:
        try:
            ser = serial.Serial(receiver_port, 9600)
            logger.info(f"Connected to receiver on port {receiver_port}")
            
            while True:
                if ser.in_waiting > 0:
                    data = ser.readline().decode('utf-8').rstrip()
                    logger.info(data)

        except serial.SerialException as e:
            logger.error(f"Error opening serial port {receiver_port}: {e}")
    
    else:
        logger.error("Exiting program due to failure to connect to Arduino.")

async def web() -> None:
    pass

# Main function to run the tasks
async def main():
    await asyncio.gather(
        readData()
    )

if __name__ == "__main__":
    asyncio.run(main())

