import socket
import csv
import tkinter as tk
from tkinter import simpledialog
from tkinter import Button
import os
import threading
from tkinter import ttk

BUFFER_SIZE = 1024
CSV_FILENAME = 'RemoteEventLog.csv'

def get_message_from_code(code): #The first section of the recieved data is a code in hex which will be mapped to one of the below descriptions taken from vauban spreadsheet
    messages = {
      
        0: "Unknown ID",
        1 : "ID suspended",
        2 : "Stolen ID",
        3 : "Offsite ID",
        4 : "Non-distributor identifier",
        5 : "Identifier not assigned",
        6 : "Reserves",
	    7 : "Reserves",
	    8 : "Reserves",
    	9 : "Reserves",
        10 : "Access Granted",
        11 : "User accepted + Awaiting code",
        12 : "User forbidden",
        13 : "User already entered",
        14 : "User already logged out",
        15 : "Invalid user on door",
        16 : "User out of range",
        17 : "Door locked",
        18 : "Vehicle not detected",
        19 : "Group forbidden",
        20 : "Wrong Code",
        21 : "Keypad blocked",
        22 : "Maximum number of passages reached",
        23 : "User without code",
        24 : "User Out of Validity",
        25 : "User accepted + Attendant waiting",
        26 : "Guide refused",
        27 : "Companion accepted",
        28 : "Attendant timeout exceeded",
        29 : "Transit time exceeded",
        30 : "Unconditional",
        31 : "Fingerprint refused",
        32 : "User accepted + waiting for validation",
        33 : "Passage count",
        34 : "Reserves",
	    35 : "Reserves",
	    36 : "Reserves",	
	    37 : "Reserves",
	    38 : "Reserves",
	    39 : "Reserves",
        40 : "Burglary", #Conditional input
        41 : "Door blocked",
        42 : "End break-in", #Conditional input
        43 : "End door blocked",
        44 : "Door open at start of free access range",
        45 : "Door closed at end of free access range",
        46 : "Opening maintained by BMS",
        47 : "Closing maintained by BMS",
        48 : "BMS auto mode command",
        49 : "Impulse opening by BMS",
        50 : "Alarm arming (bistable mode)",
        51 : "Alarm disablement (bistable mode)",
        52 : "Pulse on/off alarm",
        53 : "Wiegand format error",
        54 : "Opening on BP", #Exit Button event
        55 : "Code entry timeout exceeded",
        56 : "End of keypad lock",
        57 : "Reader connection (VEXT232)",
        58 : "Reader disconnection (VEXT232)",
        59 : "Low battery (Aperio)",
        60 : "Battery OK (Aperio)",
        61 : "Aperio disconnected",
        62 : "Aperio connected",
        63 : "Radio interference (Aperio)",
        64 : "End of radio disturbances (Aperio)",
        65 : "Enable green BG",
        66 : "End of green BG activation",
        67 : "Reserves",
 	    68 : "Reserves",
        69 : "Reserves",
        70 : "Automation execution",
        71 : "End of automation execution",
        72 : "Enclosure break-in",
        73 : "End of box break-in",
        74 : "Power supply fault",
        75 : "Power supply fault reset",
        76 : "Alert Level Change",
        77 : "Extension bus connection",
        78 : "Extension bus disconnection",
        79 : "Access to menu",
        80 : "VEXTLCD button pressed",
        81 : "Code entered on VEXTLCD",
        87 : "Controller Start Up"
    }
    return messages.get(code, "Unknown code")

def save_data_to_csv(data): #Function which takes the recieved data and then splits it up and puts into the CSV file
    stripped_data = data[:-1]  # Remove only the last character
    code = int(stripped_data[:2], 16)
    message = get_message_from_code(code) #Function which decides which event descrpition will be printed to the CSV file
   
    reader_number = int(stripped_data[17])    # Extract reader number
    if reader_number == 0: #Check to see whether no reader number is present
        reader_str = " "
    else:
        reader_str = f"Reader {reader_number}"
    
    year = int(stripped_data[2:6]) #Date 
    month = int(stripped_data[6:8])
    day = int(stripped_data[8:10])

    hour = int(stripped_data[10:12]) #time
    minute = int(stripped_data[12:14])
    second = int(stripped_data[14:16])

    last_7_digits = stripped_data[-7:]  # Get the Card number
    if last_7_digits == "0000000":
        decimal_value = " "
    else:
        decimal_value = int(last_7_digits, 16)  # Convert the last 7 digits from hexadecimal to decimal
    
    datetime_str = f"{year}-{month:02d}-{day:02d} {hour:02d}:{minute:02d}:{second:02d}" #Puts the data from the date and time into one string


    with open(CSV_FILENAME, 'a', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow([datetime_str, message, decimal_value, reader_str])
      #  csv_writer.writerow([stripped_data, datetime_str, message, decimal_value])

def quit_program():
    os._exit(0)

def start_server(window, IP, PORT):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((IP, PORT))
        server_socket.listen(1)
        print(f'Listening on IP {IP} and port {PORT}')

        while True:
            window.update()  # Update the Tkinter window to keep it responsive
            conn, addr = server_socket.accept()
            with conn:
                print(f'Client connected from {addr}')
                while True:
                    data = conn.recv(BUFFER_SIZE)
                    if not data:
                        break
                    data_str = data[1:].decode('utf-8')  # Ignore the initial byte when decoding
                    print(f'Received data: {data_str}')
                    save_data_to_csv(data_str)
                print('Client disconnected')

# Keep the imports and other functions the same

def main():
    # Create a simple Tkinter window
    root = tk.Tk()
    root.withdraw()

    # Prompt user for IP address and port number
    IP = simpledialog.askstring(" ", "Enter IP address:", parent=root)
    PORT = simpledialog.askinteger(" ", "Enter port number:", parent=root)

    # Close the Tkinter window
    root.destroy()

    # Create a new Tkinter window with progress bar, label, and quit button
    window = tk.Tk()
    window.geometry("350x80")
    window.title("GARDiS Remote Event Listener")

    # Add a progress bar
    progress_bar = ttk.Progressbar(window, mode='indeterminate', length=300)
    progress_bar.pack()
    progress_bar.start(interval=20)  # Lower interval value for a quicker progress bar

    # Add a label for IP address and port number
    ip_port_label = tk.Label(window, text=f"Listening on IP Address: {IP} Port number: {PORT}")
    ip_port_label.pack()

    quit_button = Button(window, text="Quit", command=quit_program)
    quit_button.pack()

    # Start the server in a separate thread
    server_thread = threading.Thread(target=start_server, args=(window, IP, PORT)) # Pass the user-input IP and PORT
    server_thread.daemon = True
    server_thread.start()

    window.mainloop()

if __name__ == '__main__':
    main()
