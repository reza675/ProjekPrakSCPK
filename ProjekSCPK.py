import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu
import time

# Konfigurasi halaman
st.set_page_config(page_title="UFC Dashboard", page_icon="🥊", layout="wide")
st.title("🏟️ UFC Fighters Analytics Dashboard")

# Load custom CSS (jika ada)
try:
    with open('style.css') as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except FileNotFoundError:
    pass

# Load data dari CSV
@st.cache_data
def load_data():
    return pd.read_csv('ufc-fighters-statistics.csv')

df = load_data()

# --- Sidebar Filters ---
with st.sidebar:
    st.header("Filter Fighters")
    stance_opt = st.multiselect(
        "Select Stance",
        options=df['stance'].dropna().unique(),
        default=df['stance'].dropna().unique()
    )
    weight_range = st.slider(
        "Weight (kg)",
        min_value=int(df['weight_in_kg'].min()),
        max_value=int(df['weight_in_kg'].max()),
        value=(int(df['weight_in_kg'].min()), int(df['weight_in_kg'].max()))
    )
    # Pilih kolom untuk tabel detail
    selected_cols = st.multiselect(
        "Columns to Display",
        options=df.columns.tolist(),
        default=['name', 'nickname', 'wins', 'losses', 'draws', 'stance', 'weight_in_kg']
    )

# Terapkan filter
df_selection = df[
    (df['stance'].isin(stance_opt)) &
    (df['weight_in_kg'] >= weight_range[0]) &
    (df['weight_in_kg'] <= weight_range[1])
]

# --- Fungsi Home ---
def Home():
    st.subheader("Fighter Overview")
    with st.expander("View Table Data"):
        st.dataframe(df_selection[selected_cols], use_container_width=True)

    # KPI Metrics
    total_fighters = len(df_selection)
    total_wins = int(df_selection['wins'].sum())
    total_losses = int(df_selection['losses'].sum())
    total_draws = int(df_selection['draws'].sum())
    avg_strike_acc = df_selection['significant_striking_accuracy'].mean()

    c1, c2, c3, c4, c5 = st.columns(5, gap='small')
    c1.metric("Total Fighters", total_fighters)
    c2.metric("Total Wins", total_wins)
    c3.metric("Total Losses", total_losses)
    c4.metric("Total Draws", total_draws)
    c5.metric("Avg Strike Accuracy", f"{avg_strike_acc:.1f}%")

# --- Fungsi Graphs ---
def Graphs():
    st.subheader("Charts & Trends")

    # Wins distribution
    fig1 = px.histogram(
        df_selection, x='wins', nbins=20,
        title='Distribution of Wins', template='plotly_white'
    )
    st.plotly_chart(fig1, use_container_width=True)

    # Strike accuracy by stance (box)
    fig2 = px.box(
        df_selection, x='stance', y='significant_striking_accuracy',
        title='Strike Accuracy by Stance', template='plotly_white'
    )
    st.plotly_chart(fig2, use_container_width=True)

    # Correlation scatter: reach vs wins
    fig3 = px.scatter(
        df_selection,
        x='reach_in_cm', y='wins',
        size='wins', color='stance',
        title='Reach vs Wins', template='plotly_white',
    )
    st.plotly_chart(fig3, use_container_width=True)

# --- Fungsi Perhitungan SPK WP ---
def Perhitungan_WP():
    st.subheader("Perhitungan SPK WP")
    st.write("Fungsi perhitungan Weighted Product untuk memilih fighter terbaik.")
    # Ini contoh placeholder; implementasi SPK WP Anda di sini.
    if st.button("Mulai Perhitungan WP"):
        st.spinner(text="Menghitung…")
        time.sleep(1)
        st.success("Perhitungan selesai! Hasil dapat disajikan di sini.")

# --- Main Menu ---
with st.sidebar:
    selected = option_menu(
        menu_title="Main Menu",
        options=["Home", "Perhitungan SPK WP"],
        icons=["house", "calculator"],
        menu_icon="layers",
        default_index=0
    )

if selected == "Home":
    Home()
    Graphs()
elif selected == "Perhitungan SPK WP":
    Perhitungan_WP()
    Graphs()

# Hide default Streamlit footer
hide_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>
"""
st.markdown(hide_style, unsafe_allow_html=True)
