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

# Implementation of a modified PerfectInformationPlayer
# Assumes all players predict within a certain radius of their p
# Doesn't have assumptions regarding if our p is the real one or not
class RelaxedInformationPlayer(Player):
  def __init__(self, index, weight, rule, p, possiblePredictions, radius):
    super().__init__(index, weight, rule, p, possiblePredictions)
    self.subset = self.getSubsetWithinRadius(radius)
    print(self.subset)

  def getCurrentPrediction(self, players, predictions):
    if self.index == 0:
      return 0

    result = sum(predictions[i] * players[i].weight for i in range(self.index))
    return result

  # Get a subset of possible predictions within a radius of the current p
  # Example: p = 0.4, radius = 1
  # Returns: [0.39, 0.4, 0.41]
  def getSubsetWithinRadius(self, radius):
    closest_index = np.argmin(np.abs(np.array(self.possiblePredictions) - self.p))

    start_index = max(0, closest_index - radius)
    end_index = min(len(self.possiblePredictions), closest_index + radius + 1)

    subset = self.possiblePredictions[start_index:end_index]

    return subset

  def predict(self, players, predictions, top_level=True):
    n = len(players)
    _predictions = predictions.copy()
    bestPrediction = 0

    if self.index == n - 1:
      currentPrediction = self.getCurrentPrediction(players, _predictions)
      maxScore = calculateScore(0, f(currentPrediction, self.p), self.rule)

      possiblePredictions = self.possiblePredictions
      if not top_level:
        possiblePredictions = self.subset

      for prediction in possiblePredictions:
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

      possiblePredictions = self.possiblePredictions
      if not top_level:
        possiblePredictions = self.subset
      
      for prediction in possiblePredictions:
        _predictions[self.index] = prediction
        finalPrediction = currentPrediction + (self.weight * prediction)

        for j in range(self.index + 1, n):
          otherPrediction = players[j].predict(players, _predictions, top_level=False) * players[j].weight
          finalPrediction += otherPrediction

        currentScore = calculateScore(prediction, f(finalPrediction, self.p), self.rule)

        if currentScore > maxScore:
          maxScore = currentScore
          bestPrediction = prediction

      return bestPrediction

"""
Cambiar MAXSCORE por:
Si no todos tienen la probabilidad real
Asumiendo que el otro va a tener un p (subjetivo) a cierta distancia del mío, hago el promedio
(asumiendo que esa persona/jugador tiene radio de probabilidad 0.51, 0.5, 0.49)
calculo el movimiento que va a hacer dentro de ese radio
variando la creencia

- Creencia: El p del otro está a cierto rango del mio (mirar esas probabilidades)
- Promediar el puntaje que obtendría tomando la decisión óptima

Experimento:
Tengo p=0.4. No se que piensa el otro, supongo [0.3, 0.6], asumir que la probabilidad de que
esté entre esos números es uniforme (puede ser normal). Si doy la predicción de este número, 
que puntaje obtendría?

No sé cual es la probabilidad subjetiva del siguiente
que los jugadores tengan una creencia de un rango en el que puedan estar todos

Experimento 2:
La mismo estrategia, utilizando la regla logarítmica
"""
class AverageCalculationPlayer(Player):
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
    
# Remove assumptions
# Make the model look more like a real scenario
