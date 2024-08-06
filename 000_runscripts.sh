#!/bin/bash

# Navigate to the directory containing the scripts
cd /Users/Margot/Documents/iMessageDataExtractor || exit

# Define a function to run each script and check if it was successful
run_script() {
    local script_name=$1
    python3 "$script_name"
    if [ $? -eq 0 ]; then
        echo "$script_name ran successfully."
    else
        echo "Error: $script_name failed to run."
        exit 1
    fi
}

# Run the Python scripts in order
run_script "00_cleaner.py"
run_script "01_add_numbers.py"
run_script "02_remove_dates_times.py"
run_script "03_extract_dates.py"
run_script "10_generate_requited.py"
run_script "11_generate_requited_last_pass.py"
run_script "20_generate_statistics.py"
run_script "30_frequency_generator.py"
