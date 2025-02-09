from abc import ABC, abstractmethod
import math
import numpy as np

from .rules import calculateScore, f
class Player(ABC):
  def __init__(self, index, weight, rule, p, possiblePredictions):
    self.index = index
    self.weight = weight
    self.rule = rule
    self.p = p
    self.possiblePredictions = possiblePredictions

  @abstractmethod
  def predict(self, players, predictions):
    pass

# Implementation of Tomas Schitter PerfectInformationPlayer
# Assumes that all players have perfect information about the other players' predictions
# and that they know the true final probability
class PerfectInformationPlayer(Player):
  def __init__(self, index, weight, rule, p, possiblePredictions):
    super().__init__(index, weight, rule, p, possiblePredictions)

  def getCurrentPrediction(self, players, predictions):
    if self.index == 0:
      return 0

    result = sum(predictions[i] * players[i].weight for i in range(self.index))
    return result

  def predict(self, players, predictions):
    n = len(players)
    _predictions = predictions.copy()
    bestPrediction = 0

    currentPrediction = self.getCurrentPrediction(players, _predictions)
    maxScore = calculateScore(0, f(currentPrediction, self.p), self.rule)

    for prediction in self.possiblePredictions:
      _predictions[self.index] = prediction
      finalPrediction = currentPrediction + (self.weight * prediction)

      if self.index != n - 1:
        for j in range(self.index + 1, n):
          otherPrediction = players[j].predict(players, _predictions) * players[j].weight
          finalPrediction += otherPrediction

      currentScore = calculateScore(prediction, f(finalPrediction, self.p), self.rule)

      if currentScore > maxScore:
        maxScore = currentScore
        bestPrediction = prediction

    return bestPrediction

class MovingRangePlayer(Player):
  def __init__(self, index, weight, rule, p, possiblePredictions, radius):
    super().__init__(index, weight, rule, p, possiblePredictions)
    self.subset = self.getSubsetWithinRadius(radius)

  def getCurrentPrediction(self, players, predictions):
    if self.index == 0:
      return 0

    result = sum(predictions[i] * players[i].weight for i in range(self.index))
    return result

  def getSubsetWithinRadius(self, radius):
    closest_index = np.argmin(np.abs(np.array(self.possiblePredictions) - self.p))

    start_index = max(0, closest_index - radius)
    end_index = min(len(self.possiblePredictions), closest_index + radius + 1)

    subset = self.possiblePredictions[start_index:end_index]

    return subset

  def predict(self, players, predictions):
    n = len(players)
    _predictions = predictions.copy()
    bestPrediction = 0

    currentPrediction = self.getCurrentPrediction(players, _predictions)
    maxScore = calculateScore(0, f(currentPrediction, self.p), self.rule)

    for prediction in self.possiblePredictions:
      _predictions[self.index] = prediction
      finalPrediction = currentPrediction + (self.weight * prediction)

      currentScore = 0
      if self.index != n - 1:
        scores = {}
        for subsetElem in self.subset:
          for j in range(self.index + 1, n):
            original_p = players[j].p
            players[j].p = subsetElem 
            otherPrediction = players[j].predict(players, _predictions) * players[j].weight
            finalPrediction += otherPrediction
            players[j].p = original_p
          
          scores[subsetElem] = calculateScore(prediction, f(finalPrediction, self.p), self.rule)

        maxSubsetElem = max(scores, key=scores.get)
        currentScore = scores[maxSubsetElem]
      else:
        currentScore = calculateScore(prediction, f(finalPrediction, self.p), self.rule)

      if currentScore > maxScore:
        maxScore = currentScore
        bestPrediction = prediction

    return bestPrediction

def printFile(content):
  with open("out.txt", 'a') as file:
    file.write(content + '\n')