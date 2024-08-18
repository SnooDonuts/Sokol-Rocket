#include <ELECHOUSE_CC1101_SRC_DRV.h>

void setup() {
  // Initialize Serial Monitor
  Serial.begin(9600);

  // Initialize the CC1101 module
  ELECHOUSE_cc1101.Init();           // Initialize CC1101
  ELECHOUSE_cc1101.setMHZ(868);       // Set frequency to 868MHz
  ELECHOUSE_cc1101.SetRx();           // Set the CC1101 module to receive mode

  Serial.println("CC1101 Receiver Initialized");
}

void loop() {
  // Buffer to hold incoming data
  char data[64];

  // Check if data is available
  if (ELECHOUSE_cc1101.CheckRxFifo(data)) {
    Serial.print("Received data: ");
    Serial.println(data);           // Print received data to Serial Monitor
  }
  else {
    Serial.println("No data received");
  }

  delay(100);                        // Small delay to prevent flooding the serial monitor
}
