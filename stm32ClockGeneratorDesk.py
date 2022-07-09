import sys
import glob
import serial
import time
def serial_ports():
    """ Lists serial port names

        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
    """
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result

def write_package(serial, data):
        data.replace("\r\n", "")
        strings = f"{data[0:2]} {data[2:6]} {data[8:16]} {data[16:24]} {data[24:32]} {data[41:42]}"
        print(strings)
        for byte in strings:
            print(byte, end=' ')
        print("\n")

        send_message = "write_mem " + strings
        serial.write(bytes(send_message,'UTF-8'))     # write a string
        ack = serial.readline()
        print(ack)
        return ack

def write_mem(serial):
    with open("/Users/artemflegler/Desktop/Bander_boot.hex", 'rb') as file:
        data = file.read()
    data = str(data)
    d_string = data.split(":")[2:-3]
    flag = True
    for x in d_string:
        if flag == True:
            ack = write_package(serial, x)
            if ack == bytes("OK\n",'UTF-8'):
                flag = True
            elif ack == bytes("nock\n",'UTF-8'):
                flag = False
                print("nock")
                break
    print("succes programm")

def read_mem(serial, address, count_byte):
    list_hex = []
    send_message = "read_mem " + str(address) + ' ' + str(count_byte)
    print(send_message)
    serial.write(bytes(send_message,'UTF-8'))
    for x in range(count_byte):
        x = serial.readline()
        print(x)

def main():
    list_ports = serial_ports()
    print(list_ports)

    ser = serial.Serial("/dev/tty.usbmodem6D783F5A53491", 115200)  # open serial port
    #ser = serial.Serial("/dev/tty.usbmodem8D89426B56511", 115200)  # open serial port

    print(ser)         # check which port was really used
    time.sleep(1)
    #ser.write(b"start_spam 0 36000000 100000 36500000 \n")
    ser.write(b"clock Hz 968000000 \n")     
    print("Succes")
    ser.close()
    #while 1:

    #    x = ser.readline()
    #    print(x)
    #    time.sleep(1)



    #write_mem(ser)
    #read_mem(ser, 0x080Feff4, 2000)

    #ser.close()             # close port

if __name__ == '__main__':
    main()