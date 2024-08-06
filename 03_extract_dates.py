import re

input_file_path = 'txt_files/elly_tagged.txt'
output_file_path = 'txt_files/elly_dates+sender.txt'

def clean_message_data(file_path, output_path):
    with open(file_path, 'r') as file:
        content = file.read()

    # Define regex patterns
    message_start_pattern = r'\{ Message \d+ Start \}'
    message_end_pattern = r'\{ Message \d+ End \}'

    def clean_message_block(block):
        # Clean the date line to keep only the date
        def clean_date_line(line):
            date_match = re.match(r'(\w+ \d{2}, \d{4})', line)
            return date_match.group(1) if date_match else ''
        
        # Split the block into lines
        lines = block.split('\n')
        
        if len(lines) < 2:
            return ''  # Not a valid block
        
        # Clean the date line
        lines[1] = clean_date_line(lines[1])
        
        # Find the index of the sender line
        sender_index = 2
        if sender_index >= len(lines):
            return ''  # Not a valid block
        
        # Only keep the sender line and add an empty line before the message end
        sender_line = lines[sender_index].strip()
        if len(sender_line) == 0:
            return ''  # Skip if sender line is empty

        cleaned_block = f'{lines[1]}\n{sender_line}\n'
        
        return cleaned_block
    
    # Split the content into message blocks
    message_blocks = re.split(message_start_pattern, content)[1:]
    cleaned_blocks = []
    
    for block in message_blocks:
        parts = re.split(message_end_pattern, block)
        if len(parts) < 2:
            continue
        
        header, body = parts[0], parts[1]
        
        # Clean the message block
        cleaned_block = f'{{ Message Start }}\n{clean_message_block(header)}{{ Message End }}'
        cleaned_blocks.append(cleaned_block)
    
    # Join the cleaned blocks into a single content
    cleaned_content = '\n\n'.join(cleaned_blocks)
    
    # Write cleaned content to output file
    with open(output_path, 'w') as file:
        file.write(cleaned_content)

if __name__ == '__main__':
    clean_message_data(input_file_path, output_file_path)

print(f"Content removed, only message and sender remain, exported to: '{output_file_path}'.")
