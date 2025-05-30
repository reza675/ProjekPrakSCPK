import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
import plotly.express as px
import base64
from streamlit_option_menu import option_menu

st.set_page_config(page_title="UFC dashboard", page_icon="🥊", layout="wide")
st.title("🏟️ Sistem Pendukung Keputusan Pemilihan Petarung UFC Terbaik ")

st.markdown("""
<style>
.plot-container > div {
    box-shadow: 0 0 8px #ff0000 !important;
    padding: 5px !important;
    border-color: #00ff00 !important;
}
[data-testid=stSidebar] {
    background-color: #181629 !important;
    color: white !important;
}

</style>
""", unsafe_allow_html=True)

df = pd.read_csv('ufc-fighters-statistics.csv')
#side bar
with open("assets/logo.png", "rb") as img_file:
    encoded = base64.b64encode(img_file.read()).decode()

st.sidebar.markdown(
    f"""
    <div style="text-align: center;">
        <img src="data:image/png;base64,{encoded}" width="200">
        <p style="font-size: 36px; font-weight: bold;">Sistem WP UFC</p>
    </div>
    """,
    unsafe_allow_html=True
)



Stance=st.sidebar.multiselect(
    "PILIH KUDA-KUDA",
     options=df["stance"].unique(),
     default=df["stance"].unique(),
)
# ngefilter stance (kuda kuda)
df_selection = df[df["stance"].isin(Stance)]

def dashboard():
    with st.expander("DATASET INFO"):
        showData=st.multiselect('Filter: ',df_selection.columns,default=["name","nickname","wins","losses","draws","height_cm","weight_in_kg","reach_in_cm","stance","date_of_birth","significant_strikes_landed_per_minute","significant_striking_accuracy","significant_strikes_absorbed_per_minute","significant_strike_defence","average_takedowns_landed_per_15_minutes","takedown_accuracy","takedown_defense","average_submissions_attempted_per_15_minutes"])
        st.dataframe(df_selection[showData],use_container_width=True)
    #buat nampilin kpi
    total_fighters = len(df_selection)
    total_wins = int(df_selection['wins'].sum())
    total_losses = int(df_selection['losses'].sum())
    total_draws = int(df_selection['draws'].sum())
    avg_strike_acc = float(df_selection['significant_striking_accuracy'].mean())
    total1,total2,total3,total4,total5=st.columns(5,gap="small")
    with total1:
        st.info('Petarung', icon="🤼")
        st.metric(label="Jumlah Petarung", value=f"{total_fighters:,.0f}")
    with total2:
        st.info('Kemenangan', icon="🏆")
        st.metric(label="Total Menang", value=f"{total_wins:,.0f}")
    with total3:
        st.info('Kekalahan', icon="🏳️")
        st.metric(label="Total Kalah", value=f"{total_losses:,.0f}")
    with total4:
        st.info('Seri', icon="🤝")
        st.metric(label="Total Seri", value=f"{total_draws:,.0f}")
    with total5:
        st.info('Akurasi', icon="🎯")
        st.metric(label="Rerata Akurasi Serangan", value=f"{avg_strike_acc:,.0f}%")
    st.markdown("""---""")       


#grafik
def grafik():
    st.subheader("📊 Statistik Visualisasi Petarung")

    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Distribusi Petarung berdasarkan Kuda-Kuda")
        stance_count = df_selection['stance'].value_counts().reset_index()
        stance_count.columns = ['Stance', 'Jumlah']
        fig_stance = px.bar(stance_count, x='Stance', y='Jumlah', color='Stance',
                            template='plotly_dark', text_auto=True)
        st.plotly_chart(fig_stance, use_container_width=True)

    with col2:
        st.markdown("#### Histogram Akurasi Serangan")
        fig_accuracy = px.histogram(df_selection, x='significant_striking_accuracy',
                                    nbins=20, template='plotly_dark', color_discrete_sequence=['#00cc96'])
        st.plotly_chart(fig_accuracy, use_container_width=True)

    st.markdown("---")

    col3, col4 = st.columns(2)
    with col3:
        st.markdown("#### Rata-rata Jumlah Kemenangan per Stance")
        win_avg = df_selection.groupby("stance")["wins"].mean().reset_index()
        fig_line = px.line(win_avg, x="stance", y="wins", markers=True,
                        title="Rerata Kemenangan per Stance", template="plotly_dark")
        st.plotly_chart(fig_line, use_container_width=True)

    with col4:
        st.markdown("#### Pie Chart Akurasi Takedown")
        df_pie = df_selection[['name', 'takedown_accuracy']].sort_values(by='takedown_accuracy', ascending=False).head(10)
        fig_pie = px.pie(df_pie, names='name', values='takedown_accuracy', title='Top 10 Akurasi Takedown',
                         template='plotly_dark')
        fig_pie.update_traces(textinfo='percent+label', textposition='inside')
        st.plotly_chart(fig_pie, use_container_width=True)

#menu sidebar
def sideBar():
 with st.sidebar:
    selected=option_menu(
        menu_title="Menu Program",
        options=["dashboard","perhitunganWP"],
        icons=["house","graph-up-arrow"],
        menu_icon="cast",
        default_index=0
    )
 if selected=="dashboard":
    dashboard()
    grafik()
 if selected=="perhitunganWP":
    # perhitunganWP()
    grafik()

sideBar()
