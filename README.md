# Ping_and_Command
Ping node, log in to node, run command and capture output in excel file for each IP address specified in Input File


# SSH Command Executor

This Python script provides a GUI application to execute SSH commands on a list of devices. The script reads device IP addresses and credentials from an Excel file, executes a specified command on each device, and saves the output in a new Excel file.

## Features
- Select an input Excel file with device IPs and credentials.
- Specify an SSH command to execute on each device.
- Shows progress in the GUI to indicate that the command is running.
- Saves results to an output Excel file with a timestamp, containing:
  - Device IP Address
  - Ping Result
  - Command Output

## Requirements
- **Python 3.x**
- **Netmiko**: For SSH connections.
- **pandas**: For Excel file manipulation.
- **openpyxl**: For reading/writing Excel files.
- **Tkinter**: For GUI creation.
- **Packages**: Install required packages with:
  ```bash
  pip install pandas netmiko openpyxl
  ```


## Input File Format
The input Excel file should contain three columns:

**IP Address:** The IP address of the device.

**User Name:** Username for SSH access.

**Password:** Password for SSH access.


## Usage
Run the Script: Execute the script by running:
```bash
python ssh_command_executor.py
```
**Select Input File:** Click the Browse button to select the Excel file with device details.

**Enter Command:** Type the SSH command to execute on each device in the Enter Command to Execute field.

**Execute:** Click Execute Command to start the SSH command execution.

**View Output:** The program will save an output file named ssh_command_results_*timestamp*.xlsx with columns for:

- **IP Address**

- **Status** (Success/Failure)

- **Output** (Command output or error message)



## GUI Details

The GUI has the following elements:

**Description Label:** Displays instructions for using the application.

**File Selector:** Allows users to browse for the input Excel file.

**Command Entry:** Field to specify the command to execute.

**Execute Button:** Initiates SSH command execution on the devices listed in the input file.

**Status Label:** Displays a moving dot animation during execution to indicate progress.



## Example Input Excel
Here is an example of the required format for the input Excel file:

|IP Address    |User Name |Password  |
|--------------|----------|----------|
|192.168.1.10  |	admin   |	admin123 |
| 192.168.1.11 | root     |	pass456  |

## Screenshot

### GUI prompting for information:
<img width="287" alt="Ping and command Screenshot" src="https://github.com/user-attachments/assets/e635fcdb-5f59-4f3b-9a7d-c36537f17b2c">



## Troubleshooting

**Connection Errors:** If any device is unreachable or credentials are incorrect, the program will log an error in the output file.

**Device Type:** The device type is currently set to "generic". Update this in the code if using a different device type.

## License
This project is open-source and free to use.
