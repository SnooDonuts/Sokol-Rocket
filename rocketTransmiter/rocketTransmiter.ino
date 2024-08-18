#include <Wire.h>  // For I2C communication if needed for sensors
#include <SPI.h>   // For SPI communication if needed for sensors
#include <SoftwareSerial.h>  // For serial communication
bool parachute;
float longitude;
float latitude;
float accelX;
float accelY;
float accelZ;
float gyroX;
float gyroY;
float gyroZ;


// Simulate scanning and generating fake telemetry data
float scanLongitude() {
  return random(0, 36000) / 100.0;  // Random longitude value between 0 and 360 degrees
}

float scanLatitude() {
  return random(-9000, 9000) / 100.0;  // Random latitude value between -90 and 90 degrees
}

float scanAccelerationX() {
  return random(-300, 300) / 100.0;  // Random acceleration value between -3 and 3 g
}

float scanAccelerationY() {
  return random(-300, 300) / 100.0;  // Random acceleration value between -3 and 3 g
}

float scanAccelerationZ() {
  return random(-300, 300) / 100.0;  // Random acceleration value between -3 and 3 g
}

float scanGyroscopeX() {
  return random(-200, 200) / 100.0;  // Random gyroscope value between -2 and 2 rad/s
}

float scanGyroscopeY() {
  return random(-200, 200) / 100.0;  // Random gyroscope value between -2 and 2 rad/s
}

float scanGyroscopeZ() {
  return random(-200, 200) / 100.0;  // Random gyroscope value between -2 and 2 rad/s
}

bool initiateParachute() {
  delay(100);
  return 1;
}

bool checkForParachuteInitiation() {
  delay(0);
  return 0;
}

void setup() {
  // Initialize serial communication at 9600 baud rate
  Serial.begin(9600);

  // Add any sensor initialization here if needed
}

void loop() {
  // Scan for fake telemetry data
  longitude = scanLongitude();
  latitude = scanLatitude();
  accelX = scanAccelerationX();
  accelY = scanAccelerationY();
  accelZ = scanAccelerationZ();
  gyroX = scanGyroscopeX();
  gyroY = scanGyroscopeY();
  gyroZ = scanGyroscopeZ();

  if (!parachute) {
    if (checkForParachuteInitiation()) {
      parachute = initiateParachute();
    }
  }

  // Send the telemetry data over Serial
  Serial.print("Longitude: ");
  Serial.print(longitude, 2);
  Serial.print(", Latitude: ");
  Serial.print(latitude, 2);
  Serial.print(", AccelX: ");
  Serial.print(accelX, 2);
  Serial.print(", AccelY: ");
  Serial.print(accelY, 2);
  Serial.print(", AccelZ: ");
  Serial.print(accelZ, 2);
  Serial.print(", GyroX: ");
  Serial.print(gyroX, 2);
  Serial.print(", GyroY: ");
  Serial.print(gyroY, 2);
  Serial.print(", GyroZ: ");
  Serial.print(gyroZ, 2);
  Serial.print(", Parachute: ");
  Serial.println(parachute);

  // Delay before sending the next set of data
  delay(100);  // Send data every second
}
