import re
import csv
from collections import defaultdict, Counter

def parse_messages(file_path):
    """
    Parses messages from a file and returns a list of messages with their senders and text.
    """
    with open(file_path, 'r') as file:
        content = file.read()

    # Regex pattern to match messages with start and end markers
    pattern = r'\{ Message \d+ Start \}\n(.*?)\n(?:Reactions:\n(.*?)\n)?(.*?)(?:\n\{ Message \d+ End \})'
    matches = re.findall(pattern, content, re.MULTILINE | re.DOTALL)

    messages = []
    for match in matches:
        sender, reactions, text = match
        sender = sender.strip()
        text = text.strip()
        if text:  # Only add messages with non-empty text
            # Handling case where reactions or attachments might be present
            if reactions:
                text += f" Reactions: {reactions.strip()}"
            messages.append((sender, text))

    return messages

def count_words(messages):
    """
    Counts the occurrences of each word in the message text, grouped by sender.
    """
    sender_word_counts = defaultdict(Counter)
    
    for sender, text in messages:
        # Extract words and ignore numbers, handle contractions and possessives
        words = re.findall(r'\b(?:[a-zA-Z]+(?:\'[a-zA-Z]+)?)+\b', text.lower())
        sender_word_counts[sender].update(words)
    
    return sender_word_counts

def prepare_data_for_csv(word_counts):
    """
    Prepares data for CSV export with columns: Word, Total, Margot, Elly, Difference.
    """
    all_words = set()
    for counts in word_counts.values():
        all_words.update(counts.keys())
    
    # Create a dictionary with word counts for Margot and Elly, and calculate differences
    csv_data = []
    total_counts = Counter()
    margot_counts = word_counts.get('Margot', Counter())
    elly_counts = word_counts.get('Elly', Counter())
    
    for word in all_words:
        margot_count = margot_counts.get(word, 0)
        elly_count = elly_counts.get(word, 0)
        total_count = margot_count + elly_count
        difference = margot_count - elly_count
        csv_data.append({
            'Word': word,
            'Total': total_count,
            'Margot': margot_count,
            'Elly': elly_count,
            'Difference': difference
        })
        total_counts[word] = total_count
    
    return csv_data, total_counts

def write_results_to_csv(csv_data, output_file):
    """
    Writes the word counts and total counts to a CSV file in the specified format.
    """
    with open(output_file, 'w', newline='') as csvfile:
        fieldnames = ['Word', 'Total', 'Margot', 'Elly', 'Difference']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        writer.writerows(csv_data)
        
        # Adding total counts at the end
        writer.writerow({})
        writer.writerow({'Word': 'Total', 'Total': sum(row['Total'] for row in csv_data), 'Margot': '', 'Elly': '', 'Difference': ''})

def main():
    input_file = 'txt_files/elly_tagged_nodates.txt'
    output_file = 'outputs/frequency/elly_results.csv'
    
    messages = parse_messages(input_file)
    word_counts = count_words(messages)
    csv_data, total_counts = prepare_data_for_csv(word_counts)
    
    write_results_to_csv(csv_data, output_file)
    
    print(f"Frequency report exported to '{output_file}'.")

if __name__ == '__main__':
    main()
