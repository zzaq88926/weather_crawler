import requests
import json
import urllib3

# 禁用安全請求警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def fetch_cwa_data():
    url = "https://opendata.cwa.gov.tw/fileapi/v1/opendataapi/F-A0012-001?Authorization=CWA-D2277D90-455D-46B3-BBE5-29C7C012EBA6&downloadType=WEB&format=JSON"
    
    try:
        print("正在請求資料...")
        # verify=False 忽略 SSL 憑證驗證
        response = requests.get(url, verify=False)
        
        # 檢查請求是否成功
        if response.status_code == 200:
            print("請求成功！正在解析 JSON...")
            data = response.json()
            
            # 將資料寫入檔案
            output_file = "data.json"
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
                
            print(f"資料已成功儲存至 {output_file}")
        else:
            print(f"請求失敗，狀態碼: {response.status_code}")
            
    except Exception as e:
        print(f"發生錯誤: {e}")

if __name__ == "__main__":
    fetch_cwa_data()
