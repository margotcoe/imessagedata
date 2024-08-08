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
    r'\+12064022950': sender,
    r'Read by them': f'Read by {sender}',
    r'Read by you': f'Read by {receiver}'
}

with open(input_file, 'r') as file:
    data = file.read()

for old, new in replacements.items():
    data = re.sub(old, new, data, flags=re.IGNORECASE)

with open(output_file, 'w') as file:
    file.write(data)

print(f"Tagged messages exported to '{output_file}'.")
