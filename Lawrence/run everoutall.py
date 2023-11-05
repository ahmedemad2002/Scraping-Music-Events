import pandas as pd
import subprocess
import time
import os
import json

choices = {'Top Picks': 'staff-pick=true',
 'All Live Music': 'category=live-music',
 'Major Artist Tours': 'category=music-major-artist-tour',
 'DJ & Dance Nights': 'category=music-dj',
 'Concerts': 'category=music-concert',
 'Jam Sessions': 'category=music-music-session',
 'Classical/Opera': 'category=music-classical-opera',
 'Jazz': 'category=music-jazz',
 'Pop': 'category=live-music-pop',
 'Rock': 'category=live-music-rock',
 'Funk/Reggae': 'category=music-funk-reggae',
 'Hip-Hop/Rap': 'category=music-hip-hop-rap',
 'Country/Folk/Bluegrass': 'category=live-music-country-folk-bluegrass',
 'Metal': 'category=music-metal',
 'EDM/House': 'category=live-music-edm-house',
 'Soul/R&B': 'category=music-soul-r-b',
 'World/Latin': 'category=music-world-latin',
 'Experimental/Ambient': 'category=live-music-experimental-ambient',
 'All Performance': 'category=performance&category=comedy',
 'Theater': 'category=theater',
 'Dance': 'category=dance',
 'Comedy': 'category=comedy',
 'Musical Theater': 'category=performance-musical-theater',
 'Drag': 'category=performance-drag',
 'Podcasts & Radio': 'category=performance-podcasts-radio',
 'Opera': 'category=performance-opera',
 'Cabaret & Burlesque': 'category=performance-cabaret-burlesque',
 'Circus & Acrobatics': 'category=performance-circus-acrobatics',
 'Performance Art': 'category=performance-performance-art',
 'Variety': 'category=performance-variety',
 'Visual Art': 'category=visual-art',
 'All Other Events': 'category=shopping&category=parties-nightlife&category=geek-gaming&category=festivals&category=community&category=classes-workshops&category=sports-recreation&category=weed&category=queer&category=food-drink&category=readings-talks&category=film&category=activism-social-justice&category=bipoc',
 'Food & Drink': 'category=food-drink',
 'Readings & Talks': 'category=readings-talks',
 'Film': 'category=film',
 'Festivals': 'category=festivals',
 'Parties & Nightlife': 'category=parties-nightlife',
 'Community': 'end-date=2023-11-10',
 'Activism & Social Justice': 'category=activism-social-justice',
 'BIPOC-Focused Events': 'category=bipoc',
 'Classes & Workshops': 'category=classes-workshops',
 'Geek & Gaming': 'category=geek-gaming',
 'Weed': 'category=weed',
 'Shopping': 'category=shopping',
 'Queer': 'category=queer',
 'Sports & Recreation': 'category=sports-recreation'}

print("Enter numbers to choose selected categories")
print(json.dumps(dict(enumerate(choices.keys())), indent=4))
time.sleep(1)
selection = input().split()
selection = set(int(s) for s in selection)

cat_str = ''
for s in selection:
    cat_str = cat_str + '&' + list(choices.values())[s]

start_date = input('Enter the start date of the shows (YYYY-MM-DD): ')
end_date = input('Enter the end date of the shows (YYYY-MM-DD): ')
output_file = input('Enter the path of the output file (path/to/filename.csv): ')
output_json = output_file.replace('csv', 'json')

# replce empty with default values
start_date = start_date if start_date else None
end_date = end_date if end_date else None

command = ['scrapy', 'crawl', 'everoutall', '-o', output_json]
if start_date is not None:
    command.extend(['-a', f's_date={start_date}'])
if end_date is not None:
    command.extend(['-a', f'e_date={end_date}'])
command.extend(['-a', f'categories_str={cat_str}'])

subprocess.run(command)
try:
    data = pd.read_json(output_json)
except ValueError:
    data = pd.DataFrame(columns='event_title;event_category;in_person;age_restriction;event_freq;venue_title;address;zip_code;city;state;phone_number;date;time;lowest_price;highest_price;description;source_url'.split(';'))
data.to_csv(output_file, index=False, sep=';')
# Step 4: Delete the JSON file
os.remove(output_json)
input('press Enter to exit..')
