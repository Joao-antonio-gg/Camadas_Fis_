char mensagem = 'a';
int time_d = 1666;
  char pin = 13;

void setup() {
  Serial.begin(9600); // Configura a comunicação serial com a taxa de transmissão de 9600 baud
  pinMode(pin,OUTPUT);
  digitalWrite(13,HIGH);
}

void loop() {
  digitalWrite(pin,LOW);
  delay_t();
  
  int num = 0; 
  for (int i = 0; i < 8; i++) {
    digitalWrite(pin,mensagem >> i & 1);
    num += mensagem>>i & 1;
    delay_t();
  }

  char paridade = parityBit(mensagem);
  digitalWrite(pin,paridade);
  delay_t(); 

  digitalWrite(pin,HIGH);
  delay_t();
}


bool parityBit(char message) {
  int valor = 0;
  for (int i = 0; i < 8; i++) {
    if ((message >> i) & 1) {
      valor++;
    }
  }  
  int resto = valor % 2;
  return resto;
}

void delay_t(){
  for (int i=0;i<time_d;i++){
      asm ("nop");
  }
}
