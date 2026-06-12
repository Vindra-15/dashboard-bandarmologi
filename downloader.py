import requests
import pandas as pd

def get_broker_summary(ticker, tanggal):
    tanggal_idx = tanggal.replace("-", "")
    url = f"https://idx.co.id{tanggal_idx}"

    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
        "Connection": "keep-alive",
        "Host": "www.idx.co.id",
        "Referer": "https://idx.co.id",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    try:
        session = requests.Session()
        response = session.get(url, headers=headers, timeout=15)
        if response.status_code == 200:
            json_data = response.json()
            if 'Results' in json_data and json_data['Results']:
                df_all = pd.DataFrame(json_data['Results'])
                df_filtered = df_all[df_all['StockCode'] == ticker.upper()]
                return df_filtered
        return pd.DataFrame()
    except Exception as e:
        return pd.DataFrame()
