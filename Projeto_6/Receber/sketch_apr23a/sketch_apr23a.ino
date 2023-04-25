char mensagem = "";
char pin = 13;
int time_d = 1666;
int meio_t_d = 2499;
void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(pin,INPUT);

}

void loop() {
  // put your main code here, to run repeatedly:
  
  bool teste = true;

  while(teste){
    teste = digitalRead(pin);
  }
  delay_t1();
  
  for (int i = 0; i<8;i++){
    char digit = digitalRead(pin)<<i;
    delay_t(); 
  }

  delay_t();

  char parity_b = digitalRead(pin);
  if (parityBit(mensagem) == parity_b){
    Serial.println(mensagem);
  }
  else{
    Serial.println("ERRO ERRO ERRO");
  }

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


void delay_t1(){
  for (int i=0;i<meio_t_d ;i++){
      asm ("nop");
  }
}
