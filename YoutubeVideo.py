import time
import csv
from selenium import webdriver
from bs4 import BeautifulSoup

driver = webdriver.Chrome()

# 發出請求
driver.get('https://www.youtube.com/results?search_query=newjeans+MV')
time.sleep(2)

page_content = driver.page_source

# 網頁解析
soup = BeautifulSoup(page_content, 'html.parser')
titles = soup.select('a#video-title')
views = soup.select('#metadata-line > span:nth-child(3)')

elements = soup.select('.text-wrapper style-scope ytd-video-renderer')

# 列表標題和觀看次數，並排除不包含 "MV" 的標題
video_data = [
    {'video_title': title['title'], 'video_views': view.text.strip()} for title, view in zip(titles, views)
if 'MV' in title['title']
]

print(video_data)

for element in elements:
    titles = element.select('a#video-title')[1].text
    views = element.select('#metadata-line > span:nth-child(3)')[1].text
    print(titles, views) 


# CSV 檔案第一列標題
headers = ['video_title','video_views']

# 寫入檔案
with open('newjeans_MV_views.csv', 'w', newline='', encoding='utf-8') as output_file:
    dict_writer = csv.DictWriter(output_file, headers)
    dict_writer.writeheader()
    dict_writer.writerows(video_data)

# 讀取存成檔案的資料
with open('newjeans_MV_views.csv', 'r', newline='', encoding='utf-8') as input_file:
    rows = csv.reader(input_file)
    for row in rows:
        print(row)