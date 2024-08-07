import re
import os
import configparser

# Load the configuration file
config = configparser.ConfigParser()
config.read('config.ini')

# Retrieve variables from the config file
sender = config.get('settings', 'sender')
receiver = config.get('settings', 'receiver')

# Define the input file path
input_file = 'input/+12064022950.txt'

# Define the output file path (current working directory)
output_file = f'txt_files/{sender}_pretag.txt'

# Define the text replacements
replacements = {
    r'\+12064022950': sender,  # Use raw string for the phone number to escape the '+'
    r'Read by them': f'Read by {sender}',
    r'Read by you': f'Read by {receiver}'
}

# Read the contents of the input file
with open(input_file, 'r') as file:
    data = file.read()

# Apply replacements
for old, new in replacements.items():
    data = re.sub(old, new, data, flags=re.IGNORECASE)

# Write the updated data to the output file
with open(output_file, 'w') as file:
    file.write(data)

print(f"Tagged messages exported to '{output_file}'.")
