from sqlalchemy import text
import pandas as pd
import streamlit as st
from db_utils import get_db_connection  # Import from db_utils.py

def login_player(nickname, email_code):
    """
    Log in a player by Nickname and E-mail_code.
    If the player does not exist in the players table, add a new row with empty attempts.
    If the player exists, login is denied.
    """
    engine = get_db_connection()
    with engine.connect() as conn:
        # Check if the player already exists
        query = text('SELECT * FROM players WHERE "Nickname" = :nickname')
        result = conn.execute(query, {"nickname": nickname}).fetchone()

        if result:
            # Player already exists
            print(f"❌ Player '{nickname}' already exists. Login denied.")
            return None
        else:
            # Insert new player
            query = text("""
                INSERT INTO players ("Nickname", "E-mail_code", "Attempt_1", "Attempt_2", "Attempt_3", "Attempt_4", "Attempt_5")
                VALUES (:nickname, :email_code, NULL, NULL, NULL, NULL, NULL)
            """)
            conn.execute(query, {"nickname": nickname, "email_code": email_code})
            conn.commit()  # Commit the transaction to save the changes
            print(f"✅ New player '{nickname}' added and logged in.")
            return True

def update_player_attempt(nickname, attempt_index, profit):
    """
    Update the players table with the new profit result.
    It will update the Attempt_X column corresponding to the current attempt index.
    """
    engine = get_db_connection()
    with engine.connect() as conn:
        # Find the player row
        query = text('SELECT * FROM players WHERE "Nickname" = :nickname')
        player = conn.execute(query, {"nickname": nickname}).fetchone()

        if not player:
            raise ValueError(f"Player with nickname '{nickname}' not found in table. Did you login first?")

        # Determine the column to update based on the attempt index
        attempt_col = f"Attempt_{attempt_index + 1}"  # Attempt_1 for index 0, Attempt_2 for index 1, etc.

        # Update the corresponding attempt column
        query = text(f'UPDATE players SET "{attempt_col}" = :profit WHERE "Nickname" = :nickname')
        conn.execute(query, {"profit": profit, "nickname": nickname})
        conn.commit()  # Commit the transaction to save the changes
        print(f"✅ Profit {profit} saved for {nickname} in {attempt_col}.")

def update_leaderboard(nickname, profit):
    """
    Update the leaderboard table with the player's profit.
    If the player already exists, update their profit if the new profit is higher.
    """
    engine = get_db_connection()
    with engine.connect() as conn:
        # Check if the player already exists in the leaderboard
        query = text('SELECT "Profit" FROM leaderboard WHERE "Nickname" = :nickname')
        result = conn.execute(query, {"nickname": nickname}).fetchone()

        if result:
            current_profit = result[0]  # Access the first column (Profit) by index
            if profit > current_profit:
                query = text('UPDATE leaderboard SET "Profit" = :profit WHERE "Nickname" = :nickname')
                conn.execute(query, {"profit": profit, "nickname": nickname})
                conn.commit()  # Commit the transaction to save the changes
        else:
            # Insert new record
            query = text('INSERT INTO leaderboard ("Nickname", "Profit") VALUES (:nickname, :profit)')
            conn.execute(query, {"nickname": nickname, "profit": profit})
            conn.commit()  # Commit the transaction to save the changes

        # Sort leaderboard is not needed as SQL queries can handle ordering dynamically

def get_rank_for_profit(profit):
    """
    Return the rank for the given profit in the leaderboard.
    The leaderboard is sorted in descending order by Profit.
    """
    engine = get_db_connection()
    with engine.connect() as conn:
        query = text('SELECT COUNT(*) + 1 AS rank FROM leaderboard WHERE "Profit" > :profit')
        result = conn.execute(query, {"profit": profit}).fetchone()

        # Access the rank using the index (0) instead of a string key
        return result[0] if result else 1