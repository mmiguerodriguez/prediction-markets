import numpy as np
import math

c = 0.1
log_map = {float(round(i, 2)): float(round(np.log(i), 4)) if i != 0 else -math.inf for i in np.arange(0, 1.01, 0.01)}
log_map_1_minus = {float(round(i, 2)): float(round(np.log(1 - i), 4)) if i != 1 else -math.inf for i in np.arange(0, 1.01, 0.01)}

def logRule(p, q):
  if ((p == 0 or p == 1) and q != 0 and q != 1):
    return -math.inf
  elif (q == p and (q == 0 or q == 1)):
    return 0
  # return round((q * np.log(p) + (1 - q) * np.log(1 - p)), 4)
  return round((q * log_map[p] + (1 - q) * log_map_1_minus[p]), 4)

def brierRule(p, q):
  return -(q * ((p - 1) ** 2) + (1 - q) * (p ** 2))

def quadraticError(p, q):
  return -((p - q) ** 2)

def f(p, q):
  return round((c * p + (1 - c) * q), 2)

def calculateScore(p_i, q, rule):
  score = 0
  if rule == "log":
    score = logRule(p_i, q)
  elif rule == "brier":
    score = brierRule(p_i, q)
  else:
    score = quadraticError(p_i, q)
  return round(score, 4)
  # return score