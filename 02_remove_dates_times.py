import re

# Path to the input file
input_file = 'txt_files/elly_tagged.txt'
# Path to the output file
output_file = 'txt_files/elly_tagged_nodates.txt'

def clean_message_file(input_file, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        lines = infile.readlines()
        skip_next_line = False
        
        for line in lines:
            if line.startswith('{ Message'):
                outfile.write(line)  # Write the start of the message
                skip_next_line = True  # Skip the next line (date and read info)
            elif skip_next_line:
                skip_next_line = False  # Skip this line and continue
                # We want to keep lines that start with "Margot" or "Elly"
                if line.strip().startswith('Margot') or line.strip().startswith('Elly'):
                    outfile.write(line)
            else:
                outfile.write(line)  # Write other lines (message content)

# Run the function
clean_message_file(input_file, output_file)

print(f"File exported to '{output_file}'.")
