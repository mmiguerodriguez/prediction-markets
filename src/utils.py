import random

def randomRules(n):
  rules = ["log", "brier", "quadratic"]
  return [random.choice(rules) for _ in range(n)]

def equalRules(n, regla):
  return [regla] * n

def equalWeights(n):
  return [1/n] * n