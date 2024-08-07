import re
import os
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

sender = config.get('settings', 'sender')
receiver = config.get('settings', 'receiver')
input = config.get('settings', 'input')

input_file = '{input}' 

output_file = f'txt_files/{sender}_pretag.txt'

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
