import numpy as np
import math

c = 0.1

def logRule(p, q):
  if ((p == 0 or p == 1) and q != 0 and q != 1):
    return -math.inf
  elif (q == p and (q == 0 or q == 1)):
    return 0
  return round((q * np.log(p) + (1 - q) * np.log(1 - p)), 4)

def brierRule(p, q):
  return -(q * ((p - 1) ** 2) + (1 - q) * (p ** 2))

def quadraticError(p, q):
  return -((p - q) ** 2)

def f(p, q):
  return round((c * p + (1 - c) * q), 2)

def calculateScore(p_i, q, rule):
  if rule == "log":
    return logRule(p_i, q)
  elif rule == "brier":
    return brierRule(p_i, q)
  else:
    return quadraticError(p_i, q)