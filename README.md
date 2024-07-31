針對 JavaScript 網頁前端程式生成的網頁內容(非伺服器渲染網頁) 使用 selenium 這個瀏覽器模擬工具進行爬蟲專案實作

`Step 1 設定目標`
我規劃抓取 Youtube 搜尋 "Newjeans MV" 會出現的 MV 標題和觀看人次
![](https://static.coderbridge.com/img/minnieting6675/2ed293d39f0a44fc9781cdb55c79742f.jpg)

-----

`Step 2 觀察網頁`
點選右鍵  - 檢視網頁原始碼 - 好像也有 HTML 元素 但是查關鍵字會找出一些看不懂的東西很亂==
![](https://static.coderbridge.com/img/minnieting6675/275d6b19520e4bcbaa3e72db75e63e80.jpg)

選取元素 - 點選右鍵 - 檢視 - 找到對應元素 - 標題
![](https://static.coderbridge.com/img/minnieting6675/c1efa058ef84409bbd4b3a9e2dfc1d96.png)

另一個元素是 觀看人次
![](https://static.coderbridge.com/img/minnieting6675/68a338e3cb9646148a2e2c24c6bfd2df.png)
-----

`Step 3 發出請求`
```
import time
import csv
from selenium import webdriver
from bs4 import BeautifulSoup

driver = webdriver.Chrome()

#發出請求
driver.get('https://www.youtube.com/results?search_query=newjeans+MV')
# 等待 2 秒等網頁資料都載入後再抓取
time.sleep(2)
# 取出網頁整頁內容
page_content = driver.page_source
```

-----

`Step 4 解析內容`
```
# 將 HTML 內容轉換成 BeautifulSoup 物件，html.parser 為使用的解析器
soup = BeautifulSoup(page_content, 'html.parser')
# 透過 select 使用 CSS 選擇器 選取我們要選的 html 內容
titles = soup.select('a#video-title')
views = soup.select('#metadata-line > span:nth-child(3)')


# 使用列表推導式來組合標題和觀看次數，並排除不包含 "MV" 的標題
video_data = [
    {'video_title': title['title'], 'video_views': view.text.strip()} for title, view in zip(titles, views)
if 'MV' in title['title']
]

print(video_data)
```
-----

`Step 5 儲存資料`
```
# CSV 檔案第一列標題
headers = ['video_title','video_views']

# 寫入檔案模式
with open('newjeans_MV_views.csv', 'w', newline='', encoding='utf-8') as output_file:
    dict_writer = csv.DictWriter(output_file, headers)
    dict_writer.writeheader()
    dict_writer.writerows(video_data)

# 開啟讀取 read (r) 檔案模式，透過 csv 模組將已經存成檔案的資料讀入
with open('newjeans_MV_views.csv', 'r', newline='', encoding='utf-8') as input_file:
    rows = csv.reader(input_file)
    # 以迴圈輸出每一列，每一列是一個 list
    for row in rows:
        print(row)
```

-----
擷取成果
![](https://static.coderbridge.com/img/minnieting6675/56faf920a8fe474fac169fe98d7d7ab0.jpg)
