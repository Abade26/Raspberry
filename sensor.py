from machine import Pin, I2C, ADC
import ssd1306
import time

# Configuração do I2C
i2c = I2C(0, scl=Pin(1), sda=Pin(0), freq=400000)
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

# Configuração do sensor MQ-135
mq135 = ADC(Pin(26))  # Usando GP26 como entrada analógica

# Configuração do LED (pode usar um pino disponível)
led = Pin(25, Pin.OUT)  # Exemplo: LED no pino GP25

# Lista para armazenar as últimas leituras (gráfico)
readings = []

def read_mq135():
    # Lê o valor do sensor MQ-135
    return mq135.read_u16()  # Lê o valor em 16 bits (0-65535)

def draw_graph():
    # Limpa a área do gráfico
    oled.rect(0, 32, 128, 32, 0)  # Limpa o gráfico
    if len(readings) < 2:
        return  # Não desenha se houver menos de 2 pontos

    # Desenha o gráfico
    for i in range(1, len(readings)):
        # Escalando as leituras para se encaixar na tela
        y1 = 32 + (32 - (readings[i-1] // 2000))  # Ajuste a escala
        y2 = 32 + (32 - (readings[i] // 2000))    # Ajuste a escala
        if y1 >= 32 and y1 < 64 and y2 >= 32 and y2 < 64:
            # Desenha a linha entre os pontos
            oled.line(i-1, y1, i, y2, 1)

while True:
    # Limpa a tela
    oled.fill(0)

    # Lê o valor do MQ-135
    mq135_value = read_mq135()
    
    # Armazena a leitura e mantém apenas as últimas 128 leituras
    readings.append(mq135_value)
    if len(readings) > 128:
        readings.pop(0)

    # Exibe os valores na tela OLED
    oled.text('MQ-135 Value:', 0, 0)
    oled.text(str(mq135_value), 0, 10)

    # Desenha o gráfico
    draw_graph()

    # Verifica se o valor passou de 11800
    if mq135_value > 11800:
        led.on()  # Acende o LED
        oled.text('Alerta: Qualidade Ruim', 0, 20)  # Exibe mensagem
    else:
        led.off()  # Apaga o LED

    # Atualiza a tela
    oled.show()

    # Imprime o valor no console
    print(f'MQ-135 Value: {mq135_value}')

    # Aguarda um segundo antes da próxima leitura
    time.sleep(1)
