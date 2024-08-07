import re
import configparser

config = configparser.ConfigParser()
config.read('config.ini')
sender = config.get('settings', 'sender')
receiver = config.get('settings', 'receiver')

input_file_path = f'txt_files/{sender}_tagged.txt'
output_file_path = f'txt_files/{sender}_dates+sender.txt'

def clean_message_data(file_path, output_path):
    with open(file_path, 'r') as file:
        content = file.read()

    message_start_pattern = r'\{ Message \d+ Start \}'
    message_end_pattern = r'\{ Message \d+ End \}'

    def clean_message_block(block):
        def clean_date_line(line):
            date_match = re.match(r'(\w+ \d{2}, \d{4})', line)
            return date_match.group(1) if date_match else ''

        lines = block.split('\n')
        if len(lines) < 2:
            return ''

        lines[1] = clean_date_line(lines[1])

        sender_index = 2
        if sender_index >= len(lines):
            return ''

        sender_line = lines[sender_index].strip()
        if len(sender_line) == 0:
            return ''

        sender_line = sender_line.replace('Elly', sender).replace('Margot', receiver)

        cleaned_block = f'{lines[1]}\n{sender_line}\n'

        return cleaned_block

    message_blocks = re.split(message_start_pattern, content)[1:]
    cleaned_blocks = []

    for block in message_blocks:
        parts = re.split(message_end_pattern, block)
        if len(parts) < 2:
            continue

        header, body = parts[0], parts[1]
        cleaned_block = f'{{ Message Start }}\n{clean_message_block(header)}{{ Message End }}'
        cleaned_blocks.append(cleaned_block)

    cleaned_content = '\n\n'.join(cleaned_blocks)

    with open(output_path, 'w') as file:
        file.write(cleaned_content)

if __name__ == '__main__':
    clean_message_data(input_file_path, output_file_path)

print(f"Content removed, only message and sender remain, exported to: '{output_file_path}'.")
