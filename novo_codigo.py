from machine import Pin, I2C, ADC
import ssd1306
import time

# Configuração do I2C
i2c = I2C(0, scl=Pin(1), sda=Pin(0), freq=400000)
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

# Configuração dos sensores MQ-135 e MQ-7
mq135 = ADC(Pin(26))  # MQ-135 no GP26
mq7 = ADC(Pin(27))    # MQ-7 no GP27

# Configuração do LED (pode usar um pino disponível)
led = Pin(25, Pin.OUT)  # Exemplo: LED no pino GP25

# Lista para armazenar as últimas leituras (gráfico)
readings = []

def read_mq135():
    # Lê o valor do sensor MQ-135
    return mq135.read_u16()  # Lê o valor em 16 bits (0-65535)

def read_mq7():
    # Lê o valor do sensor MQ-7
    return mq7.read_u16()  # Lê o valor em 16 bits (0-65535)

def evaluate_air_quality(value):
    if value > 30000:
        return "Péssima"
    elif value > 20000:
        return "Ruim"
    elif value > 10000:
        return "Moderada"
    else:
        return "Boa"

def draw_graph():
    # Limpa a área do gráfico
    oled.rect(0, 32, 128, 32, 0)
    if len(readings) < 2:
        return  # Não desenha se houver menos de 2 pontos

    # Desenha o gráfico
    for i in range(1, len(readings)):
        y1 = 32 + (32 - (readings[i-1] // 2000))
        y2 = 32 + (32 - (readings[i] // 2000))
        if y1 >= 32 and y1 < 64 and y2 >= 32 and y2 < 64:
            oled.line(i-1, y1, i, y2, 1)

while True:
    oled.fill(0)

    # Lê os valores dos sensores
    mq135_value = read_mq135()
    mq7_value = read_mq7()
    
    # Determina a qualidade do ar com base no MQ-7
    air_quality = evaluate_air_quality(mq7_value)
    
    # Armazena a leitura e mantém apenas as últimas 128 leituras
    readings.append(mq135_value)
    if len(readings) > 128:
        readings.pop(0)

    # Exibe os valores e a qualidade do ar na tela OLED
    oled.text('MQ-135 Value:', 0, 0)
    oled.text(str(mq135_value), 0, 10)
    oled.text('MQ-7 Quality:', 0, 20)
    oled.text(air_quality, 0, 30)

    # Desenha o gráfico
    draw_graph()

    # Verifica a qualidade do ar para acender o LED
    if mq7_value > 20000:
        led.on()  # Acende o LED
    else:
        led.off()  # Apaga o LED

    # Atualiza a tela
    oled.show()

    # Imprime o valor e a qualidade no console
    print(f'MQ-135 Value: {mq135_value}, MQ-7 Value: {mq7_value}, Air Quality: {air_quality}')

    # Aguarda um segundo antes da próxima leitura
    time.sleep(1)
