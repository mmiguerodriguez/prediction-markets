'''
En este archivo implementamos una simulacion de predicciones secuenciales con informacion perfecta.
'''

import numpy as np
import random
import math
import csv

menosInfinito = -math.inf
c = 0.1

def logRule(p,q):
  if ((p == 0 or p == 1) and q != 0 and q != 1):
    return menosInfinito
  elif (q == p and (q == 0 or q == 1)):
    return 0
  return round((q * np.log(p) + (1 - q) * np.log((1 - p))), 4)

def brierRule(p,q):
  return -(q * ((1 - p) ** 2) + (1 - q) * (p ** 2))

def quadraticError(p, q):
  return -((p - q) ** 2)

def f(p, q):
  return round((c * p + (1 - c) * q), 2)

def randomRules(N):
  rules = ["log", "brier", "quadratic"]
  return [random.choice(rules) for _ in range(N)]

def equalRules(N, regla):
  return [regla] * N

def calculateScore(p_i, realFinalProbability, rule):
  if rule == "log":
    return logRule(p_i, realFinalProbability)
  elif rule == "brier":
    return brierRule(p_i, realFinalProbability)
  else:
    return quadraticError(p_i, realFinalProbability)

def calculateBestPrediction(i, currentPrediction, weights, rules, N, q, predictionValues):
  # Si estoy en el ultimo jugador, es mi caso base (induccion hacia atras)
  if i == N - 1:
    prediction = 0
    bestPrediction = 0
    maxScore = calculateScore(0, f(currentPrediction, q), rules[i])

    for _prediction in predictionValues:
      prediction = float(_prediction)
      finalPrediction = currentPrediction + (weights[i] * prediction)
      currentScore = calculateScore(prediction, f(finalPrediction, q), rules[i])

      if currentScore > maxScore:
        maxScore = currentScore
        bestPrediction = prediction

    return bestPrediction
  else:
    prediction = 0
    finalPrediction = currentPrediction

    # seteo inicialmente el maximo puntaje en lo obtenido al predecir 0
    for j in range (i + 1, N):
      finalPrediction += calculateBestPrediction(j, finalPrediction, weights, rules, N, q, predictionValues) * weights[j]

    maxScore = calculateScore(0, f(finalPrediction, q), rules[i])
    bestPrediction = 0

    for _prediction in predictionValues:
      prediction = float(_prediction)
      finalPrediction = currentPrediction + (weights[i] * prediction)
      for j in range (i + 1, N):
        finalPrediction += calculateBestPrediction(j, finalPrediction, weights, rules, N, q, predictionValues) * weights[j]

      currentScore = calculateScore(prediction, f(finalPrediction, q), rules[i])

      if currentScore > maxScore:
        maxScore = currentScore
        bestPrediction = prediction

    return bestPrediction

# N = cantidad de jugadores
# weights = [w_1, ..., w_n], el peso de la prediccion de cada jugador en la prediccion final del mercado
# delta = precision permitida en las predicciones
# q = probabilidad a priori del evento
def simulate(N, weights, predictionValues, q):
  rules = equalRules(N, "brier")
  scores = [0] * N
  predictions = []
  currentPrediction = 0

  for i in range (0, N):
    p = calculateBestPrediction(i, currentPrediction, weights, rules, N, q, predictionValues)
    predictions.append(p)
    currentPrediction += p * weights[i]

  marketPrediction = 0
  for i in range(0, N):
    marketPrediction += weights[i] * predictions[i]

  finalPrediction = f(marketPrediction, q)
  for i in range(0, N):
    scores[i] = calculateScore(predictions[i], finalPrediction, rules[i])

  return scores, predictions, finalPrediction, marketPrediction

def execute(n):
  with open("results/scores.csv", "w", newline='') as scores, open("results/predictions.csv", "w", newline='') as predictions:
    scores_writer = csv.writer(scores)
    predictions_writer = csv.writer(predictions)
    
    # Dynamic header
    scores_header = ['q'] + [f'p{i+1}' for i in range(n)] + ['market']
    predictions_header = ['q'] + [f'p{i+1}' for i in range(n)] + ['market', 'final']
    scores_writer.writerow(scores_header)
    predictions_writer.writerow(predictions_header)
    
    # Experiment Config
    weights = [1/n] * n
    delta = 0.01
    deltaQ = 0.05

    qValues = np.arange(0, 1 + deltaQ, deltaQ).round(2).tolist()
    predictionValues = np.arange(0, 1 + delta, delta).round(2).tolist()

    for q in qValues:
      scores, predictions, finalPrediction, marketPrediction = simulate(n, weights, predictionValues, q)

      score_row = [f'{q:.2f}'] + [f'{round(puntaje, 4):.4f}' for puntaje in scores] + [f'{calculateScore(marketPrediction, finalPrediction, "brier"):.4f}']
      prediction_row = [f'{q:.2f}'] + [f'{round(prediccion, 2):.2f}' for prediccion in predictions] + [f'{round(marketPrediction, 2):.2f}', f'{round(finalPrediction, 2):.2f}']      
      scores_writer.writerow(score_row)
      predictions_writer.writerow(prediction_row)

execute(n=2)
