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
  ts = int(time.time())

  # Experiment Config
  n = config["n"]
  delta = config["delta"]
  deltaQ = config["deltaQ"]
  playerType = config["playerType"]
  
  weights = equalWeights(n)
  rules = equalRules(n, "brier")
  qValues = np.arange(0, 1 + deltaQ, deltaQ).round(2).tolist()
  possiblePredictions = np.arange(0, 1 + delta, delta).round(2).tolist()

  filename = f"{playerType}-{n}-{delta}-{deltaQ}"
  result_handler = CSVResultHandler(filename, n)
  result_handler.write_headers()

  print(f"Executing simulation...")
  print(f"n = {n}")
  print(f"players = {playerType}")
  print(f"weights = {weights}")
  print(f"rules = {rules}")
  print(f"delta = {delta}")
  print(f"deltaQ = {deltaQ}")
  # print(f"q = {q};")
  # print(f"{'\n'.join([f'{player.__class__.__name__} ({player.p}) ({player.rule}) ({player.weight:.2f})' for player in players])}")

  for q in qValues:
    players = []

    p = identity(q)
    if playerType == "RelaxedInformationPlayer":
      
      players = [RelaxedInformationPlayer(i, weights[i], rules[i], p, possiblePredictions, config["radius"]) for i in range(n)]
    elif playerType == "PerfectInformationPlayer":
      players = [PerfectInformationPlayer(i, weights[i], rules[i], p, possiblePredictions) for i in range(n)]

    scores, predictions, finalPrediction, marketPrediction = simulate(players, q)
    result_handler.write_results(q, scores, predictions, finalPrediction, marketPrediction, calculateScore(marketPrediction, finalPrediction, "brier"))

if __name__ == "__main__":
  # with open("config.json", "r") as config_file:
  #   config = json.load(config_file)
  
  config["n"] = int(input("n: "))
  config["playerType"] = input("Player type (RelaxedInformationPlayer or PerfectInformationPlayer): ")
  if config["playerType"] == "RelaxedInformationPlayer":
    config["radius"] = int(input("radius: "))

  start_time = time.time()
  execute(config)
  end_time = time.time()

  execution_time = end_time - start_time
  print(f"Execution time: {execution_time:.2f} seconds")