import os
import sys
import urllib.request
import json
import csv
import time

client_id = "YOUR_CLIENT_ID"
client_secret = "YOUR_CLIENT_SECRET"
encText = urllib.parse.quote("검색할 단어")

# Số kết quả cần hiển thị (ví dụ 50)
display = 50
# Để lấy nhiều hơn 100 kết quả, bạn có thể sử dụng phân trang với start
start = 1

# API URL với các tham số display và start
url = f"https://openapi.naver.com/v1/search/blog?query={encText}&display={display}&start={start}"
request = urllib.request.Request(url)
request.add_header("X-Naver-Client-Id", client_id)
request.add_header("X-Naver-Client-Secret", client_secret)

try:
    response = urllib.request.urlopen(request)
    rescode = response.getcode()

    if rescode == 200:
        response_body = response.read()
        data = json.loads(response_body.decode('utf-8'))

        # Tạo tên file dựa trên thời gian thực
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        file_name = f"naver_blog_search_results_{timestamp}.csv"

        # Lưu vào file CSV
        with open(file_name, mode='w', newline='', encoding='utf-8') as csv_file:
            fieldnames = ['title', 'link', 'description', 'bloggername', 'bloggerlink', 'postdate']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

            writer.writeheader()
            for item in data['items']:
                writer.writerow({
                    'title': item['title'],
                    'link': item['link'],
                    'description': item['description'],
                    'bloggername': item['bloggername'],
                    'bloggerlink': item['bloggerlink'],
                    'postdate': item['postdate']
                })

        print(f"Kết quả đã được lưu vào {file_name}")
    else:
        print("Error Code:", rescode)

except urllib.error.URLError as e:
    print(f"Error: {e.reason}")
except Exception as e:
    print(f"An unexpected error occurred: {str(e)}")
