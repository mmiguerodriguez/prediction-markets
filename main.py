import argparse
import numpy as np
import time

from src.rules import calculateScore
from src.simulation import simulate
from src.player import *
from src.utils import equalRules, equalWeights
from src.results import JSONResultHandler
from src.noise import *

config = {
  "delta": 0.01,
  "deltaQ": 0.05
}

def execute(config):
  filename = config["filename"]
  n = config["n"]
  delta = config["delta"]
  deltaQ = config["deltaQ"]
  player_type = config["player_type"]
  weights = config["weights"]
  rules = config["rules"]

  radius = config["radius"] if player_type != "perfect" else None 
  noise_function = config["noise_function"]
  noise_delta = config["noise_delta"]

  config["rules"] = rules

  q_values = np.arange(0, 1 + deltaQ, deltaQ).round(2).tolist()
  #q_values = [0.1]
  possible_predictions = np.arange(0, 1 + delta, delta).round(2).tolist()

  json_result_handler = JSONResultHandler(filename)

  print(f"Executing simulation...")
  print(f"n = {n}; players = {player_type}; weights = {weights}; rules = {rules}; delta = {delta}; deltaQ = {deltaQ}")
  print(f"noise_function = {noise_function}; noise_delta = {noise_delta};")

  scores_results = []
  predictions_results = []
  final_prediction_results = []
  market_prediction_results = []
  score_results = []

  ps = []
  for q in q_values:
    players = []

    if player_type == "perfect":
      players = [PerfectInformationPlayer(i, weights[i], rules[i], get_noisy_q(q, noise_function, noise_delta), possible_predictions) for i in range(n)]
    elif player_type == "moving_range":
      players = [MovingRangePlayer(i, weights[i], rules[i], get_noisy_q(q, noise_function, noise_delta), possible_predictions, radius) for i in range(n)]

    ps.append([player.p for player in players])

    scores, predictions, final_prediction, market_prediction = simulate(players, q)
    score = calculateScore(market_prediction, final_prediction, "brier")

    scores_results.append(scores)
    predictions_results.append(predictions)
    final_prediction_results.append(final_prediction)
    market_prediction_results.append(market_prediction)
    score_results.append(score)

  config["ps"] = ps

  json_result_handler.write_results(config, scores_results, predictions_results, final_prediction_results, market_prediction_results, score_results)

if __name__ == "__main__":  
  parser = argparse.ArgumentParser(description="Run the prediction market simulation.")

  parser.add_argument("--n", type=int, required=True, help="Number of players")
  parser.add_argument("--player_type", type=str, required=True, choices=["perfect", "moving_range"],
                      help="Type of player to instantiate")
  parser.add_argument("--rules", type=str, nargs='+', required=True, choices=["brier", "log", "quadratic"],
                      help="Valuation functions of players")
  parser.add_argument("--weights", type=float, nargs='+',required=True, help="Weights of players")

  parser.add_argument("--noise", type=str, choices=["identity", "gaussian", "uniform", "sinusoidal", "exponential"],
                      default="identity", help="Noise function")
  parser.add_argument("--noise_delta", type=float, default=0.01, help="Delta for noise function")
  parser.add_argument("--radius", type=int, help="Radius for MovingRangePlayer")
  args = parser.parse_args()

  if args.player_type == "moving_range":
    if args.radius is None:
      parser.error("radius is required for this kind of player")
    config["radius"] = args.radius

  if len(args.rules) != args.n:
    parser.error("The length of rules must be equal to the amount of players")

  if len(args.weights) != args.n:
    parser.error("The length of weights must be equal to the amount of players")
  if not (0.99 <= sum(args.weights) <= 1.01):
    parser.error("The sum of weights must be near 1 (between 0.99 and 1.01)")

  config["date"] = time.strftime("%Y-%m-%d %H:%M:%S")
  config["filename"] = int(time.time())
  config["n"] = args.n
  config["player_type"] = args.player_type
  config["rules"] = args.rules
  config["weights"] = args.weights
  config["noise_function"] = args.noise
  config["noise_delta"] = args.noise_delta

  start_time = time.time()
  execute(config)
  end_time = time.time()

  execution_time = end_time - start_time
  print(f"Execution time: {execution_time:.2f} seconds")
  print(f"Filename: {config["filename"]}.json")