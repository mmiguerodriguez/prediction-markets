import numpy as np
import csv
import json
import time

from src.rules import calculateScore
from src.simulation import simulate
from src.player import PerfectInformationPlayer
from src.utils import equalRules, equalWeights

def execute(config):
  ts = int(time.time())

  # Experiment Config
  n = config["n"]
  delta = config["delta"]
  deltaQ = config["deltaQ"]
  weights = equalWeights(n)
  rules = equalRules(n, "brier")
  print(f"n = {n}\ndelta = {delta}\ndeltaQ = {deltaQ}\nweights = {weights}\nrules = {rules}")

  qValues = np.arange(0, 1 + deltaQ, deltaQ).round(2).tolist()
  predictionValues = np.arange(0, 1 + delta, delta).round(2).tolist()

  players = [PerfectInformationPlayer(i, weights[i], rules[i], predictionValues) for i in range(n)]

  with open(f"results/scores-{n}-{delta}-{deltaQ}-{ts}.csv", "w", newline='') as scores_file, open(f"results/predictions-{n}-{delta}-{deltaQ}-{ts}.csv", "w", newline='') as predictions_file:
    scores_writer = csv.writer(scores_file)
    predictions_writer = csv.writer(predictions_file)
    
    # Dynamic header
    scores_header = ['q'] + [f'p{i+1}' for i in range(n)] + ['market']
    predictions_header = ['q'] + [f'p{i+1}' for i in range(n)] + ['market', 'final']
    scores_writer.writerow(scores_header)
    predictions_writer.writerow(predictions_header)

    for q in qValues:
      scores, predictions, finalPrediction, marketPrediction = simulate(players, q)

      score_row = [f'{q:.2f}'] + [f'{round(puntaje, 4):.4f}' for puntaje in scores] + [f'{calculateScore(marketPrediction, finalPrediction, "brier"):.4f}']
      prediction_row = [f'{q:.2f}'] + [f'{round(prediccion, 2):.2f}' for prediccion in predictions] + [f'{round(marketPrediction, 2):.2f}', f'{round(finalPrediction, 2):.2f}']      
      scores_writer.writerow(score_row)
      predictions_writer.writerow(prediction_row)

if __name__ == "__main__":
  with open("config.json", "r") as config_file:
    config = json.load(config_file)
  
  execute(config)