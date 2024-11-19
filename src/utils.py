import random

def randomRules(n):
  rules = ["log", "brier", "quadratic"]
  return [random.choice(rules) for _ in range(n)]

def equalRules(n, rule):
  return [rule] * n

def equalWeights(n):
  return [1/n] * n