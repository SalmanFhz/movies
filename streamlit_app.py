import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load Dataset
st.title("Analisis Data Film")
st.subheader("source: https://www.kaggle.com/datasets/fernandogarciah24/top-1000-imdb-dataset")
# Baca file CSV dari lokal
file_path = "movies_data.csv"  # Ganti dengan path file CSV Anda
try:
    df = pd.read_csv(file_path)
    
    st.header("Dataset")
    st.write(df.head())
    
    # Analisis Genre
    st.subheader("Rata-rata Rating IMDB per Genre")
    genre_ratings = df.groupby('Genre')['IMDB_Rating'].mean().sort_values(ascending=False)
    st.bar_chart(genre_ratings)

    # Analisis Pendapatan (Gross)
    st.subheader("Hubungan Rating dengan Pendapatan Film")
    fig1, ax1 = plt.subplots()
    ax1.scatter(df['IMDB_Rating'], df['Gross'])
    ax1.set_title('Hubungan Rating dengan Pendapatan Film')
    ax1.set_xlabel('Rating IMDB')
    ax1.set_ylabel('Pendapatan (Gross)')
    st.pyplot(fig1)

    # Analisis Sutradara (Top 10 Berdasarkan Jumlah Film)
    st.subheader("Top 10 Sutradara Berdasarkan Jumlah Film")
    director_counts = df['Director'].value_counts().head(10)
    st.bar_chart(director_counts)

    # Analisis Temporal (Perbaikan Label Tahun)
    st.subheader("Trend Rating Film Berdasarkan Tahun")
    if 'Released_Year' in df.columns:
        # Pastikan kolom tahun berupa angka
        df['Released_Year'] = pd.to_numeric(df['Released_Year'], errors='coerce')
        
        # Drop NaN jika ada
        df = df.dropna(subset=['Released_Year'])
        
        # Hitung rata-rata rating berdasarkan tahun
        year_ratings = df.groupby('Released_Year')['IMDB_Rating'].mean()

        fig2, ax2 = plt.subplots(figsize=(10, 6))
        ax2.plot(year_ratings.index, year_ratings.values, marker='o')
        ax2.set_title('Trend Rating Film Berdasarkan Tahun')
        ax2.set_xlabel('Tahun')
        ax2.set_ylabel('Rating IMDB Rata-rata')

        # Atur jarak antar label tahun
        ax2.set_xticks(year_ratings.index[::5])  # Tampilkan setiap 5 tahun
        ax2.tick_params(axis='x', rotation=45)  # Rotasi label agar rapi
        st.pyplot(fig2)
    else:
        st.warning("Kolom 'Released_Year' tidak ditemukan dalam dataset.")


    # Analisis Sutradara: Jumlah Film vs Total Gross
    st.subheader("Top 10 Sutradara: Jumlah Film vs Total Gross")
    director_film_gross = df.groupby('Director').agg({
        'Series_Title': 'count',  # Jumlah film
        'Gross': 'sum'  # Total gross
    }).sort_values('Gross', ascending=False).head(10)
    director_film_gross.columns = ['Jumlah Film', 'Total Gross']

    fig3, ax3 = plt.subplots(figsize=(12, 6))
    ax3.bar(director_film_gross.index, director_film_gross['Jumlah Film'], color='blue', alpha=0.7, label='Jumlah Film')
    ax3.set_xlabel('Sutradara')
    ax3.set_ylabel('Jumlah Film', color='blue')
    ax3.tick_params(axis='y', labelcolor='blue')
    plt.xticks(rotation=45, ha='right')

    ax4 = ax3.twinx()
    ax4.plot(director_film_gross.index, director_film_gross['Total Gross'], color='black', marker='o', label='Total Gross')
    ax4.set_ylabel('Total Gross ($)', color='black')
    ax4.tick_params(axis='y', labelcolor='black')

    plt.title('Top 10 Sutradara: Jumlah Film vs Total Gross')
    st.pyplot(fig3)

    # Analisis Sutradara: Total Gross vs IMDB Rating
    st.subheader("Top 10 Sutradara: Total Gross vs Rata-rata IMDB Rating")
    director_film_analysis = df.groupby('Director').agg({
        'Series_Title': 'count',  # Jumlah film
        'Gross': 'sum',           # Total gross
        'IMDB_Rating': 'mean'     # Rata-rata IMDB Rating
    }).sort_values('Gross', ascending=False).head(10)
    director_film_analysis.columns = ['Jumlah Film', 'Total Gross', 'Rata-rata IMDB Rating']

    fig4, ax5 = plt.subplots(figsize=(14, 7))
    ax5.bar(director_film_analysis.index, director_film_analysis['Total Gross'], 
            color='blue', alpha=0.7, label='Total Gross')
    ax5.set_xlabel('Sutradara')
    ax5.set_ylabel('Total Gross ($)', color='blue')
    ax5.tick_params(axis='y', labelcolor='blue')
    plt.xticks(rotation=45, ha='right')

    ax6 = ax5.twinx()
    ax6.plot(director_film_analysis.index, director_film_analysis['Rata-rata IMDB Rating'], 
             color='red', marker='o', label='Rata-rata IMDB Rating')
    ax6.set_ylabel('Rata-rata IMDB Rating', color='red')
    ax6.tick_params(axis='y', labelcolor='red')

    plt.title('Top 10 Sutradara: Total Gross vs Rata-rata IMDB Rating')
    st.pyplot(fig4)

except FileNotFoundError:
    st.error(f"File '{file_path}' tidak ditemukan. Pastikan file CSV berada di path yang benar.")
