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

// Define I2C Commands
#define SET_RES_COMMAND  "SETR"
#define SET_IND_COMMAND  "SETL"
#define SET_CAP_COMMAND  "SETC"
#define CMD_LENGTH       4
#define MAX_CMD_LENGTH   20

// Define the slave address of the Arduino (Any number is fine... We'll use 16)
#define SLAVE_ADDRESS 0x10

// Buffer for receiving command into
char command[MAX_CMD_LENGTH + 1];
int commandIndex = 0;

// Global variable to send back a response from the arduino to the RasPi
// Note that a response of 0 indicates an exact match was made. Any other value
// is the remaining inductance, capacitance, or resistance that was not acheived.
int response = 1;

void setup() {
  
  // Initialize I2C as slave
  Wire.begin(SLAVE_ADDRESS);
  
  // Debug serial begin
  Serial.begin(9600);
  
  // Define callbacks for I2C communication
  Wire.onReceive(receiveData);
  Wire.onRequest(sendData);
  
  Serial.println("Load controller started...");
}

void loop() {
  
}

// callback for received data
void receiveData(int byteCount) 
{
  
  // Read next byte in
  command[commandIndex] = Wire.read();
  Serial.print((int)command[commandIndex]);
  
  // See if we got the command termination byte
  if(command[commandIndex] == '\0'){
    
    if ( strncmp(SET_RES_COMMAND, command, CMD_LENGTH ) == 0 ) {
      set_r( atoi(command + CMD_LENGTH) );
    }
    else if ( strncmp(SET_IND_COMMAND, command, CMD_LENGTH) == 0 ) {
      set_l( atoi(command + CMD_LENGTH) );
    }
    else if ( strncmp(SET_CAP_COMMAND, command, CMD_LENGTH) == 0 ) {
      set_c( atoi(command + CMD_LENGTH) );
    }
    else{
      Serial.println("Got unrecognized command!");
    }
    
    commandIndex = -1;
  }
  
  if(commandIndex < MAX_CMD_LENGTH){
      commandIndex++;
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
  Serial.print("Set resistance to ");
  Serial.println(rToSet);
  
  // Report the remaining resistance if an exact match was not made
  response = 0;
  
} // end SetR

/* This function sets the inductive network to the closest possible
 * value given. Possible values that the network can achieve are discrete.
 * Decimal values should be rouneded down. Values represents mH.
 */
void set_l(int lToSet) {
  Serial.print("Set inductance to ");
  Serial.println(lToSet);
  
  // Report remaining inductance if an exact match was not made
  response = 0;
  
} // end SetL


/* This function sets the capacitive network to the closest possible
 * value given. Possible values that the network can achieve are discrete.
 * Decimal values should be rouneded down. Values represents Farads.
 */
void set_c(int cToSet) {
  Serial.print("Set capacitance to ");
  Serial.println(cToSet);
  
   // Report remaining capacitance if an exact match was not made
  response = 0;
  
} // end SetC

