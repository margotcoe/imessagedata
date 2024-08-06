import re

# Define the file paths
input_file_path = 'txt_files/elly_pretag.txt'  # Replace with your actual input file path
output_file_path = 'txt_files/elly_tagged.txt'

# Define the pattern for message dates
date_pattern = r'\b[A-Za-z]{3} \d{2}, \d{4}\b'

# Function to split the text into messages based on the date pattern
def split_messages(text):
    # Find all date matches
    dates = [match.start() for match in re.finditer(date_pattern, text)]
    
    # Split text into messages based on the dates
    messages = []
    for i in range(len(dates)):
        start = dates[i]
        end = dates[i + 1] if i + 1 < len(dates) else len(text)
        messages.append(text[start:end].strip())
    
    return messages

# Read the contents of the input file
with open(input_file_path, 'r') as file:
    data = file.read()

# Split the data into messages
messages = split_messages(data)

# Write all messages to the output file with { } indicating start and end
with open(output_file_path, 'w') as file:
    for i, message in enumerate(messages, start=1):
        file.write(f"{{ Message {i} Start }}\n")
        file.write(message + '\n')
        file.write(f"{{ Message {i} End }}\n\n")

print(f"Tagged messages exported to '{output_file_path}'.")
