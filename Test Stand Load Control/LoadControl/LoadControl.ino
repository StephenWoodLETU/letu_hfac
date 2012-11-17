/* HFAC Senior Design Team
 *
 * Variable Load (Test Stand) Microcontroller Source Code
 * 
 * Description - This program controls the Arduino on the Variable Load PCB.
 * The purpose of the Ardiuno, is to listen to the Raspberry Pi on the I2C
 * communication channel to set a particular R, L, and C on the Variable
 * Load PCB.
 */

// I2C Libraries:
#include "Wire.h"

// Pin Assignments:
int const Res2_5  = 22;
int const Res5    = 23; 
int const Res12   = 24; 
int const Res25   = 25;
int const Res50   = 26;
int const Res100  = 41;
int const Res250  = 40;
int const Res500  = 39;
int const Res1000 = 38;

int const Cap15    = 28;
int const Cap33    = 29;
int const Cap68    = 30;
int const Cap120   = 31;
int const Cap330   = 32;
int const Cap680   = 47;
int const Cap1000  = 46;
int const Cap2200  = 45;
int const Cap4700  = 44;
int const Cap9400  = 43;
int const Cap18800 = 42;

int const Ind31_25m = 33;
int const Ind62_5m  = 34;
int const Ind125m   = 35;
int const Ind250m   = 36;
int const Ind500m   = 37;
int const Ind1      = 52;
int const Ind2      = 51;
int const Ind4      = 50;
int const Ind8      = 49;

// Define I2C Commands
#define SET_RES_COMMAND  "SETR"
#define SET_IND_COMMAND  "SETL"
#define SET_CAP_COMMAND  "SETC"
#define CMD_LENGTH       4

// Define the slave address of the Arduino (Any number is fine... We'll use 16)
#define SLAVE_ADDRESS 0x10

// Global variable to send back a response from the arduino to the RasPi
// Note that a response of 0 indicates an exact match was made. Any other value
// is the remaining inductance, capacitance, or resistance that was not acheived.
int response = 1;

void setup() {
  pinMode(Res2_5, OUTPUT);
  pinMode(Res5, OUTPUT);
  pinMode(Res12, OUTPUT);
  pinMode(Res25, OUTPUT);
  pinMode(Res50, OUTPUT);
  pinMode(Res250, OUTPUT);
  pinMode(Res500, OUTPUT);
  pinMode(Res1000, OUTPUT);
  pinMode(Cap15, OUTPUT);
  pinMode(Cap33, OUTPUT);
  pinMode(Cap68, OUTPUT);
  pinMode(Cap120, OUTPUT);
  pinMode(Cap330, OUTPUT);
  pinMode(Cap680, OUTPUT);
  pinMode(Cap1000, OUTPUT);
  pinMode(Cap2200, OUTPUT);
  pinMode(Cap4700, OUTPUT);
  pinMode(Cap9400, OUTPUT);
  pinMode(Cap18800, OUTPUT);
  pinMode(Ind31_25m, OUTPUT);
  pinMode(Ind62_5m, OUTPUT);
  pinMode(Ind125m, OUTPUT);
  pinMode(Ind250m, OUTPUT);
  pinMode(Ind500m, OUTPUT);
  pinMode(Ind1, OUTPUT);
  pinMode(Ind2, OUTPUT);
  pinMode(Ind4, OUTPUT);
  pinMode(Ind8, OUTPUT);
  
  // Initialize I2C as slave
  Wire.begin(SLAVE_ADDRESS);
  
  // Define callbacks for I2C communication
  Wire.onReceive(receiveData);
  Wire.onRequest(sendData);
}

void loop() {
  
}

// callback for received data
void receiveData(int byteCount) 
{
  // The command tupple contains both the operation to be taken and the value (operand) to set
  String commandTupple = "";
  String commandValue = "";
  String commandOperation = "";
  
  while(Wire.available())
  { 
     commandTupple = commandTupple + (char)Wire.read();
  }
  
  // Inclusive starting index, Optional exclusive ending index
  commandOperation = commandTupple.substring(0, CMD_LENGTH + 1)
  commandValue = commandTupple.substring(CMD_LENGTH + 1);
  
  if ( commandOperation.equals(SET_RES_COMMAND) ) {
    set_r( atoi(commandValue) );
  }
  
  if ( commandOperation.equals(SET_IND_COMMAND) ) {
    set_l( atoi(commandValue) );
  }
  
  if ( commandOperation.equals(SET_CAP_COMMAND) ) {
    set_c( atoi(commandValue) );
  }
}

// callback for sending data
void sendData()
{ 
  Wire.write(response);  
  response = 0;
}

/* This function sets the resistive network to the closest possible
 * value given. Possible values that the network can achieve are discrete.
 * Decimal values should be rouneded down. Values represents Ohms.
 */
