import argparse
import numpy as np
import time

from src.rules import calculateScore
from src.simulation import simulate
from src.player import *
from src.utils import equalRules, equalWeights
from src.results import CSVResultHandler
from src.noise import *

config = {
  "n": 4,
  "delta": 0.01,
  "deltaQ": 0.05
}

def execute(config):
  # ts = int(time.time())

  n = config["n"]
  delta = config["delta"]
  deltaQ = config["deltaQ"]
  player_type = config["player_type"]
  noise_function = config["noise_function"]
  noise_delta = config["noise_delta"]
  
  # Should we add a config for weights, rules?
  weights = equalWeights(n)
  rules = equalRules(n, "brier")

  qValues = np.arange(0, 1 + deltaQ, deltaQ).round(2).tolist()
  possiblePredictions = np.arange(0, 1 + delta, delta).round(2).tolist()

  filename = f"{player_type}-{n}-{delta}-{deltaQ}"
  result_handler = CSVResultHandler(filename, n)
  result_handler.write_headers()

  print(f"Executing simulation...")
  print(f"n = {n}; players = {player_type}; weights = {weights}; rules = {rules}; delta = {delta}; deltaQ = {deltaQ}")

  for q in qValues:
    players = []

    # if p is defined here, all players have same beliefs
    # p = get_noisy_q(q, noiseFn, 0.025)

    if player_type == "relaxed":
      players = [RelaxedInformationPlayer(i, weights[i], rules[i], get_noisy_q(q, noise_function, noise_delta), possiblePredictions, config["radius"]) for i in range(n)]
    elif player_type == "perfect":
      players = [PerfectInformationPlayer(i, weights[i], rules[i], get_noisy_q(q, noise_function, noise_delta), possiblePredictions) for i in range(n)]

    print("Simulation step", [player.p for player in players])

    scores, predictions, finalPrediction, marketPrediction = simulate(players, q)
    result_handler.write_results(q, scores, predictions, finalPrediction, marketPrediction, calculateScore(marketPrediction, finalPrediction, "brier"))

if __name__ == "__main__":
  # with open("config.json", "r") as config_file:
  #   config = json.load(config_file)
  
  parser = argparse.ArgumentParser(description="Run the prediction market simulation.")
  parser.add_argument("--n", type=int, required=True, help="Number of players")
  parser.add_argument("--player_type", type=str, required=True, choices=["perfect", "relaxed"], help="Type of player to instantiate")
  parser.add_argument("--noise", type=str, choices=["identity", "gaussian", "uniform", "sinusoidal", "exponential"], default="identity", help="Noise function")
  parser.add_argument("--noise_delta", type=float, default=0.01, help="Delta for noise function")
  parser.add_argument("--radius", type=int, help="Radius for RelaxedInformationPlayer")

  args = parser.parse_args()

  config["n"] = args.n
  config["player_type"] = args.player_type
  # config["rule"] = args.rule
  config["noise_function"] = args.noise
  config["noise_delta"] = args.noise_delta
  if args.player_type == "relaxed":
    if args.radius is None:
      parser.error("--radius is required for RelaxedInformationPlayer")
    config["radius"] = args.radius

  start_time = time.time()
  execute(config)
  end_time = time.time()

  execution_time = end_time - start_time
  print(f"Execution time: {execution_time:.2f} seconds")