from .rules import calculateScore, f
import time
from concurrent.futures import ProcessPoolExecutor

def simulate(players, q):
  predictions = [0 for _ in range(len(players))]

  for player in players:
    start_time = time.time()

    p = player.predict(players, predictions.copy())
    predictions[player.index] = p

    end_time = time.time()
    execution_time = end_time - start_time
    print(f"p{player.index} - prediction time: {execution_time:.2f} seconds")

  print(f"q: {q} - p: {', '.join([str(player.p) for player in players])}; predictions: {predictions}")

  marketPrediction = sum(player.weight * predictions[i] for i, player in enumerate(players))
  finalPrediction = f(marketPrediction, q)
  scores = [calculateScore(predictions[i], finalPrediction, player.rule) for i, player in enumerate(players)]

  return scores, predictions, finalPrediction, marketPrediction