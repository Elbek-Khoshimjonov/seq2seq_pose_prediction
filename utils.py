import numpy as np
import torch
import pandas as pd

def load_dataset(path="dev2.pkl"):
  # Load pandas
  df = pd.read_pickle(path)
  # Train, val and test split
  count = len(df)
  train_count = int(0.8 * count)
  val_count = int(0.1 * count)

  # Pandas split
  train_df = df[:train_count]
  val_df = df[train_count: train_count+val_count]
  test_df = df[train_count+val_count:]

  print("Train: %d, val: %d, test: %d\n" % (len(train_df), len(val_df), len(test_df)))

  return train_df, val_df, test_df


def preprocess(df):

  x = []
  y = []
  for _, row in df.iterrows():
    data = row["data"]
    for i in range(len(data)-150):
      x.append( np.copy(data[i : i+75]) )
      y.append( np.copy(data[i+75 : i+150]) )

  x = np.asarray(x)
  x[:, :, :, 0] = (x[:, :, :, 0] - 960.0)/960.0
  x[:, :, :, 1] = (x[:, :, :, 1] - 540.0)/540.0

  y = np.asarray(y)
  y[:, :, :, 0] = (y[:, :, :, 0] - 960.0)/960.0
  y[:, :, :, 1] = (y[:, :, :, 1] - 540.0)/540.0
  
  return x, y

def custom_loss(y_true, y_pred):

  diff = y_true - y_pred
  diff = torch.sum(diff*diff, -1)
  diff = torch.sqrt(diff)
  return torch.mean(diff) * np.sqrt(1920**2+1080**2)

def distance(y_true, y_pred):

  diff = y_true - y_pred
  diff = np.sum(np.square(diff), axis=-1)
  diff = np.sqrt(diff)
  return np.mean(diff) * np.sqrt(1920**2+1080**2)
