from abc import ABC, abstractmethod
import random

from .rules import calculateScore, f
class Player(ABC):
  def __init__(self, index, weight, rule, expectedProbabilityValues):
    self.index = index
    self.weight = weight
    self.rule = rule
    self.expectedProbabilityValues = expectedProbabilityValues

  @abstractmethod
  def predict(self, currentPrediction, players, q):
    pass

# Implementation of Tomas Schitter PerfectInformationPlayer
class PerfectInformationPlayer(Player):
  def predict(self, currentPrediction, players, q):
    n = len(players)

    if self.index == n - 1:
      prediction = 0
      bestPrediction = 0
      maxScore = calculateScore(0, f(currentPrediction, q), self.rule)

      for _prediction in self.possiblePredictions:
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

      for _prediction in self.possiblePredictions:
        prediction = float(_prediction)
        finalPrediction = currentPrediction + (self.weight * prediction)
        for j in range(self.index + 1, n):
          finalPrediction += players[j].predict(finalPrediction, players, q) * players[j].weight

        currentScore = calculateScore(prediction, f(finalPrediction, q), self.rule)

        if currentScore > maxScore:
          maxScore = currentScore
          bestPrediction = prediction

      return bestPrediction

class BruteForcePlayer(Player):
  def predict(self, currentPrediction, players, q):
    n = len(players)
    bestPrediction = 0
    maxScore = -float('inf')

    for _prediction in self.expectedProbabilityValues:
      prediction = float(_prediction)
      finalPrediction = currentPrediction + (self.weight * prediction)

      # Assume other players (after me) have the same belief
      for j in range(self.index + 1, n):
        finalPrediction += players[j].weight * prediction

      currentScore = calculateScore(prediction, f(finalPrediction, q), self.rule)

      if currentScore > maxScore:
        maxScore = currentScore
        bestPrediction = prediction

    return bestPrediction

class RandomPredictionPlayer(Player):
  def predict(self, currentPrediction, players, q):
    return random.choice(self.expectedProbabilityValues)

class ConservativePlayer(Player):
  def predict(self, currentPrediction, players, q):
    return min(self.expectedProbabilityValues, key=lambda x: abs(x - currentPrediction))

class AggressivePlayer(Player):
  def predict(self, currentPrediction, players, q):
    return max(self.expectedProbabilityValues) if random.random() > 0.5 else min(self.expectedProbabilityValues)

class TrendFollowingPlayer(Player):
  def predict(self, currentPrediction, players, q):
    if self.index == 0:
      return random.choice(self.expectedProbabilityValues)

    previous_prediction = players[self.index - 1].predict(currentPrediction, players, q)
    trend = previous_prediction - currentPrediction
    return min(self.expectedProbabilityValues, key=lambda x: abs(x - (currentPrediction + trend)))