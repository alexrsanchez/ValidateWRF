import numpy as np
import xarray

def calculate_statistics(obs_array, model_array):
    # 1. RMSE
    series_diff = obs_array - model_array
    rmse = ((series_diff**2).sum(dim='time')/len(obs_array.time))**0.5

    # 2. Bias
    bias = (series_diff.sum(dim='time'))/len(series_diff.time)

    # 3. MAE
    mae = (abs(series_diff)).sum(dim='time')/len(series_diff.time)
    return rmse, bias, mae
