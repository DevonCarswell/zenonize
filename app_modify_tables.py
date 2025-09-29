from db_connection import get_db_connection
import pandas as pd

def login_player(nickname, email_code):
    # """
    # Log in a player by Nickname and E-mail_code.
    # If the player does not exist in table_Players.csv, add a new row with empty attempts.
    # If the player exists, login is denied.
    # """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        # Check if player exists
        cursor.execute("SELECT nickname FROM players WHERE nickname = ?", (nickname,))
        if cursor.fetchone():
            print(f"❌ Player '{nickname}' already exists. Login denied.")
            return None
            
        # Create new player
        cursor.execute(
            "INSERT INTO players (nickname, email_code) VALUES (?, ?)",
            (nickname, email_code)
        )
        conn.commit()
        print(f"✅ New player '{nickname}' added and logged in.")
        return True




def update_player_attempt(nickname, email_code, profit, attempt_idx):
    """
    Update the players table with the new profit result for a specific attempt.
    attempt_idx should be 0-4 (representing attempts 1-5)
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        # Find the player
        cursor.execute("SELECT * FROM players WHERE nickname = ?", (nickname,))
        player = cursor.fetchone()
        if not player:
            raise ValueError(f"Player with nickname '{nickname}' not found. Did you login first?")
            
        # Update email_code to keep it consistent
        cursor.execute(
            "UPDATE players SET email_code = ? WHERE nickname = ?",
            (email_code, nickname)
        )

        # Update the specific attempt column (attempt_idx + 1 because columns are 1-based)
        attempt_num = attempt_idx + 1
        cursor.execute(
            f"UPDATE players SET attempt_{attempt_num} = ? WHERE nickname = ?",
            (profit, nickname)
        )
        conn.commit()
        print(f"✅ Profit {profit} saved for {nickname} in attempt {attempt_num}.")
        return True

def update_leaderboard(nickname, profit):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        # First check if player exists and compare profits
        cursor.execute("SELECT profit FROM leaderboard WHERE nickname = ?", (nickname,))
        result = cursor.fetchone()
        
        if result:
            # Update only if new profit is higher
            if profit > result[0]:
                cursor.execute(
                    "UPDATE leaderboard SET profit = ? WHERE nickname = ?",
                    (profit, nickname)
                )
        else:
            # Insert new record
            cursor.execute(
                "INSERT INTO leaderboard (nickname, profit) VALUES (?, ?)",
                (nickname, profit)
            )
        
        conn.commit()

def get_rank_for_profit(profit):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM leaderboard WHERE profit > ?", (profit,))
        rank = cursor.fetchone()[0] + 1
        return rank


def get_simulation_results():
    """Get all simulation results from the database"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        # Read all records from simulation_results table
        cursor.execute("SELECT * FROM simulation_results")
        columns = [desc[0] for desc in cursor.description]  # Get column names
        rows = cursor.fetchall()
        
        # Convert to pandas DataFrame
        df = pd.DataFrame(rows, columns=columns)    
        
        return df