# 🌊 台灣近海海象觀測地圖 (Taiwan Sea Weather Map)

這是一個使用 Streamlit 建構的互動式網頁應用程式，可以即時爬取中央氣象局 (CWA) 的海面天氣預報資料 (F-A0012-001)，並在地圖上視覺化顯示各地點的風速、浪高及天氣狀況。

## ✨ 功能特色

- **即時爬蟲**: 自動從 CWA Open API 獲取最新資料。
- **互動地圖**: 使用 Plotly Mapbox 顯示全台近海觀測點，滑鼠懸停可查看詳細數據。
- **資料庫整合**: 使用 SQLite 儲存歷史資料，避免重複請求 API。
- **自動更新**: 網頁開啟時自動檢查並更新資料。

## 🛠️ 安裝與執行

### 1. 安裝套件

請確保您已安裝 Python 3.8+，然後執行以下指令安裝必要套件：

```bash
pip install -r requirements.txt
```

### 2. 執行應用程式

在終端機執行以下指令啟動 Streamlit：

```bash
streamlit run streamlit_app.py
```

啟動後，瀏覽器會自動開啟應用程式 (預設網址: `https://weathercrawler-fhjesnaj7t8zhzvyu2pcbq.streamlit.app/`)。

## 📂 專案結構

- `streamlit_app.py`: 主程式，負責 UI 顯示與地圖繪製。
- `weather_crawler.py`: 爬蟲模組，負責抓取 API 資料、解析並存入資料庫。
- `data.db`: SQLite 資料庫檔案 (自動產生)。
- `requirements.txt`: 專案依賴套件列表。

## 🚀 部署至 Streamlit Cloud

本專案已準備好部署至 Streamlit Cloud。

1.  將本專案上傳至 GitHub Repository。
2.  前往 [Streamlit Cloud](https://streamlit.io/cloud)。
3.  點擊 "New app"。
4.  選擇您的 Repository、Branch (通常是 `main`)，並將 "Main file path" 設為 `streamlit_app.py`。
5.  點擊 "Deploy"！

Streamlit Cloud 會自動讀取 `requirements.txt` 並安裝所需套件。

## ⚠️ 注意事項

- 本專案使用 CWA 開放資料 API，請遵守相關使用規範。
- 為了避免 SSL 憑證錯誤，爬蟲腳本中已禁用 SSL 驗證 (`verify=False`)。
