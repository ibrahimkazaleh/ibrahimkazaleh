import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
from LearningAlgorithms import ClassificationAlgorithms
import seaborn as sns
import itertools
from sklearn.metrics import accuracy_score, confusion_matrix
from joblib import dump, load


df=pd.read_pickle('../../data/interim/03_data_featuers.pkl')

df_train=df.drop(['participant','category','set'],axis=1)

x=df_train.drop('label',axis=1)
y=df_train[['label']]

X_train,X_test,Y_train,Y_test=train_test_split(x,y,test_size=0.25,random_state=42,stratify=y)
 

# --------------------------------------------------------------
# Split feature subsets
# --------------------------------------------------------------

basic_features = ["acc_x", "acc_y", "acc_z", "gyr_x", "gyr_y", "gyr_z"]
square_features = ["acc_r", "gyr_r"]
pca_features = ["pca_1", "pca_2", "pca_3"]
time_features = [f for f in df_train.columns if "_temp_" in f]
cluster_features = ["cluster"]
freq_features = [f for f in df_train.columns if (("_freq" in f) or ("_pse" in f))]



# Print feature counts
print("Basic features:", len(basic_features))
print("Square features:", len(square_features))
print("PCA features:", len(pca_features))
print("Time features:", len(time_features))
print("Frequency features:", len(freq_features))
print("Cluster features:", len(cluster_features))

featuer_set_1 =list(set(basic_features))
featuer_set_2=list(set(basic_features + square_features + pca_features))
featuer_set_3=list(set(featuer_set_2 + time_features))
featuer_set_4=list(set(featuer_set_3 + freq_features + cluster_features))

# -------------------------
# ----- the best model ----
learner = ClassificationAlgorithms()
(
    class_train_y,
    class_test_y,
    class_train_prob_y,
    class_test_prob_y,
) = learner.random_forest(
    X_train[featuer_set_4], Y_train, X_test[featuer_set_4], gridsearch=False
)

accuracy = accuracy_score(Y_test,class_test_y)

# Save the model 
dump(learner, '../../models/random_forest_model.joblib')



