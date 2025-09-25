import streamlit as st
from streamlit_autorefresh import st_autorefresh
from db_connection import get_db_connection

# ---------- Automatikus frissítés ----------
#10 másodpercenként újratölti az oldalt
st_autorefresh(interval=10 * 1000, key="leaderboard_refresh")

# ---------- Streamlit UI ----------
st.image("header.png", width='content')
st.subheader("Leaderboard 🏆")

# Helyezés hozzáadása
bg_colors = {1: "#B9A534", 2: "#858585", 3: "#AD7134"}  # arany, ezüst, bronz
border_color = "#FFFFFF"  # keret szín a 4. helytől

# Load from database instead of CSV
with get_db_connection() as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT nickname, profit FROM leaderboard ORDER BY profit DESC")
    rows = cursor.fetchall()
    
    for rank, (nickname, profit) in enumerate(rows, 1):
        if rank <= 3:
            style = f"""
            background-color:{bg_colors[rank]};
            border-radius:12px;
            border:1px solid {border_color};
            padding:12px 20px;
            margin-bottom:8px;
            display:flex;
            justify-content:space-between;
            align-items:center;
            font-family:sans-serif;
            """
        else:
            style = f"""
            background-color:transparent;
            border-radius:12px;
            border:1px solid {border_color};
            padding:12px 20px;
            margin-bottom:8px;
            display:flex;
            justify-content:space-between;
            align-items:center;
            font-family:sans-serif;
            """

        st.markdown(f"""
        <div style="{style}">
            <div style="display:flex; align-items:center; gap:10px;">
                <span style="font-weight:bold; width:40px;">{rank}{"st" if rank==1 else "nd" if rank==2 else "rd" if rank==3 else "th"}</span>
                <span style="font-weight:bold; font-size:16px;">{nickname}</span>
            </div>
            <div style="font-size:16px;">€{profit:.2f}</div>
        </div>
        """, unsafe_allow_html=True)





















