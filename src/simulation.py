from .rules import calculateScore, f

def simulate(players, q):
  predictions = [0 for _ in range(len(players))]

  for player in players:
    p = player.predict(players, predictions.copy()) #, q)
    predictions[player.index] = p

  print(f"q: {q} - p: {', '.join([str(player.p) for player in players])}; predictions: {predictions}")

  marketPrediction = sum(player.weight * predictions[i] for i, player in enumerate(players))
  finalPrediction = f(marketPrediction, q)
  scores = [calculateScore(predictions[i], finalPrediction, player.rule) for i, player in enumerate(players)]

  return scores, predictions, finalPrediction, marketPrediction