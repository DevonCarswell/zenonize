from sqlalchemy import create_engine
import streamlit as st

def get_db_connection():
    """
    Create and return a SQLAlchemy engine for database connection.
    """
    db_url = f"postgresql://{st.secrets['DB_USER']}:{st.secrets['DB_PASSWORD']}@{st.secrets['DB_HOST']}:{st.secrets['DB_PORT']}/{st.secrets['DB_NAME']}"
    engine = create_engine(db_url)
    return engine
