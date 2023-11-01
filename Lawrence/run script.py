import pandas as pd
import subprocess
import time
import os

spider_names = ['everout', 'songkick', 'ticketmaster', 'do206', 'eventbrite', 'bandsintown', 'stubhub', 'viagogo', 'seatgeek']

for i, name in enumerate(spider_names):
    print(f'Enter {i+1} to scrape {name}.com')
    
time.sleep(1)

spider_num = int(input('Enter the number of website you want to scrape: '))
spider_name = spider_names[spider_num-1]
start_date = input('Enter the start date of the shows (YYYY-MM-DD): ')
end_date = input('Enter the end date of the shows (YYYY-MM-DD): ')
output_file = input('Enter the path of the output file (path/to/filename.csv): ')
output_json = output_file.replace('csv', 'json')

# replce empty with default values
start_date = start_date if start_date else None
end_date = end_date if end_date else None

command = ['scrapy', 'crawl', spider_name, '-o', output_json]

if start_date is not None:
    command.extend(['-a', f's_date={start_date}'])
if end_date is not None:
    command.extend(['-a', f'e_date={end_date}'])

subprocess.run(command)
try:
    data = pd.read_json(output_json)
except ValueError:
    data = pd.DataFrame(columns='event_title;venue_title;address;zip_code;city;state;phone_number;date;time;lowest_price;highest_price;source_url'.split(';'))
data.to_csv(output_file, index=False, sep=';')
# Step 4: Delete the JSON file
os.remove(output_json)
input('press Enter to exit..')