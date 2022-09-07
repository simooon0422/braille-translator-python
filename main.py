from machine import Pin,UART

uart = UART(0,9600)

while True:
    if uart.any():
        command = uart.read()
        message = str(command.rstrip(), 'utf8')#str(command)#command.decode('utf-8')#str(command.rstrip(), 'utf8')
        print(message)

        
