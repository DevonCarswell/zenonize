import streamlit as st
from streamlit_autorefresh import st_autorefresh
from db_connection import get_db_connection


def show_leaderboard():
    # ---------- Automatikus frissítés ----------
    #10 másodpercenként újratölti az oldalt
    st_autorefresh(interval=10 * 1000, key="leaderboard_refresh")

    # ---------- Streamlit UI ----------
    st.image("header.png", width='content')
    st.subheader("Leaderboard 🏆")

    # 🔹 Add Back button at the bottom
    if st.button("⬅️ Back"):
        st.session_state.page = "login"
        st.query_params.clear()
        st.rerun()
    # Helyezés hozzáadása
    bg_colors = {1: "#B9A534", 2: "#858585", 3: "#AD7134"}  # arany, ezüst, bronz
    border_color = "#FFFFFF"  # keret szín a 4. helytől

    # Load from database instead of CSV
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT nickname, profit FROM leaderboard ORDER BY profit DESC")
        rows = cursor.fetchall()

    # Dense ranking
    rank = 0
    prev_profit = None
    for idx, (nickname, profit) in enumerate(rows, 1):
        if profit != prev_profit:  # new profit → new rank
            rank = idx
            prev_profit = profit

        # Style for top 3
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

        # Ordinal suffix (1st, 2nd, 3rd, etc.)
        def ordinal(n):
            return "%d%s" % (n, "tsnrhtdd"[(n//10%10!=1)*(n%10<4)*n%10::4])

        st.markdown(f"""
        <div style="{style}">
            <div style="display:flex; align-items:center; gap:10px;">
                <span style="font-weight:bold; width:41px;">{ordinal(rank)}</span>
                <span style="font-weight:bold; font-size:16px;">{nickname}</span>
            </div>
            <div style="font-size:16px;">€{profit:.2f}</div>
        </div>
        """, unsafe_allow_html=True)