void set_r(int rToSet) {
  
  int resRemaining = rToSet;
  
  if (resRemaining >= 1000) {
    digitalWrite(Res1000, HIGH);
    resRemaining -= 1000;
  }
  
  if (resRemaining >= 500) {
    digitalWrite(Res500, HIGH);
    resRemaining -= 500;
  }
  
  if (resRemaining >= 250) {
    digitalWrite(Res250, HIGH);
    resRemaining -= 250;
  }
  
  if (resRemaining >= 100) {
    digitalWrite(Res100, HIGH);
    resRemaining -= 100;
  }
  
  if (resRemaining >= 50) {
    digitalWrite(Res50, HIGH);
    resRemaining -= 50;
  }
  
  if (resRemaining >= 25) {
    digitalWrite(Res25, HIGH);
    resRemaining -= 25;
  }
  
  if (resRemaining >= 12) {
    digitalWrite(Res12, HIGH);
    resRemaining -= 12;
  }
  
  if (resRemaining >= 5) {
    digitalWrite(Res5, HIGH);
    resRemaining -= 5;
  }
  
  if (resRemaining >= 2) {
    digitalWrite(Res2_5, HIGH);
    resRemaining -= 2;
  }
  
  // Report the remaining resistance if an exact match was not made
  response = resRemaining;
  
} // end SetR

/* This function sets the inductive network to the closest possible
 * value given. Possible values that the network can achieve are discrete.
 * Decimal values should be rouneded down. Values represents mH.
 */
void set_l(int lToSet) {
  int indRemaining = lToSet;
  
  if (indRemaining >= 8000) {
    digitalWrite(Ind8, HIGH);
    indRemaining -= 8000;
  }
  
  
  if (indRemaining >= 4000) {
    digitalWrite(Ind4, HIGH);
    indRemaining -= 4000;
  }
  
  if (indRemaining >= 2000) {
    digitalWrite(Ind2, HIGH);
    indRemaining -= 2000;
  }
  
  if (indRemaining >= 1000) {
    digitalWrite(Ind1, HIGH);
    indRemaining -= 1000;
  }
  
  if (indRemaining >= 500) {
    digitalWrite(Ind500m, HIGH);
    indRemaining -= 500;
  }
  
  if (indRemaining >= 250) {
    digitalWrite(Ind250m, HIGH);
    indRemaining -= 250;
  }
  
  if (indRemaining >= 125) {
    digitalWrite(Ind125m, HIGH);
    indRemaining -= 125;
  }
  
  if (indRemaining >= 62) {
    digitalWrite(Ind62_5m, HIGH);
    indRemaining -= 62;
  }
  
  if (indRemaining >= 31) {
    digitalWrite(Ind31_25m, HIGH);
    indRemaining -= 31;
  }
  
  // Report remaining inductance if an exact match was not made
  response = indRemaining;
  
} // end SetL


/* This function sets the capacitive network to the closest possible
 * value given. Possible values that the network can achieve are discrete.
 * Decimal values should be rouneded down. Values represents Farads.
 */
void set_c(int cToSet) {
  
  capRemaining = cToSet;
  
  if (capRemaining >= 18800) {
    digitalWrite(Cap18800, HIGH);
    capRemaining -= 18800;
  }
  
  if (capRemaining >= 9400) {
    digitalWrite(Cap9400, HIGH);
    capRemaining -= 9400;
  }
  
  if (capRemaining >= 4700) {
    digitalWrite(Cap4700, HIGH);
    capRemaining -= 4700;
  }
  
  if (capRemaining >= 2200) {
    digitalWrite(Cap2200, HIGH);
    capRemaining -= 2200;
  }
  
  if (capRemaining >= 1000) {
    digitalWrite(Cap1000, HIGH);
    capRemaining -= 1000;
  }
  
  if (capRemaining >= 680) {
    digitalWrite(Cap680, HIGH);
    capRemaining -= 680;
  }
  
  if (capRemaining >= 330) {
    digitalWrite(Cap330, HIGH);
    capRemaining -= 330;
  }
  
  if (capRemaining >= 120) {
    digitalWrite(Cap120, HIGH);
    capRemaining -= 120;
  }
  
  if (capRemaining >= 68) {
    digitalWrite(Cap68, HIGH);
    capRemaining -= 68;
  }
  
  if (capRemaining >= 33) {
    digitalWrite(Cap33, HIGH);
    capRemaining -= 33;
  }
  
  if (capRemaining >= 15) {
    digitalWrite(Cap15, HIGH);
    capRemaining -= 15;
  }
  
   // Report remaining capacitance if an exact match was not made
  response = capRemaining;
  
} // end SetC

