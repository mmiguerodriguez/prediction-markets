import numpy as np

def identity(q):
  return q

def add_gaussian_noise(q, epsilon):
  """
  Add Gaussian noise to the q value.
  """
  noise = np.random.normal(0, epsilon)
  noisy_q = q + noise
  return np.clip(noisy_q, 0, 1).round(2)

def add_uniform_noise(q, epsilon):
  """
  Add uniform noise to the q value.
  """
  noise = np.random.uniform(-epsilon, epsilon)
  noisy_q = q + noise
  return np.clip(noisy_q, 0, 1).round(2)

def add_sinusoidal_noise(q, epsilon, frequency=1.0):
  """
  Add sinusoidal noise to the q value.
  """
  noise = epsilon * np.sin(2 * np.pi * frequency * q)
  noisy_q = q + noise
  return np.clip(noisy_q, 0, 1).round(2)

def add_exponential_noise(q, epsilon):
  """
  Add exponential noise to the q value.
  """
  noise = np.random.exponential(epsilon)
  noisy_q = q + noise
  return np.clip(noisy_q, 0, 1).round(2)

# Example usage
# q = 0.5
# epsilon = 0.05

# noisy_q_gaussian = add_gaussian_noise(q, epsilon)
# noisy_q_uniform = add_uniform_noise(q, epsilon)
# noisy_q_sinusoidal = add_sinusoidal_noise(q, epsilon)
# noisy_q_exponential = add_exponential_noise(q, epsilon)

# print(f"Original q: {q}")
# print(f"Noisy q (Gaussian): {noisy_q_gaussian}")
# print(f"Noisy q (Uniform): {noisy_q_uniform}")
# print(f"Noisy q (Sinusoidal): {noisy_q_sinusoidal}")
# print(f"Noisy q (Exponential): {noisy_q_exponential}")