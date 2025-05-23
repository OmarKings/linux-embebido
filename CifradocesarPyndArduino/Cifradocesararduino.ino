/*
  ArduinoSerialBridge.ino
  Comunicación serial con el cliente Python:
  - Espera el mensaje de “HELLO” y responde con “WORLD”
  - Luego, recibe líneas de texto y las devuelve prefijadas con “Echo: ”
*/

void setup() {
  // Inicia la comunicación serial a 9600 baudios (debe coincidir con el Python)
  Serial.begin(9600);
  // Espera hasta que el puerto serie esté listo
  while (!Serial) {
    ; // nada
  }
}

void loop() {
  // Si hay datos entrantes en el buffer serial
  if (Serial.available()) {
    // Lee hasta el salto de línea '\n'
    String line = Serial.readStringUntil('\n');

    // Elimina posibles retornos de carro o espacios al final
    line.trim();

    // Handshake inicial: si recibe "HELLO", responde "WORLD"
    if (line == "HELLO") {
      Serial.println("WORLD");
    }
    else {
      // Para cualquier otro texto, lo devuelve como eco
      Serial.print("Echo: ");
      Serial.println(line);
    }
  }
}
