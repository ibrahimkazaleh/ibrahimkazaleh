from sklearn.neural_network import MLPClassifier
import pandas as pd
import numpy as np
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import train_test_split
import joblib

# rede data 
df=pd.read_pickle('../../data/interim/03_data_featuers.pkl')


df_train= df.drop(['participant','category','set'],axis=1)

X = df_train.drop('label',axis=1)
y = df_train['label']

X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.25,random_state =42,stratify=y )

# feature 
basic_features = ["acc_x", "acc_y", "acc_z", "gyr_x", "gyr_y", "gyr_z"]
feature_set_1 = list(set(basic_features))

def feedforward_neural_network(
    train_X,
    train_y,
    test_X,
    hidden_layer_sizes=(100,),
    max_iter=2000,
    activation="logistic",
    alpha=0.0001,
    learning_rate="adaptive",
    gridsearch=True,
    print_model_details=False,
):

    if gridsearch:
        tuned_parameters = [
            {
                "hidden_layer_sizes": [
                    (5,),
                    (10,),
                    (25,),
                    (100,),
                    (
                        100,
                        5,
                    ),
                    (
                        100,
                        10,
                    ),
                ],
                "activation": [activation],
                "learning_rate": [learning_rate],
                "max_iter": [1000, 2000],
                "alpha": [alpha],
            }
        ]
        nn = GridSearchCV(
            MLPClassifier(), tuned_parameters, cv=5, scoring="accuracy"
        )
    else:
        # Create the model
        nn = MLPClassifier(
            hidden_layer_sizes=hidden_layer_sizes,
            activation=activation,
            max_iter=max_iter,
            learning_rate=learning_rate,
            alpha=alpha,
        )
        

    # Fit the model
    nn.fit(
        train_X,
        train_y.values.ravel(),
    )

    if gridsearch and print_model_details:
        print(nn.best_params_)

    if gridsearch:
        nn = nn.best_estimator_

    # Apply the model
    pred_prob_training_y = nn.predict_proba(train_X)
    pred_prob_test_y = nn.predict_proba(test_X)
    pred_training_y = nn.predict(train_X)
    pred_test_y = nn.predict(test_X)
    frame_prob_training_y = pd.DataFrame(pred_prob_training_y, columns=nn.classes_)
    frame_prob_test_y = pd.DataFrame(pred_prob_test_y, columns=nn.classes_)
    
    
    return pred_training_y, pred_test_y, frame_prob_training_y, frame_prob_test_y,nn



class_train_y, class_test_y, class_train_prob_y, class_test_prob_y ,nn= feedforward_neural_network(
    X_train[feature_set_1], y_train, X_test[feature_set_1], gridsearch=False
)

# model (nn)
model_path = "../../models/NN_workout_prediction_model(0).pkl"
try:
    model = joblib.load(model_path)
    print("Model loaded successfully!")
except Exception as e:
    print(f"Failed to load the model: {e}")
    raise


