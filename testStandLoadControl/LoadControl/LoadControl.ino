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
int const Res2_5  = 49;
int const Res5    = 50; 
int const Res12   = 51; 
int const Res25   = 52;
int const Res50   = 53;
int const Res100  = 5;
int const Res250  = 36;
int const Res500  = 35;
int const Res1000 = 34;

int const CapShort = 22;
int const Cap8_2   = 23;
int const Cap16    = 24;
int const Cap33    = 25;
int const Cap62    = 26;
int const Cap127   = 27;
int const Cap256   = 28;
int const Cap510   = 43;
int const Cap1020  = 42;
int const Cap2040  = 41;
int const Cap4100  = 40;
int const Cap8200  = 39;
int const Cap16400 = 38;

int const Ind31_25m = 29;
int const Ind62_5m  = 30;
int const Ind125m   = 31;
int const Ind250m   = 32;
int const Ind500m   = 33;
int const Ind1      = 48;
int const Ind2      = 47;
int const Ind4      = 46;
int const Ind8      = 45;
int const Ind16     = 44;

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
  pinMode(CapShort, OUTPUT);
  pinMode(Cap8_2, OUTPUT);
  pinMode(Cap16, OUTPUT);
  pinMode(Cap33, OUTPUT);
  pinMode(Cap6215, OUTPUT);
  pinMode(Cap12762, OUTPUT);
  pinMode(Cap256, OUTPUT);
  pinMode(Cap510, OUTPUT);
  pinMode(Cap1020, OUTPUT);
  pinMode(Cap2040, OUTPUT);
  pinMode(Cap4100, OUTPUT);
  pinMode(Cap8200, OUTPUT);
  pinMode(Cap16400, OUTPUT);
  pinMode(Ind31_25m, OUTPUT);
  pinMode(Ind62_5m, OUTPUT);
  pinMode(Ind125m, OUTPUT);
  pinMode(Ind250m, OUTPUT);
  pinMode(Ind500m, OUTPUT);
  pinMode(Ind1, OUTPUT);
  pinMode(Ind2, OUTPUT);
  pinMode(Ind4, OUTPUT);
  pinMode(Ind8, OUTPUT);
  pinMode(Ind16, OUTPUT);
  
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
  
  if (capRemaining >= 16400) {
    digitalWrite(Cap16400, HIGH);
    capRemaining -= 16400;
  }
  
  if (capRemaining >= 8200) {
    digitalWrite(Cap8200, HIGH);
    capRemaining -= 8200;
  }
  
  if (capRemaining >= 4100) {
    digitalWrite(Cap4100, HIGH);
    capRemaining -= 4100;
  }
  
  if (capRemaining >= 2040) {
    digitalWrite(Cap2040, HIGH);
    capRemaining -= 2040;
  }
  
  if (capRemaining >= 1000) {
    digitalWrite(Cap1020, HIGH);
    capRemaining -= 1000;
  }
  
  if (capRemaining >= 510) {
    digitalWrite(Cap510, HIGH);
    capRemaining -= 510;
  }
  
  if (capRemaining >= 256) {
    digitalWrite(Cap256, HIGH);
    capRemaining -= 256;
  }
  
  if (capRemaining >= 127) {
    digitalWrite(Cap127, HIGH);
    capRemaining -= 127;
  }
  
  if (capRemaining >= 62) {
    digitalWrite(Cap62, HIGH);
    capRemaining -= 62;
  }
  
  if (capRemaining >= 33) {
    digitalWrite(Cap33, HIGH);
    capRemaining -= 33;
  }
  
  if (capRemaining >= 16) {
    digitalWrite(Cap16, HIGH);
    capRemaining -= 16;
  }
  
  if (capRemaining >= 8) {
    digitalWrite(Cap8_2, HIGH);
    capRemaining -= 8;
  }
  
   // Report remaining capacitance if an exact match was not made
  response = capRemaining;
  
} // end SetC

