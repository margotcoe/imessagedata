import re
from datetime import datetime, timedelta
from collections import defaultdict
import statistics

input_file_path = 'txt_files/elly_tagged.txt'
output_file_path = 'outputs/statistics/elly_message_statistics.md'

date_pattern = r'(\b[A-Za-z]{3} \d{2}, \d{4}\b)'
message_pattern = r'\{ Message \d+ Start \}(.*?)\{ Message \d+ End \}'
read_by_pattern = r'\(Read by (Margot|Elly) after (.*?)(?:\)|$)'

def extract_messages_dates_read_times(text):
    messages = re.findall(message_pattern, text, re.DOTALL)
    dates = [re.search(date_pattern, msg).group(0) for msg in messages if re.search(date_pattern, msg)]
    read_times = re.findall(read_by_pattern, text)
    return messages, dates, read_times

def parse_duration(duration_str):
    time_units = {'hour': 3600, 'minute': 60, 'second': 1}
    total_seconds = 0
    matches = re.findall(r'(\d+)\s*(hour|minute|second)s?', duration_str)
    for amount, unit in matches:
        total_seconds += int(amount) * time_units[unit]
    return total_seconds

with open(input_file_path, 'r') as file:
    data = file.read()

messages, dates, read_times = extract_messages_dates_read_times(data)

sender_count = defaultdict(int)
yearly_message_count = defaultdict(int)
yearly_sender_count = defaultdict(lambda: defaultdict(int))
read_times_by_sender = defaultdict(list)
read_times_by_year = defaultdict(lambda: defaultdict(list))
days_with_messages = defaultdict(set)
all_dates = set()
attachment_count = defaultdict(int)

total_messages = len(messages)
date_of_first_message = min(dates, key=lambda d: datetime.strptime(d, '%b %d, %Y'))
date_of_last_message = max(dates, key=lambda d: datetime.strptime(d, '%b %d, %Y'))

for message, date in zip(messages, dates):
    year = datetime.strptime(date, '%b %d, %Y').year
    if year == 2021:
        continue

    sender_match = re.search(r'(Margot|Elly)', message)
    if sender_match:
        sender = sender_match.group(1)
        sender_count[sender] += 1
        yearly_message_count[year] += 1
        yearly_sender_count[sender][year] += 1
        days_with_messages[year].add(date)
        all_dates.add(date)

        if "attachments/" in message:
            attachment_count[sender] += 1

        read_time_matches = re.findall(read_by_pattern, message)
        for read_sender, read_duration in read_time_matches:
            if read_sender:
                read_seconds = parse_duration(read_duration)
                read_times_by_sender[read_sender].append(read_seconds)
                read_times_by_year[read_sender][year].append(read_seconds)

def average_read_times(read_times):
    return round(statistics.mean(read_times), 2) if read_times else 0

def average_read_times_by_year(read_times_by_year):
    avg_by_year = {}
    for year, times in read_times_by_year.items():
        avg_by_year[year] = round(statistics.mean(times), 2) if times else 0
    return avg_by_year

def average_read_times_by_threshold(read_times):
    under_hour = [t for t in read_times if t < 3600]
    over_hour = [t for t in read_times if t >= 3600]
    return (
        round(statistics.mean(under_hour), 2) if under_hour else 0,
        round(statistics.mean(over_hour), 2) if over_hour else 0
    )

def days_in_year(year):
    return (datetime(year + 1, 1, 1) - datetime(year, 1, 1)).days

def percentage_days_with_messages(total_days, days_with_msgs):
    return round((days_with_msgs / total_days) * 100, 2) if total_days > 0 else 0

def calculate_days_missed(dates, year):
    start_date = datetime(year, 1, 1)
    end_date = datetime(year + 1, 1, 1)
    all_dates_in_year = set()
    
    for single_date in (start_date + timedelta(n) for n in range((end_date - start_date).days)):
        all_dates_in_year.add(single_date.strftime('%b %d, %Y'))
    
    missed_dates = all_dates_in_year - set(dates)
    return sorted(missed_dates)

def percentage_days_2024_so_far(total_days, days_with_msgs):
    today = datetime.now()
    total_days_2024 = (today - datetime(2024, 1, 1)).days + 1
    return round((days_with_msgs / total_days_2024) * 100, 2) if total_days_2024 > 0 else 0

with open(output_file_path, 'w') as file:
    file.write('# Message Statistics\n\n')
    file.write(f'**Total Messages:** {total_messages}\n')
    file.write(f'**Date of First Message:** {date_of_first_message}\n')
    file.write(f'**Date of Last Message:** {date_of_last_message}\n\n')

    file.write('## Total Messages by Sender\n')
    for sender, count in sender_count.items():
        file.write(f'- {sender}: {count}\n')
    
    file.write('\n## Breakdown of Messages by Year\n')
    for year, count in sorted(yearly_message_count.items()):
        file.write(f'- {year}: {count}\n')

    file.write('\n## Breakdown of Messages by Sender and Year\n')
    for sender, years in sorted(yearly_sender_count.items()):
        file.write(f'### {sender}\n')
        for year, count in sorted(years.items()):
            file.write(f'- {year}: {count}\n')

    file.write('\n## Average Read Times\n')
    for sender in ['Margot', 'Elly']:
        all_times = read_times_by_sender[sender]
        avg_total = average_read_times(all_times)
        avg_by_year = average_read_times_by_year(read_times_by_year[sender])
        avg_under_hour, avg_over_hour = average_read_times_by_threshold(all_times)
        
        file.write(f'### {sender}\n')
        file.write(f'- **Average Total Read Time:** {avg_total} seconds\n')
        file.write(f'- **Average Read Time by Year:**\n')
        for year, avg in sorted(avg_by_year.items()):
            file.write(f'  - {year}: {avg} seconds\n')
        file.write(f'- **Average Read Time Under 1 Hour:** {avg_under_hour} seconds\n')
        file.write(f'- **Average Read Time Over 1 Hour:** {avg_over_hour} seconds\n')

    file.write('\n## Days with Messages\n')
    total_days_all = (datetime.now() - datetime.strptime(date_of_first_message, '%b %d, %Y')).days
    file.write(f'- **Total Days Covered:** {total_days_all}\n')

    for year in sorted(yearly_message_count.keys()):
        total_days = days_in_year(year)
        days_with_msgs = len(days_with_messages[year])
        percentage = percentage_days_with_messages(total_days, days_with_msgs)
        file.write(f'### {year}\n')
        file.write(f'- **Total Days with Messages:** {days_with_msgs}\n')
        file.write(f'- **Total Days in Year:** {total_days}\n')
        file.write(f'- **Percentage of Days with Messages:** {percentage}%\n')
        
        if year == 2023:
            missed_days = calculate_days_missed(dates, year)
            file.write(f'- **Days Missed in {year}:**\n')
            for missed_day in missed_days:
                file.write(f'  - {missed_day}\n')

    total_days_2024 = days_in_year(2024)
    days_with_msgs_2024 = len(days_with_messages.get(2024, set()))
    percentage_2024 = percentage_days_2024_so_far(total_days_2024, days_with_msgs_2024)
    file.write(f'\n## 2024 Statistics\n')
    file.write(f'- **Total Days with Messages (2024 so far):** {days_with_msgs_2024}\n')
    file.write(f'- **Total Days in 2024:** {total_days_2024}\n')
    file.write(f'- **Percentage of Days with Messages (2024 so far):** {percentage_2024}%\n')

    file.write('\n## Attachments Sent\n')
    for sender, count in attachment_count.items():
        file.write(f'- {sender}: {count}\n')

print(f"Statistics exported to '{output_file_path}'.")
