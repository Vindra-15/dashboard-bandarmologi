import streamlit as st
import pandas as pd
from downloader import get_broker_summary
import plotly.express as px

st.set_page_config(page_title="Moneyflow Bandarmologi", layout="wide")
st.title("📊 Dashboard Moneyflow & Harga IHSG")
st.caption("Penyedia Data Stabil via Yahoo Finance API (Bebas Blokir)")

st.sidebar.header("Pengaturan Analisis")
ticker = st.sidebar.text_input("Kode Saham:", "BBRI").upper()
tanggal_pilihan = st.sidebar.date_input("Pilih Tanggal:")
tanggal_str = tanggal_pilihan.strftime("%Y-%m-%d")

if st.sidebar.button("Analisis"):
    df_saham = get_broker_summary(ticker, tanggal_str)
    
    if not df_saham.empty:
        saham_data = df_saham.iloc[0]
        
        harga_close = float(saham_data.get('Close', 0))
        volume_transaksi = float(saham_data.get('Volume', 0))
        nilai_transaksi = float(saham_data.get('Value', 0))
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Harga Penutupan (Close)", f"Rp {harga_close:,.0f}")
        col2.metric("Volume Transaksi", f"{volume_transaksi:,.0f} Lembar")
        col3.metric("Estimasi Nilai Perputaran", f"Rp {nilai_transaksi:,.0f}")
        
        st.markdown("---")
        st.subheader(f"📈 Grafik Performa Historis Saham {ticker}")
        st.info("Menampilkan rangkuman volume perdagangan harian.")
        
        # Membuat visualisasi data ringkas
        fig = px.bar(df_saham, x='Date', y='Volume', title=f"Volume Perdagangan Saham {ticker}")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Data tidak ditemukan untuk tanggal ini. Mohon ganti ke tanggal hari kerja bursa yang telah lewat (Senin-Jumat).")
