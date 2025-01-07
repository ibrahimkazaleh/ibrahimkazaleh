import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

path_file = r"../../../src/features"
import sys
sys.path.append(path_file)

from DataTransformation import LowPassFilter, PrincipalComponentAnalysis
from TemporalAbstraction import NumericalAbstraction
from sklearn.cluster import KMeans
import TemporalAbstraction  
from FrequencyAbstracktion import FourierTransformation


def build_features(input_df):
    """
    Function to process raw sensor data and build features for machine learning.
    
    Args:
        input_df (pd.DataFrame): DataFrame containing raw sensor data with columns:
                                ['acc_x', 'acc_y', 'acc_z', 'gyr_x', 'gyr_y', 'gyr_z', 'time', 'set'].
    
    Returns:
        pd.DataFrame: DataFrame with features extracted from the input data.
    """
    df = input_df.copy()
    predictor_columns = ['acc_x', 'acc_y', 'acc_z', 'gyr_x', 'gyr_y', 'gyr_z']

    # --------------------------------------------------------------
    # Dealing with missing values (imputation)
    # --------------------------------------------------------------
    for col in predictor_columns:
        df[col] = df[col].interpolate()

    # --------------------------------------------------------------
    # Butterworth lowpass filter
    # --------------------------------------------------------------
    low_pass = LowPassFilter()
    fs = 1000 / 200
    cutoff = 1.3

    for col in predictor_columns:
        df = low_pass.low_pass_filter(df, col, fs, cutoff, order=5)
        df[col] = df[col + '_lowpass']
        del df[col + '_lowpass']

    # --------------------------------------------------------------
    # Principal component analysis PCA
    # --------------------------------------------------------------
    pca = PrincipalComponentAnalysis()
    df = pca.apply_pca(df, predictor_columns, 3)

    # --------------------------------------------------------------
    # Sum of squares attributes
    # --------------------------------------------------------------
    df['acc_r'] = np.sqrt(df['acc_x'] ** 2 + df['acc_y'] ** 2 + df['acc_z'] ** 2)
    df['gyr_r'] = np.sqrt(df['gyr_x'] ** 2 + df['gyr_y'] ** 2 + df['gyr_z'] ** 2)

    # --------------------------------------------------------------
    # Temporal abstraction
    # --------------------------------------------------------------
    num_abs = NumericalAbstraction()
    window_size = int(1000 / 200)
    temporal_columns = predictor_columns + ['acc_r', 'gyr_r']

    df_temporal_list = []
    for s in df['set'].unique():
        subset = df[df['set'] == s].copy()
        for col in temporal_columns:
            num_abs.abstract_numerical(subset, [col], window_size, 'mean')
            num_abs.abstract_numerical(subset, [col], window_size, 'std')
        df_temporal_list.append(subset)

    df = pd.concat(df_temporal_list)

    # --------------------------------------------------------------
    # Frequency features
    # --------------------------------------------------------------
    freq_abs = FourierTransformation()
    fs = int(2800 / 200)
    freq_columns = temporal_columns

    df_freq_list = []
    for s in df['set'].unique():
        subset = df[df['set'] == s].reset_index(drop=True).copy()
        freq_abs.abstract_frequency(subset, freq_columns, 6, fs)
        df_freq_list.append(subset)

    df = pd.concat(df_freq_list).set_index("epoch (ms)", drop=True)

    # --------------------------------------------------------------
    # Dealing with overlapping windows
    # --------------------------------------------------------------
    df = df.dropna()
    df = df.iloc[::2]  # Downsampling

    return df

import pandas as pd
import numpy as np

# إنشاء بيانات محاكاة للحساسات
np.random.seed(42)  # لضمان ثبات النتائج
rows = 500  # عدد الصفوف

# إنشاء الأعمدة
data = {
    "epoch (ms)": pd.date_range(start="2024-01-01", periods=rows, freq="200ms"),
    "acc_x": np.random.uniform(-10, 10, rows),
    "acc_y": np.random.uniform(-10, 10, rows),
    "acc_z": np.random.uniform(-10, 10, rows),
    "gyr_x": np.random.uniform(-500, 500, rows),
    "gyr_y": np.random.uniform(-500, 500, rows),
    "gyr_z": np.random.uniform(-500, 500, rows),
    "set": [1] * 250 + [2] * 250,  # مجموعة افتراضية للتمارين
    "label": ["exercise1"] * 250 + ["exercise2"] * 250  # أسماء التمارين
}

# إنشاء DataFrame
# df_test = pd.DataFrame(data)


# df = pd.DataFrame([{
#             "acc_x": data.acc_x,
#             "acc_y": data.acc_y,
#             "acc_z": data.acc_z,
#             "gyr_x": data.gyr_x,
#             "gyr_y": data.gyr_y,
#             "gyr_z": data.gyr_z,
#             "time": data.time
#         }])

# build_features(df_test.iloc(1))

# ---------------





# df = df_test.copy()
# predictor_columns = ['acc_x', 'acc_y', 'acc_z', 'gyr_x', 'gyr_y', 'gyr_z']

# # --------------------------------------------------------------
# # Dealing with missing values (imputation)
# # --------------------------------------------------------------
# for col in predictor_columns:
#     df[col] = df[col].interpolate()

# # --------------------------------------------------------------
# # Butterworth lowpass filter
# # --------------------------------------------------------------
# low_pass = LowPassFilter()
# fs = 1000 / 200
# cutoff = 1.3

# for col in predictor_columns:
#     df = low_pass.low_pass_filter(df, col, fs, cutoff, order=5)
#     df[col] = df[col + '_lowpass']
#     del df[col + '_lowpass']

#     # --------------------------------------------------------------
#     # Principal component analysis PCA
#     # --------------------------------------------------------------
# pca = PrincipalComponentAnalysis()
# df = pca.apply_pca(df, predictor_columns, 3)

# # --------------------------------------------------------------
# # Sum of squares attributes
# # --------------------------------------------------------------
# df['acc_r'] = np.sqrt(df['acc_x'] ** 2 + df['acc_y'] ** 2 + df['acc_z'] ** 2)
# df['gyr_r'] = np.sqrt(df['gyr_x'] ** 2 + df['gyr_y'] ** 2 + df['gyr_z'] ** 2)

# # --------------------------------------------------------------
# # Temporal abstraction
# # --------------------------------------------------------------
# num_abs = NumericalAbstraction()
# window_size = int(1000 / 200)
# temporal_columns = predictor_columns + ['acc_r', 'gyr_r']

# df_temporal_list = []
# for s in df['set'].unique():
#     subset = df[df['set'] == s].copy()
#     for col in temporal_columns:
#         num_abs.abstract_numerical(subset, [col], window_size, 'mean')
#         num_abs.abstract_numerical(subset, [col], window_size, 'std')
#     df_temporal_list.append(subset)

# df = pd.concat(df_temporal_list)

#     # --------------------------------------------------------------
#     # Frequency features
#     # --------------------------------------------------------------
# freq_abs = FourierTransformation()
# fs = int(2800 / 200)
# freq_columns = temporal_columns

# df_freq_list = []
# for s in df['set'].unique():
#     subset = df[df['set'] == s].reset_index(drop=True).copy()
#     freq_abs.abstract_frequency(subset, freq_columns, 6, fs)
#     df_freq_list.append(subset)

# df = pd.concat(df_freq_list).set_index("epoch (ms)", drop=True)

# # --------------------------------------------------------------
# # Dealing with overlapping windows
# # --------------------------------------------------------------
# df = df.dropna()
# df = df.iloc[::2]  # Downsampling
