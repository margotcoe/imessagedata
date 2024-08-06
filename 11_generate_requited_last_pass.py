import csv
from datetime import datetime, timedelta
from collections import defaultdict

csv_file_path = 'outputs/requited/elly_dates_and_senders.csv'
output_file_path = 'outputs/requited/elly_requited_final.txt'

def read_dates_and_senders(file_path):
    dates = []
    senders = {'Margot': set(), 'Elly': set()}

    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            date = datetime.strptime(row['Date'], '%Y-%m-%d').date()
            sender = row['Sender']
            if sender in senders:
                senders[sender].add(date)
                dates.append(date)
    
    return dates, senders

def analyze_dates(dates, senders):
    if not dates:
        return defaultdict(lambda: defaultdict(set)), defaultdict(lambda: defaultdict(set))

    # Define the range to consider
    start_date = datetime(2023, 1, 1).date()
    end_date = datetime(2024, 12, 31).date()

    # Filter dates to consider
    dates = [date for date in dates if start_date <= date <= end_date]
    all_dates_by_year = defaultdict(set)
    
    for date in (start_date + timedelta(days=i) for i in range((end_date - start_date).days + 1)):
        if start_date <= date <= end_date:
            all_dates_by_year[date.year].add(date)
    
    missing_dates_senders = defaultdict(lambda: defaultdict(set))
    
    for sender, sender_dates in senders.items():
        sender_dates = [date for date in sender_dates if start_date <= date <= end_date]
        sender_dates_by_year = defaultdict(set)
        
        for date in sender_dates:
            sender_dates_by_year[date.year].add(date)
        
        for year, all_dates in all_dates_by_year.items():
            if year in [2023, 2024]:
                missing_dates = all_dates - sender_dates_by_year[year]
                missing_dates_senders[sender][year] = missing_dates

    return missing_dates_senders

def write_results(missing_dates_senders):
    with open(output_file_path, 'w') as file:
        file.write('Missing Dates by Sender for 2023 and 2024:\n')
        for sender in ['Margot', 'Elly']:
            file.write(f'\n{sender}:\n')
            for year in [2023, 2024]:
                if year in missing_dates_senders[sender]:
                    file.write(f'  Year {year}:\n')
                    for date in sorted(missing_dates_senders[sender][year]):
                        file.write(f'    {date.strftime("%Y-%m-%d")}\n')

if __name__ == '__main__':
    dates, senders = read_dates_and_senders(csv_file_path)
    missing_dates_senders = analyze_dates(dates, senders)
    write_results(missing_dates_senders)
    print(f'Results have been written to {output_file_path}')
