import csv

class CSVResultHandler:
  def __init__(self, n, delta, deltaQ, ts):
    self.n = n
    self.delta = delta
    self.deltaQ = deltaQ
    self.ts = ts
    self.scores_file = f"results/{n}-{delta}-{deltaQ}-{ts}-scores.csv"
    self.predictions_file = f"results/{n}-{delta}-{deltaQ}-{ts}-predictions.csv"

  def write_headers(self):
    with open(self.scores_file, "w", newline='') as scores_file, open(self.predictions_file, "w", newline='') as predictions_file:
      scores_writer = csv.writer(scores_file)
      predictions_writer = csv.writer(predictions_file)
      
      scores_header = ['q'] + [f'p{i+1}' for i in range(self.n)] + ['market']
      predictions_header = ['q'] + [f'p{i+1}' for i in range(self.n)] + ['market', 'final']
      scores_writer.writerow(scores_header)
      predictions_writer.writerow(predictions_header)

  def write_results(self, q, scores, predictions, finalPrediction, marketPrediction, score):
    with open(self.scores_file, "a", newline='') as scores_file, open(self.predictions_file, "a", newline='') as predictions_file:
      scores_writer = csv.writer(scores_file)
      predictions_writer = csv.writer(predictions_file)

      score_row = [f'{q:.2f}'] + [f'{round(score, 4):.4f}' for score in scores] + [f'{score:.4f}']
      prediction_row = [f'{q:.2f}'] + [f'{round(prediction, 2):.2f}' for prediction in predictions] + [f'{round(marketPrediction, 2):.2f}', f'{round(finalPrediction, 2):.2f}']

      scores_writer.writerow(score_row)
      predictions_writer.writerow(prediction_row)
