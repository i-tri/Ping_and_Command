import pandas as pd
from netmiko import ConnectHandler
from tkinter import Tk, Label, Entry, Button, filedialog, StringVar, messagebox
import threading
import time
from datetime import datetime


# Function to browse for input Excel file
def browse_file():
    file_path = filedialog.askopenfilename(title="Select Excel file", filetypes=[("Excel files", "*.xlsx *.xls")])
    input_file_var.set(file_path)


# Function to execute SSH commands in a separate thread
def execute_command_thread():
    input_file = input_file_var.get()
    command = command_var.get()

    # Check if file and command are provided
    if not input_file:
        messagebox.showerror("Error", "Please select an input Excel file.")
        return
    if not command:
        messagebox.showerror("Error", "Please enter a command to execute.")
        return

    # Read IP addresses and credentials from the Excel file
    df = pd.read_excel(input_file)

    # Ensure necessary columns are present
    required_columns = {'IP Address', 'User Name', 'Password'}
    if not required_columns.issubset(df.columns):
        messagebox.showerror("Error", "Excel file must contain 'IP Address', 'User Name', and 'Password' columns.")
        return

    # Store results
    results = []

    # Loop through each row in the Excel file
    for index, row in df.iterrows():
        ip = row['IP Address']
        username = row['User Name']
        password = row['Password']

        # Device parameters for Netmiko
        device = {
            'device_type': 'cisco_ios',  # Adjust to the appropriate device type
            'ip': ip,
            'username': username,
            'password': password,
        }

        # Connect via Netmiko and run command
        try:
            with ConnectHandler(**device) as ssh:
                output = ssh.send_command(command)
                results.append([ip, 'Success', output if output else 'No output'])

        except Exception as e:
            results.append([ip, 'Failure', str(e)])

    # Save results to new Excel file with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f'ssh_command_results_{timestamp}.xlsx'
    result_df = pd.DataFrame(results, columns=['IP Address', 'Status', 'Output'])
    result_df.to_excel(output_file, index=False)

    # Update status and enable button after completion
    messagebox.showinfo("Completed", f"Results saved to {output_file}")
    status_label.config(text="Execution Completed")
    execute_button.config(state="normal")


# Function to manage the moving dots animation
def animate_status():
    dots = ""
    while execute_button['state'] == "disabled":
        dots = "." * ((len(dots) + 1) % 4)  # Cycles between ".", "..", "..."
        status_label.config(text=f"Executing Command{dots}")
        time.sleep(0.5)


# Function to start command execution with threading
def start_execution():
    execute_button.config(state="disabled")
    status_label.config(text="Executing Command...")

    # Start the animation in a separate thread
    animation_thread = threading.Thread(target=animate_status)
    animation_thread.start()

    # Start the command execution in a separate thread
    command_thread = threading.Thread(target=execute_command_thread)
    command_thread.start()


# Set up GUI
root = Tk()
root.title("SSH Command Executor")

# Variables for file path and command
input_file_var = StringVar()
command_var = StringVar()

# Description label
description = """This program will execute the provided SSH command on the nodes listed in the Input Excel file.
The input file musts contain 3 columns: Ip Address, User Name, Password
The output will be saved in a separate Excel file with the IP, Ping Result, and Command Output."""
Label(root, text=description, wraplength=400, justify="left").grid(row=0, column=0, columnspan=3, padx=10, pady=10)

# GUI layout
Label(root, text="Select Input Excel File:").grid(row=1, column=0, padx=10, pady=5)
Entry(root, textvariable=input_file_var, width=50).grid(row=1, column=1, padx=10, pady=5)
Button(root, text="Browse", command=browse_file).grid(row=1, column=2, padx=10, pady=5)

Label(root, text="Enter Command to Execute:").grid(row=2, column=0, padx=10, pady=5)
Entry(root, textvariable=command_var, width=50).grid(row=2, column=1, padx=10, pady=5)

# Execute button and status label
execute_button = Button(root, text="Execute Command", command=start_execution)
execute_button.grid(row=3, column=1, pady=10)

status_label = Label(root, text="")
status_label.grid(row=4, column=1, pady=5)

# Run the GUI
root.mainloop()
