import re
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

sender = config.get('settings', 'sender')
receiver = config.get('settings', 'receiver')

input_file_path = f'txt_files/{sender}_pretag.txt'
output_file_path = f'txt_files/{sender}_tagged.txt'  
date_pattern = r'\b[A-Za-z]{3} \d{2}, \d{4}\b'

def split_messages(text):
    dates = [match.start() for match in re.finditer(date_pattern, text)]

    messages = []
    for i in range(len(dates)):
        start = dates[i]
        end = dates[i + 1] if i + 1 < len(dates) else len(text)
        messages.append(text[start:end].strip())

    return messages

with open(input_file_path, 'r') as file:
    data = file.read()

messages = split_messages(data)

with open(output_file_path, 'w') as file:
    for i, message in enumerate(messages, start=1):
        file.write(f"{{ Message {i} Start }}\n")
        file.write(message + '\n')
        file.write(f"{{ Message {i} End }}\n\n")

print(f"Tagged messages exported to '{output_file_path}'.")
