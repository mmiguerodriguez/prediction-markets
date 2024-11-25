from abc import ABC, abstractmethod
import math
import random

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
class PerfectInformationPlayer(Player):
  def getCurrentPrediction(self, players, predictions):
    if self.index == 0:
      return 0

    result = sum(predictions[i] * players[i].weight for i in range(self.index))
    return result

  def predict(self, players, predictions):
    n = len(players)
    _predictions = predictions.copy()
    bestPrediction = 0

    if self.index == n - 1:
      currentPrediction = self.getCurrentPrediction(players, _predictions)
      maxScore = calculateScore(0, f(currentPrediction, self.p), self.rule)

      for prediction in self.possiblePredictions:
        _predictions[self.index] = prediction
        finalPrediction = currentPrediction + (self.weight * prediction)
        currentScore = calculateScore(prediction, f(finalPrediction, self.p), self.rule)

        if currentScore > maxScore:
          maxScore = currentScore
          bestPrediction = prediction

      return bestPrediction
    else:
      currentPrediction = self.getCurrentPrediction(players, _predictions)
      maxScore = calculateScore(0, f(currentPrediction, self.p), self.rule)

      for prediction in self.possiblePredictions:
        _predictions[self.index] = prediction
        finalPrediction = currentPrediction + (self.weight * prediction)

        for j in range(self.index + 1, n):
          otherPrediction = players[j].predict(players, _predictions) * players[j].weight
          finalPrediction += otherPrediction

        currentScore = calculateScore(prediction, f(finalPrediction, self.p), self.rule)

        if currentScore > maxScore:
          maxScore = currentScore
          bestPrediction = prediction

      return bestPrediction

class NaivePlayer(Player):
  def getCurrentPrediction(self, players, predictions):
    if self.index == 0:
      return 0
    
    result = sum(predictions[i] * players[i].weight for i in range(self.index))
    return result

  def predict(self, players, predictions, q):
    n = len(players)
    bestPrediction = 0
    maxScore = -math.inf

    for prediction in self.possiblePredictions:
      finalPrediction = self.getCurrentPrediction(players, predictions) + (self.weight * prediction)

      for j in range(self.index + 1, n):
        finalPrediction += players[j].weight * prediction

      currentScore = calculateScore(prediction, f(finalPrediction, q), self.rule)

      if currentScore > maxScore:
        maxScore = currentScore
        bestPrediction = prediction

    return bestPrediction

# class RandomPredictionPlayer(Player):
#   def predict(self, currentPrediction, players, q):
#     return random.choice(self.possiblePredictions)

# class ConservativePlayer(Player):
#   def predict(self, currentPrediction, players, q):
#     return min(self.possiblePredictions, key=lambda x: abs(x - currentPrediction))

# class AggressivePlayer(Player):
#   def predict(self, currentPrediction, players, q):
#     return max(self.possiblePredictions) if random.random() > 0.5 else min(self.possiblePredictions)

# class TrendFollowingPlayer(Player):
#   def predict(self, currentPrediction, players, q):
#     if self.index == 0:
#       return random.choice(self.possiblePredictions)

#     previous_prediction = players[self.index - 1].predict(currentPrediction, players, q)
#     trend = previous_prediction - currentPrediction
#     return min(self.possiblePredictions, key=lambda x: abs(x - (currentPrediction + trend)))
