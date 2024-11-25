from .rules import calculateScore, f

def simulate(players, q):
  predictions = [0 for _ in range(len(players))]

  for player in players:
    p = player.predict(players, predictions.copy())
    predictions[player.index] = p

  marketPrediction = sum(player.weight * predictions[i] for i, player in enumerate(players))
  finalPrediction = f(marketPrediction, q)
  scores = [calculateScore(predictions[i], finalPrediction, player.rule) for i, player in enumerate(players)]

  return scores, predictions, finalPrediction, marketPrediction