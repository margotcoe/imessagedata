import re
import csv
from collections import defaultdict, Counter
import configparser

config = configparser.ConfigParser()
config.read('config.ini')
sender = config.get('settings', 'sender')
receiver = config.get('settings', 'receiver')

def parse_messages(file_path):
    """
    Parses messages from a file and returns a list of messages with their senders and text.
    """
    with open(file_path, 'r') as file:
        content = file.read()

    pattern = r'\{ Message \d+ Start \}\n(.*?)\n(?:Reactions:\n(.*?)\n)?(.*?)(?:\n\{ Message \d+ End \})'
    matches = re.findall(pattern, content, re.MULTILINE | re.DOTALL)

    messages = []
    for match in matches:
        sender, reactions, text = match
        sender = sender.strip()
        text = text.strip()
        if text:  

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
        
        words = re.findall(r'\b(?:[a-zA-Z]+(?:\'[a-zA-Z]+)?)+\b', text.lower())
        sender_word_counts[sender].update(words)
    
    return sender_word_counts

def prepare_data_for_csv(word_counts):
    """
    Prepares data for CSV export with columns: Word, Total, receiver, sender, Difference.
    """
    all_words = set()
    for counts in word_counts.values():
        all_words.update(counts.keys())
    
    csv_data = []
    total_counts = Counter()
    receiver_counts = word_counts.get(receiver, Counter())
    sender_counts = word_counts.get(sender, Counter())
    
    for word in all_words:
        receiver_count = receiver_counts.get(word, 0)
        sender_count = sender_counts.get(word, 0)
        total_count = receiver_count + sender_count
        difference = receiver_count - sender_count
        csv_data.append({
            'Word': word,
            'Total': total_count,
            receiver: receiver_count,
            sender: sender_count,
            'Difference': difference
        })
        total_counts[word] = total_count
    
    return csv_data, total_counts

def write_results_to_csv(csv_data, output_file):
    """
    Writes the word counts and total counts to a CSV file in the specified format.
    """
    fieldnames = ['Word', 'Total', receiver, sender, 'Difference']
    
    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        writer.writerows(csv_data)
        
        writer.writerow({})
        writer.writerow({'Word': 'Total', 'Total': sum(row['Total'] for row in csv_data), receiver: '', sender: '', 'Difference': ''})

def main():
    input_file = f'txt_files/{sender}_tagged_nodates.txt'
    output_file = f'outputs/frequency/{sender}_results.csv'
    
    messages = parse_messages(input_file)
    word_counts = count_words(messages)
    csv_data, total_counts = prepare_data_for_csv(word_counts)
    
    write_results_to_csv(csv_data, output_file)
    
    print(f"Frequency report exported to '{output_file}'.")

if __name__ == '__main__':
    main()
