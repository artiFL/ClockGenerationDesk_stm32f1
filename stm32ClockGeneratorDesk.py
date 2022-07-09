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

if __name__ == '__main__':
    main()