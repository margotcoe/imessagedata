import re
import configparser

# Load the configuration file
config = configparser.ConfigParser()
config.read('config.ini')

# Retrieve variables from the config file
sender = config.get('settings', 'sender')
receiver = config.get('settings', 'receiver')

# Define the file paths
input_file = f'txt_files/{sender}_tagged.txt'
output_file = f'txt_files/{sender}_tagged_nodates.txt'

def clean_message_file(input_file, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        lines = infile.readlines()
        skip_next_line = False

        for line in lines:
            if line.startswith('{ Message'):
                outfile.write(line)
                skip_next_line = True
            elif skip_next_line:
                skip_next_line = False
                
                if line.strip().startswith(receiver) or line.strip().startswith(sender):
                    outfile.write(line)
            else:
                outfile.write(line)

# Run the function
clean_message_file(input_file, output_file)

print(f"File exported to '{output_file}'.")
