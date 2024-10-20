from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.neural_network import MLPClassifier
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Conv2D, Flatten, SimpleRNN, LSTM

def define_models():
    """Define a list of models to train."""
    models = [
        ("Logistic Regression", LogisticRegression(C=1, solver='liblinear')),
        ("Random Forest", RandomForestClassifier(n_estimators=30, max_depth=3)),
        ("XGBClassifier", XGBClassifier(use_label_encoder=False, eval_metric='logloss')),
        ("Decision Tree", DecisionTreeClassifier(max_depth=5)),
        ("MLP Classifier", MLPClassifier(hidden_layer_sizes=(100,), max_iter=300)),
        ("CNN", Sequential([
            Conv2D(32, kernel_size=(3, 3), activation='relu', input_shape=(28, 28, 1)),
            Flatten(),
            Dense(128, activation='relu'),
            Dense(1, activation='sigmoid')
        ])),
        ("RNN", Sequential([
            SimpleRNN(50, input_shape=(100, 1), activation='relu'),
            Dense(1, activation='sigmoid')
        ])),
        ("LSTM", Sequential([
            LSTM(50, input_shape=(100, 1), activation='relu'),
            Dense(1, activation='sigmoid')
        ]))
    ]
    return models
