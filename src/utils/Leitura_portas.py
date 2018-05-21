import glob
import sys
import codecs
import serial
import time
import binascii


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

'''Sub Serial_Parameters()

Dim SerialPort As Variant

'************************************************************
'SerialInterface
'************************************************************
IOSettingsCam "READ"

'Inicializa a comunicaçao com a placa serial (PORT=1)
SerialPort = 1
frmmain.Serial.CommPort = SerialPort
       
'*******************************************************************
'Baud rate = 9600, sem paridade, 1 stop bit e 8 bits de dados
frmmain.Serial.Settings = "9600,n,8,1"

'*******************************************************************
frmmain.Serial.NullDiscard = False
frmmain.Serial.InputLen = 1
frmmain.Serial.InBufferCount = 0
-
'*******************************************************************
'Nao aceita ocorrencia de EVENTOS na recepcao ( = 0 )Threshold=limiar
frmmain.Serial.RThreshold = 1
frmmain.Serial.SThreshold = 0
frmmain.Serial.RTSEnable = False
frmmain.Serial.DTREnable = True

'*******************************************************************
'Dimensiona o vetor do protocolo na inicialização
bytes = 5
elemento = 1
ReDim frame_aux(5) As Byte
ReDim frame(5) As Byte
End Sub'''


def processa_frame(statesh):
    frame = statesh.frame
    try:
        if frame[3] == 5:
            filter_temp = (8.0036 * (0.001221 * (frame[5] + (256 * float(frame[6])))) - 2.5794)
            print("Filter Temperature: " + str(filter_temp))
        elif frame[3] == 17:
            bytenum = 5
            elemento = 1
            bytes(statesh.frame_aux[5])
            bytes(statesh.frame[5])
        elif frame[3] == 6:
            print('FRAME DE ERRO NO OBTURADOR')
        else:
            print('Tipo desconhecido (Falha grave na serial)')
    except Exception as e:
        # Resume Next???
        print("Frame Processing: " + str(e))


# hex(174)[2:]
def SerialShutter(StateSh):
    bytes(StateSh.frame_aux[5])
    bytes(StateSh.frame[5])
    expected_bytes = 5
    # elemento = 1
    global transdado, tipo_oper, ser
    portlist = serial_ports()
    for i in range(0, len(portlist)):
        ser = serial.Serial(portlist[i])  # open serial port
        print(ser.name)  # check which port was really used
    while ser.out_waiting != expected_bytes:
        if StateSh == "CLOSED":
            transdado = hex(235)[2:] + hex(144)[2:] + hex(214)[2:] + \
                        hex(1)[2:] + hex(174)[2:]
            tipo_oper = "obtoff"
        else:
            transdado = hex(235)[2:] + hex(144)[2:] + hex(86)[2:] + \
                        hex(1)[2:] + hex(46)[2:]
            tipo_oper = "obton"
    return transdado, tipo_oper


def open_default_port():
    global count
    # portlist = serial_ports()
    ser = serial.Serial('COM2', 9600, bytesize=serial.EIGHTBITS,
                        parity=serial.PARITY_NONE,
                        stopbits=serial.STOPBITS_ONE, timeout=5)# open serial port
    ser.close()
    '''ser.set_buffer_size()
    ser.set_input_flow_control()'''
    ser.setDTR(True)
    ser.setRTS(False)
    ser.open()
    # ser.is_open()
    #transdado = 'EB905601'
    '''transdado = hex(235)[2:] + hex(144)[2:] + hex(86)[2:] + '0' + hex(1)[2:] + hex(46)[2:]
    # q = transdado[7]
    #newRegisterValue = bits_to_hex(input)
    ntransdado=bytearray.fromhex(transdado)
    print(transdado)
    print(ntransdado)
    print(len(ntransdado))'''
    print("Escrevendo: " + binascii.hexlify(bytes([235, 144, 86, 1, 46])).decode())
    ser.write(binascii.hexlify(bytes([235, 144, 86, 1, 46])))
    #ser.write(transdado) # abrir obturador
    #in_put = 'b\xEB\x90\x56\x01\xAE'
    #ser.write(in_put)
    #ser.write(b'eb90d601ae')  # fechar obturador
    print("passou aqui")
    #ser.write(transdado.encode())
    # print("passou aqui")
    int.from_bytes()

    # print("passou aqui")
    print("Resultado: " + ser.read_all().decode())
    """for line in ser.read():
        print("passou aqui")
        print(str(count) + str(': ') + chr(line))
        count = count + 1"""
    '''for i in range(0, len(portlist)):

        ser = serial.Serial(portlist[i], 9600, bytesize=serial.EIGHTBITS,
                                    parity=serial.PARITY_EVEN, rtscts=1)  # open serial port

        #print(ser.name)  # check which port was really used
        transdado = hex(235)[2:] + hex(144)[2:] + hex(214)[2:] + \
                    hex(1)[2:] + hex(174)[2:]
        tt = b'String'
        ser.write(transdado)

        for line in ser.read():
            print(str(count) + str(': ') + chr(line))
            count = count + 1'''
            # ser.write(b'hello')  # write a string
    ser.close()  # close port

def open_aux_port():
    import serial
    # Equivalente em Windows?
    ser = serial.Serial('COM1')  # open serial port
    print(ser.name)  # check which port was really used
    ser.write(b'hello')
    ser.read()# write a string
    ser.close()  # close port

# open_default_port()
# print(SerialShutter(open_default_port()))