import os
import urllib.request
import json
import csv
import time
import torch
from transformers import CLIPProcessor, CLIPModel

client_id = "fKOPWU2yFkCyiBPRbBiU"
client_secret = "Whlf2LfCSw"
encText = urllib.parse.quote("vietnam")

# Số kết quả cần hiển thị
display = 50
start = 1
url = f"https://openapi.naver.com/v1/search/blog?query={encText}&display={display}&start={start}"
request = urllib.request.Request(url)
request.add_header("X-Naver-Client-Id", client_id)
request.add_header("X-Naver-Client-Secret", client_secret)

# Tải CLIP model và processor
model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

try:
    response = urllib.request.urlopen(request)
    rescode = response.getcode()

    if rescode == 200:
        response_body = response.read()
        data = json.loads(response_body.decode('utf-8'))

        # Tạo tên file
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        file_name = f"naver_blog_search_results_{timestamp}.csv"

        # Lưu vào file CSV với URL ảnh
        with open(file_name, mode='w', newline='', encoding='utf-8') as csv_file:
            fieldnames = ['title', 'link', 'description', 'bloggername', 'bloggerlink', 'postdate', 'image_url', 'clip_score']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()

            for item in data['items']:
                title = item['title']
                description = item['description']
                
                # Dùng CLIP để tính điểm phù hợp giữa tiêu đề và mô tả
                inputs = processor(text=[title], images=None, return_tensors="pt", padding=True)
                outputs = model.get_text_features(**inputs)
                clip_score = outputs.norm().item()  # Điểm phù hợp

                # URL ảnh (giả sử API cung cấp trong dữ liệu)
                image_url = item.get('image_url', '')  # Nếu không có ảnh, sẽ là chuỗi trống

                # Ghi dữ liệu vào file
                writer.writerow({
                    'title': title,
                    'link': item['link'],
                    'description': description,
                    'bloggername': item['bloggername'],
                    'bloggerlink': item['bloggerlink'],
                    'postdate': item['postdate'],
                    'image_url': image_url,
                    'clip_score': clip_score
                })

        print(f"Kết quả đã được lưu vào {file_name}")
    else:
        print("Error Code:", rescode)

except urllib.error.URLError as e:
    print(f"Error: {e.reason}")
except Exception as e:
    print(f"An unexpected error occurred: {str(e)}")
