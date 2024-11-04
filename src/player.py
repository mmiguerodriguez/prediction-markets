from .rules import calculateScore, f

class PerfectInformationPlayer:
  def __init__(self, index, weight, rule, predictionValues):
    self.index = index
    self.weight = weight
    self.rule = rule
    self.predictionValues = predictionValues

  def predict(self, currentPrediction, players, q):
    n = len(players)

    if self.index == n - 1:
      prediction = 0
      bestPrediction = 0
      maxScore = calculateScore(0, f(currentPrediction, q), self.rule)

      for _prediction in self.predictionValues:
        prediction = float(_prediction)
        finalPrediction = currentPrediction + (self.weight * prediction)
        currentScore = calculateScore(prediction, f(finalPrediction, q), self.rule)

        if currentScore > maxScore:
          maxScore = currentScore
          bestPrediction = prediction

      return bestPrediction
    else:
      prediction = 0
      finalPrediction = currentPrediction

      for j in range(self.index + 1, n):
        finalPrediction += players[j].predict(finalPrediction, players, q) * players[j].weight

      maxScore = calculateScore(0, f(finalPrediction, q), self.rule)
      bestPrediction = 0

      for _prediction in self.predictionValues:
        prediction = float(_prediction)
        finalPrediction = currentPrediction + (self.weight * prediction)
        for j in range(self.index + 1, n):
          finalPrediction += players[j].predict(finalPrediction, players, q) * players[j].weight

        currentScore = calculateScore(prediction, f(finalPrediction, q), self.rule)

        if currentScore > maxScore:
          maxScore = currentScore
          bestPrediction = prediction

      return bestPrediction
