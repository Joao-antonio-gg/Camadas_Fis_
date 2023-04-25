int reciever = 13;
int clockCicles = F_CPU/9600;
bool readValue;
char recebeu = "";
bool paridade;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(reciever, INPUT);
}

void loop() {
  // put your main code here, to run repeatedly:
  readValue = true;
  while(readValue){
    readValue = digitalRead(reciever);
    
  }
  firstDelay();
  int i = 0;
  while(i < 8){
    recebeu |= digitalRead(reciever)<<i|recebeu;
    unitDelay();
    i++;
  }
  Serial.println(recebeu);
  paridade = digitalRead(reciever);
  if (parityBit(recebeu) == paridade){
    Serial.println(recebeu);
  }
  else{
    Serial.print("Erro no envio da mensagem");
  }
  delay(5000);
}

void unitDelay(){
  for (int i = 0; i < 1666 ;i++){ asm("NOP"); }
}

void firstDelay(){
  for (int i = 0; i < 2500 ;i++){ asm("NOP"); }
}
bool parityBit(char message){
  int soma = 0;
  for (int i = 0; i < 8; i++){ if ((i >> message) & 1) { soma++; }}
  int resto = soma % 2;
  return resto;
}
