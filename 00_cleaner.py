import re
import os

# Define the input file path
input_file = 'input/+12064022950.txt'

# Define the output file path (current working directory)
output_file = 'txt_files/elly_pretag.txt'

# Define the text replacements
replacements = {
    r'\+12064022950': 'Elly',  # Use raw string for the phone number to escape the '+'
    r'Read by them': 'Read by Elly',
    r'Read by you': 'Read by Margot'
    
}

# Read the contents of the input file
with open(input_file, 'r') as file:
    data = file.read()

# Perform the replacements
for pattern, replacement_text in replacements.items():
    data = re.sub(pattern, replacement_text, data)

# Write the modified content to the output file in the current working directory
with open(output_file, 'w') as file:
    file.write(data)

print(f"Exported to '{output_file}'")
