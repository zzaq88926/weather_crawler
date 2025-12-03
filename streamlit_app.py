import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
import time
import weather_crawler  # Import the crawler module

# 資料庫路徑 (需與 weather_crawler.py 一致)
DB_FILE = "data.db"

# --- 核心功能：爬蟲並更新資料庫 ---
def run_weather_crawler_task():
    """
    呼叫 weather_crawler 模組執行爬蟲
    """
    try:
        # 1. 下載
        data = weather_crawler.fetch_and_save_json()
        if not data:
            return False, "API 請求失敗或無法下載資料"
        
        # 2. 解析
        records = weather_crawler.parse_weather_data(data)
        if not records:
            return False, "解析後沒有資料 (可能是地點名稱與座標表不符)"
            
        # 3. 存入 DB
        weather_crawler.create_and_insert_db(records)
        
        return True, f"更新成功！共取得 {len(records)} 筆資料 (時間: {time.strftime('%H:%M:%S')})"
        
    except Exception as e:
        return False, f"發生系統錯誤: {e}"

# --- 讀取資料 ---
def load_data_from_db():
    try:
        conn = sqlite3.connect(DB_FILE)
        # 記得讀取 lat 和 lon
        df = pd.read_sql("SELECT location, description, wind_speed, wave_height, lat, lon FROM weather", conn)
        conn.close()
        return df
    except Exception as e:
        st.error(f"讀取資料庫失敗: {e}")
        return pd.DataFrame()

# --- Streamlit 頁面設定 ---
st.set_page_config(page_title="台灣海象地圖", layout="wide")

st.title("🌊 台灣近海海象觀測地圖")
st.markdown("將滑鼠游標移到地圖上的**圓點**，即可查看詳細天氣資訊。")

# --- 1️⃣ 自動更新邏輯 ---
if 'first_load' not in st.session_state:
    with st.spinner('正在初始化並下載最新天氣資料...'):
        success, msg = run_weather_crawler_task()
        if success:
            st.toast(f"🎉 網頁開啟自動更新：{msg}", icon="✅")
        else:
            st.error(f"自動更新失敗: {msg}")
    st.session_state['first_load'] = True

col1, col2 = st.columns([3, 1])

# 讀取資料
df = load_data_from_db()

if not df.empty:
    with col1:
        # 🌟 繪製地圖的核心程式碼 🌟
        fig = px.scatter_mapbox(
            df,
            lat="lat",          # 資料庫的緯度欄位
            lon="lon",          # 資料庫的經度欄位
            hover_name="location", # 滑鼠懸停顯示地點名
            hover_data={        # 滑鼠懸停顯示的其他資訊
                "lat": False,   # 隱藏經緯度顯示
                "lon": False,
                "description": True,
                "wind_speed": True,
                "wave_height": True
            },
            color="description", # 根據天氣狀況顯示不同顏色
            zoom=6,             # 初始縮放大小
            center={"lat": 23.8, "lon": 121}, # 台灣中心點
            height=600,         # 地圖高度
            size_max=15         # 點的大小
        )
        
        # 設定地圖樣式
        fig.update_layout(mapbox_style="open-street-map")
        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0}) # 去除邊框
        
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("📊 詳細數據列表")
        
        # 手動更新按鈕
        if st.button("🔄 手動更新資料", type="primary"):
            with st.spinner("正在更新..."):
                success, msg = run_weather_crawler_task()
                if success:
                    st.success(msg)
                    time.sleep(1) # 讓使用者看到成功訊息
                    st.rerun() # 重新整理頁面以顯示新資料
                else:
                    st.error(msg)
        
        # 顯示簡易表格在旁邊
        st.dataframe(
            df[['location', 'description', 'wave_height']],
            hide_index=True,
            use_container_width=True
        )
else:
    st.error("資料庫讀取失敗或無資料，請先執行爬蟲程式。")