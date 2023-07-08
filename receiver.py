import socket
import json
import logging
from trap_mail import generate_mail
from data_processing import decoding_snmp_traps

ip_address = ''
port = 164

# create a socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.bind((ip_address, port))

# to process snmp traps
def process_snmp_traps(trap_data):
    oid_value_pairs = trap_data.split(" ")[9:]
    print(oid_value_pairs[1])
    trap_oid = oid_value_pairs[1].split("=")[1]

    message = decoding_snmp_traps(trap_oid)



    print(f"Message: {message}")
    generate_mail(message)

    logging.basicConfig(
    filename='snmp_traps.log',
    level=logging.DEBUG,
    format='%(asctime)s  %(levelname)-8s: %(process)d %(thread)d %(message)s')
    logger = logging.getLogger("mylogger")
    logger.info(format(message))


def receiving_snmp_traps():

    while True:

        print(f">>> Socket bound to {ip_address}:{port}")

        # receive data from the client
        s.listen(5)

        # accept connections from outside
        c, address = s.accept()
        print(f">>> Connection from {address} has been established!")

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
            print(">>> Socket timeout")

        decode_data = data.decode('utf-8').strip()
        print(f"Data received from client: {repr(decode_data)}")       

        # convert the recieved data JSON array into python list 
        if decode_data.strip():
            try:
                json_string = json.dumps(decode_data)
                array_data = json.loads(json_string)
                process_snmp_traps(array_data)
            except json.JSONDecodeError:
                print(">>> Invalid JSON format received")
        else:
            print(">>> Empty data received")

        # close the connection and socket
        c.close()
        # receiving_snmp_traps()

while True:
    receiving_snmp_traps()
