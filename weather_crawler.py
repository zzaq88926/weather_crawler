import json
import sqlite3
import requests
import urllib3

# 禁用安全請求警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# 檔案路徑
json_file_path = "data.json"
db_file_path = "data.db"
# API URL (F-A0012-001)
API_URL = "https://opendata.cwa.gov.tw/fileapi/v1/opendataapi/F-A0012-001?Authorization=CWA-D2277D90-455D-46B3-BBE5-29C7C012EBA6&downloadType=WEB&format=JSON"

# 🌏 台灣常見地點經緯度對照表 (人工定義，確保地圖有點)
LOCATION_COORDS = {
    "釣魚台海面": (25.8, 123.5), "彭佳嶼基隆海面": (25.4, 122.0), "宜蘭蘇澳沿海": (24.6, 121.9),
    "新竹鹿港沿海": (24.8, 120.8), "鹿港東石沿海": (24.0, 120.2), "東石安平沿海": (23.2, 120.0),
    "安平高雄沿海": (22.8, 120.1), "高雄枋寮沿海": (22.4, 120.4), "枋寮恆春沿海": (22.1, 120.6),
    "鵝鑾鼻沿海": (21.8, 120.9), "成功臺東沿海": (22.9, 121.3), "臺東大武沿海": (22.5, 121.1),
    "綠島海面": (22.6, 121.5), "蘭嶼海面": (22.0, 121.6), "花蓮沿海": (24.0, 121.7),
    "金門海面": (24.4, 118.3), "馬祖海面": (26.1, 119.9), "澎湖海面": (23.5, 119.5),
    "沙塘鳩": (25.2, 121.5), "基隆": (25.13, 121.74), "新竹": (24.84, 120.94),
    "臺中": (24.15, 120.68), "高雄": (22.62, 120.31), "花蓮": (23.99, 121.60)
}

def fetch_and_save_json():
    """從 API 下載最新資料並存檔"""
    try:
        response = requests.get(API_URL, verify=False)
        if response.status_code == 200:
            data = response.json()
            with open(json_file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            return data
    except Exception as e:
        print(f"下載失敗: {e}")
    return None

def parse_weather_data(data):
    """解析資料並加入經緯度"""
    parsed_records = []
    try:
        location_data = data['cwaopendata']['dataset']['location']
        for location in location_data:
            loc_name = location['locationName']
            
            # 取得經緯度 (如果在對照表裡就用，沒有就設為 None)
            lat, lon = LOCATION_COORDS.get(loc_name, (None, None))
            
            # 如果找不到座標，為了地圖顯示，我們可以試著模糊匹配 (Optional)
            if lat is None:
                # 簡單處理：如果找不到座標，暫時跳過，避免地圖報錯，或是給一個預設值
                continue 

            weather_element = location['weatherElement']
            
            # Wx, WindSpeed, WaveHeight
            wx = next((e['time'][0]['parameter']['parameterName'] for e in weather_element if e['elementName'] == 'Wx'), 'N/A')
            wind = next((e['time'][0]['parameter']['parameterName'] for e in weather_element if e['elementName'] == 'WindSpeed'), 'N/A')
            wave = next((e['time'][0]['parameter']['parameterName'] for e in weather_element if e['elementName'] == 'WaveHeight'), 'N/A')
            
            parsed_records.append((loc_name, wx, wind, wave, lat, lon))
            
    except Exception as e:
        print(f"解析錯誤: {e}")
        return []
    return parsed_records

def create_and_insert_db(records):
    """建立包含經緯度的資料庫"""
    conn = sqlite3.connect(db_file_path)
    cursor = conn.cursor()
    
    # 3️⃣ 重建資料表 (確保欄位正確)
    cursor.execute("DROP TABLE IF EXISTS weather;")
    
    cursor.execute("""
        CREATE TABLE weather ( 
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            location TEXT, 
            description TEXT,
            wind_speed TEXT,
            wave_height TEXT,
            lat REAL,
            lon REAL
        );
    """)
    
    # 4️⃣ 存入資料 (含座標)
    cursor.executemany("INSERT INTO weather (location, description, wind_speed, wave_height, lat, lon) VALUES (?, ?, ?, ?, ?, ?)", records)
    
    conn.commit()
    conn.close()
    print(f"成功存入 {len(records)} 筆含座標的資料")

if __name__ == "__main__":
    print("--- 執行爬蟲與座標定位 ---")
    data = fetch_and_save_json()
    if data:
        records = parse_weather_data(data)
        if records:
            create_and_insert_db(records)
        else:
            print("解析後沒有資料 (可能是地點名稱與座標表不符)")