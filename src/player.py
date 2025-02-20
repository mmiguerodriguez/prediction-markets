from abc import ABC, abstractmethod
import math
import numpy as np
import time

from .rules import calculateScore, f
class Player(ABC):
  def __init__(self, index, weight, rule, p, possiblePredictions):
    self.index = index
    self.weight = weight
    self.rule = rule
    self.p = p
    self.possiblePredictions = possiblePredictions

  def getCurrentPrediction(self, players, predictions):
    if self.index == 0:
      return 0

    result = sum(predictions[i] * players[i].weight for i in range(self.index))
    return result

  @abstractmethod
  def predict(self, players, predictions):
    pass

"""
Jugador de Información Perfecta - de Tomás Schitter

Asume que todos los jugadores tienen información perfecta sobre las predicciones de los demás jugadores 
y que conocen la verdadera probabilidad final del evento.

Sigue la implementación de la tesis de Prediccion de Mercados de Tomás Schitter
"""
class PerfectInformationPlayer(Player):
  def __init__(self, index, weight, rule, p, possiblePredictions):
    super().__init__(index, weight, rule, p, possiblePredictions)

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

"""
Variación del Jugador de Información Perfecta

Asume que la probabilidad recibida "p" está dentro de un cierto radio de la probabilidad verdadera, pero puede no ser la real.
"subset" es el conjunto de posibles probabilidades que el jugador elegirá dentro del radio definido desde el constructor.
- Ejemplo: p = 0.5, radio = 1, posiblesPredicciones = [0.49, 0.5, 0.51]

El método "predict" itera sobre todas las posibles predicciones [0, 0.01, 0.02, ..., 1] y calcula la puntuación para cada una.
En cada paso de la iteración, tomamos un elemento del subconjunto como la probabilidad que va a tomar el siguiente jugador,
y calculamos su predicción en base a este nuevo "p" para el siguiente jugador. Luego, calculamos la puntuación para esta predicción
y la comparamos con la puntuación máxima hasta el momento. Si es mayor, actualizamos la puntuación máxima y la mejor predicción.

Si el jugador es el último, no necesitamos calcular la predicción del siguiente jugador, ya que no hay más jugadores después de él.
En este caso, simplemente calculamos la puntuación para la predicción actual y la comparamos con la puntuación máxima hasta el momento.
"""
class MovingRangePlayer(Player):
  def __init__(self, index, weight, rule, p, possiblePredictions, radius):
    super().__init__(index, weight, rule, p, possiblePredictions)
    self.subset = self.getSubsetWithinRadius(radius)

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

      if self.index == 0:
        print(prediction, currentScore, maxScore)

      if currentScore > maxScore:
        maxScore = currentScore
        bestPrediction = prediction

    return bestPrediction

class UpdatedBeliefsPlayer(Player):
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

      # if self.index == 0:
      #   print(prediction)

    return bestPrediction

def printFile(content):
  with open("out.txt", 'a') as file:
    file.write(content + '\n')