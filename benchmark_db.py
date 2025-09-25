import time
import random
import sqlite3
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from statistics import mean, median
import shutil
from contextlib import contextmanager

# Test database path
TEST_DB_PATH = "./db/test_zenonize.db"

def setup_test_db():
    """Create a copy of the production database for testing"""
    if os.path.exists(TEST_DB_PATH):
        os.remove(TEST_DB_PATH)
    shutil.copy("./db/zenonize.db", TEST_DB_PATH)

@contextmanager
def get_test_db_connection():
    """Context manager for test database connections with proper isolation level"""
    conn = sqlite3.connect(TEST_DB_PATH, timeout=30.0)  # 30 sec timeout
    # conn.execute("PRAGMA journal_mode=WAL")  # Write-Ahead Logging for better concurrency
    conn.execute("PRAGMA synchronous=NORMAL")  # Faster writes with reasonable safety
    try:
        yield conn
    finally:
        conn.close()

def create_test_user(nickname):
    """Create a test user for benchmarking"""
    with get_test_db_connection() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO players (nickname, email_code) VALUES (?, ?)",
                (nickname, f"test_{nickname}@test.com")
            )
            conn.commit()
        except sqlite3.IntegrityError:
            pass  # Ignore if user already exists

def update_attempt_test(nickname, attempt_idx):
    """Test function for single attempt update with sequential attempts"""
    start_time = time.time()
    profit = random.uniform(1000, 10000)
    
    try:
        with get_test_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("BEGIN IMMEDIATE")
            
            # Update specific attempt (attempt_idx is already 1-based)
            cursor.execute(
                f"UPDATE players SET attempt_{attempt_idx} = ? WHERE nickname = ?",
                (profit, nickname)
            )
            
            conn.commit()
            end_time = time.time()
            return end_time - start_time
    except Exception as e:
        print(f"Error for {nickname} attempt {attempt_idx}: {str(e)}")
        return None

def run_benchmark(num_users):
    """Run benchmark with specified number of users"""
    print(f"\nRunning benchmark with {num_users} users...")
    
    # Create test users in batches
    print("Creating test users...")
    batch_size = 100
    with ThreadPoolExecutor(max_workers=1) as executor:
        for i in range(0, num_users, batch_size):
            batch = [f"test_user_{j}" for j in range(i, min(i + batch_size, num_users))]
            list(executor.map(create_test_user, batch))
    
    # Statistics per attempt
    attempt_stats = {i: [] for i in range(1, 6)}
    
    # Run updates for each attempt sequentially
    for attempt in range(1, 6):
        print(f"\nRunning attempt {attempt} updates...")
        start_attempt = time.time()
        
        with ThreadPoolExecutor(max_workers=1) as executor:
            futures = {
                executor.submit(update_attempt_test, f"test_user_{i}", attempt): i 
                for i in range(num_users)
            }
            
            for future in as_completed(futures):
                time_taken = future.result()
                if time_taken is not None:
                    attempt_stats[attempt].append(time_taken)
        
        # Print statistics for this attempt
        times = attempt_stats[attempt]
        if times:
            print(f"\nAttempt {attempt} Results:")
            print(f"Successful updates: {len(times)}/{num_users}")
            print(f"Average time: {mean(times):.3f} seconds")
            print(f"Median time: {median(times):.3f} seconds")
            print(f"Min time: {min(times):.3f} seconds")
            print(f"Max time: {max(times):.3f} seconds")
    
    # Overall statistics
    all_times = [t for times in attempt_stats.values() for t in times]
    total_updates = len(all_times)
    total_time = time.time() - start_attempt
    
    print(f"\nOverall Results:")
    print(f"Total time for all attempts: {total_time:.2f} seconds")
    print(f"Total successful updates: {total_updates}/{num_users * 5}")
    print(f"Average request time across all attempts: {mean(all_times):.3f} seconds")
    print(f"Median request time across all attempts: {median(all_times):.3f} seconds")
    print(f"Updates per second: {total_updates/total_time:.1f}")

def main():
    """Main benchmark function"""
    print("Setting up test database...")
    setup_test_db()
    
    run_benchmark(100)    # Test with 100 users
    run_benchmark(1000)   # Test with 1000 users

if __name__ == "__main__":
    main()
