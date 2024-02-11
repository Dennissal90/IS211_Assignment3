import csv
import re
from datetime import datetime
from collections import Counter

def process_weblog(file_name):
    with open(file_name, newline='') as csvfile:
        logreader = csv.reader(csvfile)
        image_hits = 0
        total_hits = 0
        browsers = Counter()
        hourly_hits = Counter()

        for row in logreader:
            path, datetime_str, user_agent, status, size = row
            total_hits += 1

            if re.search(r'\.(jpg|gif|png)$', path, re.IGNORECASE):
                image_hits += 1
            
            if 'Firefox' in user_agent:
                browsers['Firefox'] += 1
            elif 'Chrome' in user_agent:
                browsers['Chrome'] += 1
            elif 'MSIE' in user_agent or 'Trident' in user_agent:
                browsers['Internet Explorer'] += 1
            elif 'Safari' in user_agent and 'Chrome' not in user_agent:
                browsers['Safari'] += 1
            
            hour = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S").hour
            hourly_hits[hour] += 1

    image_hit_percentage = (image_hits / total_hits) * 100 if total_hits else 0

    most_popular_browser = browsers.most_common(1)[0] if browsers else ('None', 0)

    sorted_hourly_hits = sorted(hourly_hits.items())

    return image_hit_percentage, most_popular_browser, sorted_hourly_hits

file_name = 'weblog.csv' # Assuming the CSV file is in the same directory as this script
image_hit_percentage, most_popular_browser, sorted_hourly_hits = process_weblog(file_name)

print(f"Image Hit Percentage: {image_hit_percentage}%")
print(f"Most Popular Browser: {most_popular_browser[0]} with {most_popular_browser[1]} hits")
print("Hits per Hour:")
for hour, hits in sorted_hourly_hits:
    print(f"Hour {hour}: {hits} hits")
