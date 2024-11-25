import numpy as np
import time

from src.rules import calculateScore
from src.simulation import simulate
from src.player import *
from src.utils import equalRules, equalWeights
from src.results import CSVResultHandler
from src.noise import *

config = {
  "n": 2,
  "delta": 0.01,
  "deltaQ": 0.05
}

def execute(config):
  ts = int(time.time())

  # Experiment Config
  n = config["n"]
  delta = config["delta"]
  deltaQ = config["deltaQ"]
  weights = equalWeights(n)
  rules = equalRules(n, "brier")
  print(f"n = {n}\ndelta = {delta}\ndeltaQ = {deltaQ}")

  qValues = np.arange(0, 1 + deltaQ, deltaQ).round(2).tolist()
  possiblePredictions = np.arange(0, 1 + delta, delta).round(2).tolist()

  result_handler = CSVResultHandler(n, delta, deltaQ, ts)
  result_handler.write_headers()
  for q in qValues:
    p = add_uniform_noise(q, 0.025)
    players = [PerfectInformationPlayer(i, weights[i], rules[i], p, possiblePredictions) for i in range(n)]
    print(f"players = {', '.join([f'{player.__class__.__name__} ({p}) ({player.rule}) ({player.weight})' for player in players])}")

    scores, predictions, finalPrediction, marketPrediction = simulate(players, q)
    result_handler.write_results(q, scores, predictions, finalPrediction, marketPrediction, calculateScore(marketPrediction, finalPrediction, "brier"))

if __name__ == "__main__":
  # with open("config.json", "r") as config_file:
  #   config = json.load(config_file)
  
  execute(config)