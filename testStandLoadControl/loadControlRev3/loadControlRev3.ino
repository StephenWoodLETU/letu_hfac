/* HFAC Senior Design Team
 *
 * Variable Load (Test Stand) Microcontroller Source Code
 * 
 * Description - This program controls the Arduino on the Variable Load PCB.
 * The purpose of the Ardiuno, is to listen to the Raspberry Pi on the I2C
 * communication channel to set a particular R, L, and C on the Variable
 * Load PCB.
 */

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

void setup() {
  pinMode(Res2_5, OUTPUT);
  pinMode(Res5, OUTPUT);
  pinMode(Res12, OUTPUT);
  pinMode(Res25, OUTPUT);
  pinMode(Res50, OUTPUT);
  pinMode(Res100, OUTPUT);
  pinMode(Res250, OUTPUT);
  pinMode(Res500, OUTPUT);
  pinMode(Res1000, OUTPUT);
  pinMode(CapShort, OUTPUT);
  pinMode(Cap8_2, OUTPUT);
  pinMode(Cap16, OUTPUT);
  pinMode(Cap33, OUTPUT);
  pinMode(Cap62, OUTPUT);
  pinMode(Cap127, OUTPUT);
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
  
  Serial.begin(9600);
  
} // end setup

void loop() {
  int rToSet;
  int lToSet;
  int cToSet;
  int missedR;
  int missedL;
  int missedC;
  
  boolean newCommand = false;
  
  while(Serial.available() > 0) {
    rToSet = Serial.parseInt();
    lToSet = Serial.parseInt();
    cToSet = Serial.parseInt();
    
    newCommand = true;
  } // close serial read loop
  
  if (newCommand) {
    reset();
    
    missedR = set_r(rToSet);
    missedL = set_l(lToSet);
    missedC = set_c(cToSet);
    
    Serial.print(missedR);
    Serial.print(", ");
    Serial.print(missedL);
    Serial.print(", ");
    Serial.print(missedC);
    Serial.println(" done");
    
    
    newCommand = false;
  } // end if new command
}


/* This function sets all relays low
 */
void reset() {
  digitalWrite(Res2_5, LOW);
  digitalWrite(Res5, LOW);
  digitalWrite(Res12, LOW);
  digitalWrite(Res25, LOW);
  digitalWrite(Res50, LOW);
  digitalWrite(Res100, LOW);
  digitalWrite(Res250, LOW);
  digitalWrite(Res500, LOW);
  digitalWrite(Res1000, LOW);
  digitalWrite(CapShort, LOW);
  digitalWrite(Cap8_2, LOW);
  digitalWrite(Cap16, LOW);
  digitalWrite(Cap33, LOW);
  digitalWrite(Cap62, LOW);
  digitalWrite(Cap127, LOW);
  digitalWrite(Cap256, LOW);
  digitalWrite(Cap510, LOW);
  digitalWrite(Cap1020, LOW);
  digitalWrite(Cap2040, LOW);
  digitalWrite(Cap4100, LOW);
  digitalWrite(Cap8200, LOW);
  digitalWrite(Cap16400, LOW);
  digitalWrite(Ind31_25m, LOW);
  digitalWrite(Ind62_5m, LOW);
  digitalWrite(Ind125m, LOW);
  digitalWrite(Ind250m, LOW);
  digitalWrite(Ind500m, LOW);
  digitalWrite(Ind1, LOW);
  digitalWrite(Ind2, LOW);
  digitalWrite(Ind4, LOW);
  digitalWrite(Ind8, LOW);
  digitalWrite(Ind16, LOW);
}

/* This function sets the resistive network to the closest possible
 * value given. Possible values that the network can achieve are discrete.
 * Decimal values should be rouneded down. Values represents Ohms.
 */
int set_r(int rToSet) {
  
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
  return resRemaining;
} // end SetR

/* This function sets the inductive network to the closest possible
 * value given. Possible values that the network can achieve are discrete.
 * Decimal values should be rouneded down. Values represents mH.
 */
int set_l(int lToSet) {
  int indRemaining = lToSet;
  
   if (indRemaining >= 16000) {
    digitalWrite(Ind16, HIGH);
    indRemaining -= 16000;
  }
  
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
  return indRemaining;
} // end SetL


/* This function sets the capacitive network to the closest possible
 * value given. Possible values that the network can achieve are discrete.
 * Decimal values should be rouneded down. Values represents Farads.
 */
int set_c(int cToSet) {
  
  // If no capicitance to set, short the caps
  if (cToSet < 8) {
    digitalWrite(CapShort, HIGH);
    return 0;
  }
  
  int capRemaining = cToSet;
  
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
  return capRemaining;
} // end SetC
