import socket
import json
import logging
# import select

ip_address = ''
port = 168

# create a socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.bind((ip_address, port))

# to process snmp traps
def process_snmp_traps(trap_data):

    print(f"Received SNMP trap: {trap_data}")
    logging.basicConfig(filename='snmp_traps.log',level=logging.DEBUG, format=f"%(levelname)-8s: \t %(filename)s \t %(funcName)s \t %(lineno)s - %(message)s")
    logger = logging.getLogger("mylogger")
    logger.debug("trap_data: {}".format(trap_data))


def receiving_snmp_traps():

    while True:

        print(f"Socket bound to {ip_address}:{port}")

        # receive data from the client
        s.listen(5)

        # accept connections from outside
        c, address = s.accept()
        print(f"Connection from {address} has been established!")

        # # Set a timeout of 10 seconds

        # receive data from the client
        data = b''

        c.settimeout(5)  

        try:
            while True:
                packet = c.recv(1024)
                if not packet:
                    break
                data += packet

        except socket.timeout:
            print("Socket timeout")

        decode_data = data.decode('utf-8').strip()
        print(f"Data received from client: {repr(decode_data)}")       

        # convert the recieved data JSON array into python list 
        if decode_data.strip():
            try:
                json_string = json.dumps(decode_data)
                array_data = json.loads(json_string)
                process_snmp_traps(array_data)
            except json.JSONDecodeError:
                print("Invalid JSON format received")
        else:
            print("Empty data received")

        # close the connection and socket
        c.close()
        # receiving_snmp_traps()


while True:
    receiving_snmp_traps()