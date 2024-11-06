import numpy as np
from .player import PerfectInformationPlayer
from .rules import calculateScore, f

def simulate(players, q):
  n = len(players)

  predictions = []
  currentPrediction = 0
  for player in players:
    p = player.predict(currentPrediction, players, q)
    predictions.append(p)
    currentPrediction += p * player.weight

  marketPrediction = sum(player.weight * predictions[i] for i, player in enumerate(players))
  finalPrediction = f(marketPrediction, q)
  scores = [calculateScore(predictions[i], finalPrediction, player.rule) for i, player in enumerate(players)]

  return scores, predictions, finalPrediction, marketPrediction