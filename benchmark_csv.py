import time
import random
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed
from statistics import mean, median
import os
from pathlib import Path
import shutil

# Test CSV paths
TEST_PLAYERS_CSV = "./test_data/table_Players.csv"
TEST_LEADERBOARD_CSV = "./test_data/table_Leaderboard.csv"

def setup_test_csvs():
    """Create test CSV files"""
    os.makedirs("./test_data", exist_ok=True)
    
    # Create fresh Players CSV
    players_df = pd.DataFrame(columns=[
        'Nickname', 'Email_code', 'Attempt_1', 'Attempt_2', 
        'Attempt_3', 'Attempt_4', 'Attempt_5'
    ])
    players_df.to_csv(TEST_PLAYERS_CSV, index=False)
    
    # Create fresh Leaderboard CSV
    leaderboard_df = pd.DataFrame(columns=['Nickname', 'Profit'])
    leaderboard_df.to_csv(TEST_LEADERBOARD_CSV, index=False)

def create_test_user(nickname):
    """Create a test user in CSV"""
    try:
        df = pd.read_csv(TEST_PLAYERS_CSV)
        if nickname not in df['Nickname'].values:
            new_row = pd.DataFrame({
                'Nickname': [nickname],
                'Email_code': [f"test_{nickname}@test.com"],
                'Attempt_1': [None],
                'Attempt_2': [None],
                'Attempt_3': [None],
                'Attempt_4': [None],
                'Attempt_5': [None]
            })
            df = pd.concat([df, new_row], ignore_index=True)
            df.to_csv(TEST_PLAYERS_CSV, index=False)
    except Exception as e:
        print(f"Error creating user {nickname}: {str(e)}")

def update_attempt_test(nickname, attempt_idx):
    """Test function for single attempt update using CSV"""
    start_time = time.time()
    profit = random.uniform(1000, 10000)
    attempt_num = attempt_idx + 1
    
    try:
        df = pd.read_csv(TEST_PLAYERS_CSV)
        df.loc[df['Nickname'] == nickname, f'Attempt_{attempt_num}'] = profit
        df.to_csv(TEST_PLAYERS_CSV, index=False)
        
        end_time = time.time()
        return end_time - start_time
    except Exception as e:
        print(f"Error for {nickname} attempt {attempt_num}: {str(e)}")
        return None

def run_benchmark(num_users):
    """Run benchmark with specified number of users"""
    print(f"\nRunning CSV benchmark with {num_users} users...")
    
    # Create test users in batches
    print("Creating test users...")
    batch_size = 100
    with ThreadPoolExecutor(max_workers=1) as executor: # original worker numbers: 20
        for i in range(0, num_users, batch_size):
            batch = [f"test_user_{j}" for j in range(i, min(i + batch_size, num_users))]
            list(executor.map(create_test_user, batch))
    
    # Statistics per attempt
    attempt_stats = {i: [] for i in range(1, 6)}
    
    # Run updates for each attempt sequentially
    for attempt in range(1, 6):
        print(f"\nRunning attempt {attempt} updates...")
        start_attempt = time.time()
        
        with ThreadPoolExecutor(max_workers=1) as executor: # original worker numbers: 50
            futures = {
                executor.submit(update_attempt_test, f"test_user_{i}", attempt-1): i 
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
    print("Setting up test CSV files...")
    setup_test_csvs()
    
    run_benchmark(100)    # Test with 100 users
    run_benchmark(1000)   # Test with 1000 users
    
    # Cleanup
    #shutil.rmtree("./test_data")

if __name__ == "__main__":
    main()
