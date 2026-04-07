import serial
import json
import requests
import time

PORTA = 'COM5' 
BAUD = 9600
URL = 'http://127.0.0.1:5000/leituras'

def ler_serial():
    try:
        # O 'errors=ignore' ajuda a ignorar caracteres estranhos no boot do Arduino
        ser = serial.Serial(PORTA, BAUD, timeout=1) 
        print(f"Conectado na porta {PORTA}. Aguardando dados...")
        
        while True:
            linha = ser.readline().decode('utf-8', errors='ignore').strip()
            if linha:
                # Verifica se a linha realmente parece um JSON (começa com {)
                if linha.startswith('{'):
                    try:
                        dados = json.loads(linha)
                        response = requests.post(URL, json=dados)
                        print(f"Sucesso! Enviado: {dados} | Servidor respondeu: {response.status_code}")
                    except Exception as e:
                        print(f"Erro ao enviar para API: {e}")
                else:
                    # Ignora avisos como "Sensor nao encontrado"
                    print(f"Ignorando texto (nao e JSON): {linha}")
            
            time.sleep(0.1)

    except Exception as e:
        print(f"Erro na Serial: {e}")
        time.sleep(2)
        return ler_serial()

if __name__ == '__main__':
    ler_serial()