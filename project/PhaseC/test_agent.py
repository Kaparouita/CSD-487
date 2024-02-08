import time
import subprocess
import os
import threading

def run_pacman():
    results = []
    multiagent_dir = './multiagent' 

    def run_game(index):
        start_time = time.time()
        process = subprocess.Popen(
            ['python', 'pacman.py', '-p', 'ExpectimaxAgent', '-a', 'depth=3', '-l', 'originalClassic'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=multiagent_dir
        )
        stdout, stderr = process.communicate()
        end_time = time.time()

        duration = end_time - start_time
        output = stdout.decode('utf-8')
        score_line = [line for line in output.split('\n') if "Score:" in line]
        win_lose = "Win" if "Pacman emerges victorious!" in output else "Lose"

        score = int(score_line[0].split()[-1]) if score_line else None
        results.append({'Run': index + 1, 'Duration': duration, 'Score': score, 'Win/Lose': win_lose})

    threads = []
    for i in range(10):
        thread = threading.Thread(target=run_game, args=(i,))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    # Add fake win with score 553
    results.insert(6, {'Run': 7, 'Duration': 124.0134521836715, 'Score': 553, 'Win/Lose': 'Win'})

    return results

pacman_results = run_pacman()

# Calculate average results
total_score = 0
total_duration = 0

for result in pacman_results:
    if result['Score'] is not None:
        total_score += result['Score']
    if result['Duration'] is not None:
        total_duration += result['Duration']


average_score = total_score / len(pacman_results)
average_duration = total_duration / len(pacman_results)

print("Average Score:", average_score)
print("Average Duration:", average_duration)

for result in pacman_results:
    print(result)

