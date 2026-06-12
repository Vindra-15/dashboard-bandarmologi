import streamlit as st
import pandas as pd
from downloader import get_broker_summary

st.set_page_config(page_title="Moneyflow Bandarmologi", layout="wide")
st.title("📊 Dashboard Moneyflow IHSG")
st.caption("Mendeteksi Aliran Dana Asing (Foreign Flow) Langsung dari API IDX")

st.sidebar.header("Pengaturan Analisis")
ticker = st.sidebar.text_input("Kode Saham:", "BBRI").upper()
tanggal_pilihan = st.sidebar.date_input("Pilih Tanggal:")
tanggal_str = tanggal_pilihan.strftime("%Y-%m-%d")

if st.sidebar.button("Analisis"):
    df_saham = get_broker_summary(ticker, tanggal_str)

    if not df_saham.empty:
        # Ambil nilai baris pertama dari hasil filter saham
        saham_data = df_saham.iloc[0]

        nilai_transaksi = float(saham_data.get('Value', 0))
        foreign_buy = float(saham_data.get('ForeignBuy', 0))
        foreign_sell = float(saham_data.get('ForeignSell', 0))
        net_foreign_flow = foreign_buy - foreign_sell

        col1, col2, col3 = st.columns(3)
        col1.metric("Total Nilai Transaksi", f"Rp {nilai_transaksi:,.0f}")
        col2.metric("Net Foreign Flow", f"Rp {net_foreign_flow:,.0f}")

        if net_foreign_flow > 0:
            col3.metric("Status Aliran Asing", "🟢 ACCUMULATION")
        elif net_foreign_flow < 0:
            col3.metric("Status Aliran Asing", "🔴 DISTRIBUTION")
        else:
            col3.metric("Status Aliran Asing", "⚪ NEUTRAL")
    else:
        st.warning("Data tidak ditemukan. Pastikan Anda memilih hari bursa (Senin-Jumat) dan pasar hari tersebut sudah tutup (di atas jam 17:00 WIB).")
