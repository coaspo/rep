#include <WiFi.h>
#include "time.h"
#include "arduino_secrets.h"

// NTP Servers and Time Zone settings
const char* ntpServer = "pool.ntp.org";
// Example for GMT-5 (EST) with Daylight Saving Time
const long  gmtOffset_sec = -18000; // Offset in seconds from UTC. -5 hours * 3600 seconds/hour
const int   daylightOffset_sec = 3600; // 1 hour daylight saving offset

void printLocalTime();

void setup() {
  Serial.begin(115200);
  delay(1000);

  // Connect to Wi-Fi network
  Serial.printf("Connecting to %s ", SECRET_SSID);
  WiFi.begin(SECRET_SSID, SECRET_PASS);
  while (WiFi.status() != WL_CONNECTED) {
      delay(500);
      Serial.print(".");
  }
  Serial.println(" CONNECTED");

  // Initialize and get time from NTP server
  configTime(gmtOffset_sec, daylightOffset_sec, ntpServer);
  Serial.println("Waiting for NTP time sync...");
  // Wait until time is successfully synchronized
  while (!getLocalTime(nullptr)) {
      Serial.print(".");
      delay(1000);
  }

  Serial.println("\nTime synchronized.");
  printLocalTime();
}

void loop() {
  // You can repeatedly call this function to print the current time
  printLocalTime();
  delay(5000); // Print every 5 seconds
}

// Function to print the local time
void printLocalTime() {
  struct tm timeinfo;
  if(!getLocalTime(&timeinfo)){
    Serial.println("Failed to obtain time");
    return;
  }
  // Print time in a readable format
  Serial.println(&timeinfo, "%A, %B %d %Y %H:%M:%S");
}
