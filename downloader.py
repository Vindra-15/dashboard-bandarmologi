# downloader.py
import yfinance as yf
import pandas as pd

def get_broker_summary(ticker, tanggal):
    """
    Mengambil data perdagangan harian pasar historis dari Yahoo Finance.
    Format ticker Indonesia di Yahoo Finance harus diakhiri '.JK' (Contoh: BBRI.JK)
    """
    # Menambahkan ekstensi bursa Jakarta (.JK) jika belum ada
    ticker_jk = f"{ticker.upper()}.JK" if not ticker.endswith(".JK") else ticker.upper()
    
    try:
        # Inisialisasi Ticker
        stock = yf.Ticker(ticker_jk)
        
        # Ambil data historis harian spesifik pada tanggal tersebut
        # Kita ambil rentang 5 hari ke belakang agar memastikan data sebelum tanggal tersebut ikut terbaca
        df_hist = stock.history(start=tanggal, period="1d")
        
        if not df_hist.empty:
            # Mengembalikan baris pertama data yang ditemukan
            df_cleaned = df_hist.reset_index()
            # Menyeragamkan kolom agar dibaca sebagai format data bursa oleh app.py
            df_cleaned['Value'] = df_cleaned['Close'] * df_cleaned['Volume']
            df_cleaned['StockCode'] = ticker.upper()
            return df_cleaned
            
        return pd.DataFrame()
    except Exception as e:
        print(f"Error Yahoo Finance: {e}")
        return pd.DataFrame()
