import csv
from datetime import datetime
import re
import configparser

config = configparser.ConfigParser()
config.read('config.ini')
sender = config.get('settings', 'sender')
receiver = config.get('settings', 'receiver')

input_file_path = f'txt_files/{sender}_dates+sender.txt'
output_file_path = f'outputs/requited/{sender}_dates_and_senders.csv'

def parse_dates_and_senders(file_path):
    records = []

    with open(file_path, 'r') as file:
        content = file.read()

    blocks = content.split('{ Message End }')

    for block in blocks:
        block = block.strip()
        if not block:
            continue

        lines = block.split('\n')
        lines = [line.strip() for line in lines if line.strip() and line.strip() != '{ Message Start }']

        if len(lines) == 2:
            date_line = lines[0]
            sender_line = lines[1]

            date_match = re.match(r'^(\w+ \d{2}, \d{4})$', date_line)
            if date_match:
                date_str = date_match.group(1)
                date = datetime.strptime(date_str, '%b %d, %Y').date()

                if sender_line in [receiver, sender]:
                    records.append({'Date': date.strftime('%Y-%m-%d'), 'Sender': sender_line})

    return records

def write_to_csv(records, file_path):
    with open(file_path, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['Date', 'Sender'])
        writer.writeheader()
        for record in records:
            writer.writerow(record)

if __name__ == '__main__':
    records = parse_dates_and_senders(input_file_path)
    if records:
        write_to_csv(records, output_file_path)
        print(f'Records have been written to {output_file_path}')
    else:
        print('No records were found.')
