import socket
import json
import logging
from trap_mail import generate_mail
from data_processing import *
from database import store_trap_messages
import threading
import tkinter as tk
from PIL import ImageTk, Image


def test_func(entry):
    output_text.insert("end", entry + "\n")


# to process snmp traps
def process_snmp_traps(trap_data):

    details, oid_pair_dictionary = decode_message(trap_data)
    details_list = details.split(" ")


    trap_oid = oid_pair_dictionary[".1.3.6.1.6.3.1.1.4.1.0"]
    
    message = decoding_snmp_traps(trap_oid)

    logging.basicConfig(
    filename='snmp_traps.log',
    level=logging.DEBUG,
    format='%(asctime)s  %(levelname)-8s: %(process)d %(thread)d %(message)s')
    logger = logging.getLogger("mylogger")

    if(trap_oid == ".1.3.6.1.4.1.9.9.513.0.11"):
        logger.warning(format(message))
        location= oid_pair_dictionary[".1.3.6.1.4.1.9.9.513.1.1.1.1.5.0"] 
        message = f"{message} the router in the {location} has gone DOWN. Please check the router. Thank you!"
        generate_mail(message)
        test_func(">>> Email sent!")
        print(oid_pair_dictionary[".1.3.6.1.4.1.9.9.513.1.1.1.1.5.0"])
    elif(trap_oid == ".1.3.6.1.4.1.9.9.599.0.6"):
        logger.info(format(message))
        temp= "CLIENT DISSOCIATION:"
        message = f"{temp} {message}"
        generate_mail(message)
        test_func(">>> Email sent!")
    elif(trap_oid == ".1.3.6.1.4.1.9.9.599.0.7"):
        logger.info(format(message))
        temp= "CLIENT ASSOCIATION:"
        message = f"{temp} {message}"
        generate_mail(message)
        test_func(">>> Email sent!")
    elif(trap_oid == ".1.3.6.1.4.1.9.9.599.0.9"):
        logger.info(format(message))
        temp= "Station establishes a connection or association with a controller."
        message = f"{temp} {message}"
        generate_mail(message)
        test_func(">>> Email sent!")
    else:
        logger.info(format(message))

    print(f"Message: {message}")
    test_func(f"Message: {message}")
    test_func("----------------------------------------------")




def receiving_snmp_traps():

    while True:

        print(f">>> Socket bound to {ip_address}:{port}")
        test_func(f">>> Socket bound to {ip_address}:{port}")

        # receive data from the client
        s.listen(5)

        # accept connections from outside
        c, address = s.accept()
        print(f">>> Connection from {address} has been established!")
        test_func(">>> Connection from has been established!")

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
            test_func(">>> Socket timeout")

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
                test_func(">>> Invalid JSON format received")
                test_func("----------------------------------------------")
        else:
            print(">>> Empty data received")
            test_func(">>> Empty data received")
            test_func("----------------------------------------------")

        # close the connection and socket
        c.close()
        # receiving_snmp_traps()


# def start_snmp_trap_receiver():
#     # Start the SNMP trap receiver in a separate thread
#     # while True:

def start_snmp_trap_receiver():
    receiving_snmp_thread = threading.Thread(target=receiving_snmp_traps)
    receiving_snmp_thread.start()


HEIGHT = 590
WIDTH = 590

def show_snmp_logs():
    try:
        with open('snmp_traps.log', 'r') as log_file:
            log_contents = log_file.read()
            output_text.delete(1.0, tk.END)  # Clear the existing content
            output_text.insert(tk.END, log_contents)
    except FileNotFoundError:
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, "snmp_traps.log not found!")

def clear_screen():
    output_text.delete(1.0, tk.END)

root = tk.Tk()
root.title("SNMP Trap Receiver")

# Create the canvas
canvas = tk.Canvas(root, height=HEIGHT, width=WIDTH)
canvas.pack()

image = Image.open('newdelgihxgo.jpeg')
background_image = ImageTk.PhotoImage(image)
background_label = tk.Label(root, image=background_image)
background_label.place(relwidth=1, relheight=1)

output_frame = tk.Frame(root, bg="white")
output_frame.place(relwidth=0.85, relheight=0.7, relx=0.5, rely=0.05, anchor="n")

output_text = tk.Text(output_frame, bg="black", fg="white")
output_text.pack(fill="both", expand=True, padx=5, pady=5)

frame = tk.Frame(root, bg="white")
frame.place(relwidth=0.85, relheight=0.1, relx=0.5, rely=0.8, anchor="n")

button_snmp_listener = tk.Button(frame, text="SNMP listener", bg="white", fg="black", command=start_snmp_trap_receiver)
button_snmp_listener.place(relx=0.025, rely=0.1, relwidth=0.3, relheight=0.8)

button_show_logs = tk.Button(frame, text="Show Logs", bg="white", fg="black", command=show_snmp_logs)
button_show_logs.place(relx=0.35, rely=0.1, relwidth=0.3, relheight=0.8)

button_clear_screen = tk.Button(frame, text="Clear Screen", bg="white", fg="black", command=clear_screen)
button_clear_screen.place(relx=0.675, rely=0.1, relwidth=0.3, relheight=0.8)


ip_address = ''
port = 164

# create a socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.bind((ip_address, port))


# Start the tkinter main event loop
root.mainloop()
