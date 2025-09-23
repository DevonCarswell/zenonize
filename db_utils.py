from sqlalchemy import create_engine
import streamlit as st

def get_db_connection():
    """
    Create and return a SQLAlchemy engine for database connection.
    """
    db_url = "postgresql://postgres:2P62dm>rDLC8wDI3-:<@db:5432/zenonize"
    # db_url = f"postgresql://{st.secrets['DB_USER']}:{st.secrets['DB_PASSWORD']}@{st.secrets['DB_HOST']}:{st.secrets['DB_PORT']}/{st.secrets['DB_NAME']}"
    engine = create_engine(db_url)
    return engine
