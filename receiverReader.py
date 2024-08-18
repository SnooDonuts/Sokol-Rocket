import serial
import serial.tools.list_ports
import time

def findArduinoPort():
    # Scan all available ports
    ports = serial.tools.list_ports.comports()
    arduino_port = None

    for port in ports:
        # Check for typical Arduino identifiers in device names
        if 'ttyUSB' in port.device or 'ttyACM' in port.device:
            arduino_port = port.device
            break

    return arduino_port

def attemptConnection(max_retries=5):
    for attempt in range(1, max_retries + 1):
        arduino_port = findArduinoPort()

        if arduino_port:
            print(f"Arduino found on port: {arduino_port}")
            return arduino_port

        print(f"Attempt {attempt} failed: No Arduino found.")
        time.sleep(1)

    print("Failed to find Arduino after 5 attempts.")
    return None
