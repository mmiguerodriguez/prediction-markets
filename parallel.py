import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from main import execute

# config["date"] = time.strftime("%Y-%m-%d %H:%M:%S")
# config["filename"] = int(time.time())
# config["n"]
# config["delta"]
# config["deltaQ"]
# config["player_type"]
# config["weights"]
# config["rules"]
# config["radius"]
# config["noise_function"]
# config["noise_delta"]

configs = [
  { "n": 4, "delta": 0.01, "deltaQ": 0.05, "player_type": "perfect", "weights": [0.25, 0.25, 0.25, 0.25], "rules": ["brier", "brier", "brier", "brier"], "noise_function": "identity", "noise_delta": 0.01 },
  { "n": 4, "delta": 0.01, "deltaQ": 0.05, "player_type": "perfect", "weights": [0.25, 0.25, 0.25, 0.25], "rules": ["brier", "brier", "brier", "brier"], "noise_function": "identity", "noise_delta": 0.01 },
  { "n": 4, "delta": 0.01, "deltaQ": 0.05, "player_type": "perfect", "weights": [0.25, 0.25, 0.25, 0.25], "rules": ["brier", "brier", "brier", "brier"], "noise_function": "identity", "noise_delta": 0.01 },
  { "n": 4, "delta": 0.01, "deltaQ": 0.05, "player_type": "perfect", "weights": [0.25, 0.25, 0.25, 0.25], "rules": ["brier", "brier", "brier", "brier"], "noise_function": "identity", "noise_delta": 0.01 },
  { "n": 4, "delta": 0.01, "deltaQ": 0.05, "player_type": "perfect", "weights": [0.25, 0.25, 0.25, 0.25], "rules": ["brier", "brier", "brier", "brier"], "noise_function": "identity", "noise_delta": 0.01 },
  { "n": 4, "delta": 0.01, "deltaQ": 0.05, "player_type": "perfect", "weights": [0.25, 0.25, 0.25, 0.25], "rules": ["brier", "brier", "brier", "brier"], "noise_function": "identity", "noise_delta": 0.01 },
  { "n": 4, "delta": 0.01, "deltaQ": 0.05, "player_type": "perfect", "weights": [0.25, 0.25, 0.25, 0.25], "rules": ["brier", "brier", "brier", "brier"], "noise_function": "identity", "noise_delta": 0.01 },
]

def run_execute(config):
  config["date"] = time.strftime("%Y-%m-%d %H:%M:%S")
  config["filename"] = int(time.time())
  execute(config)

with ThreadPoolExecutor(max_workers=len(configs)) as executor:
  futures = [executor.submit(run_execute, config) for config in configs]
  for future in as_completed(futures):
    try:
      future.result()
    except Exception as e:
      print(f"Exception: {e}")

print("All tasks completed.")