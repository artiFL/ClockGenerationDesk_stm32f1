import sys
import glob
from numpy import byte
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

freq_pic = 100000000


span = 20000000
LO_pic = freq_pic - span / 2

def main():
    list_ports = serial_ports()
    print(list_ports)

    heterodine = serial.Serial("/dev/tty.usbmodem6D783F5A53491", 115200)  # open serial port
    input = serial.Serial("/dev/tty.usbmodem8D89426B56511", 115200)  # open serial port
    time.sleep(1)
    #input.write(b"start_spam 1 2000000000 10000 2000100000 \n") 


    RF_freq = 'clock Hz ' + str(freq_pic) + '\n'
    input.write(bytes(RF_freq, encoding="utf-8"))  
    
    
    LO_frreq = 'clock Hz ' + str(LO_pic) + '\n'
    heterodine.write(bytes(LO_frreq, encoding="utf-8"))  
    print(f'RF = {freq_pic}  LO = {LO_pic}')

    print("Succes")
    input.close()
    heterodine.close()

if __name__ == '__main__':
    main()