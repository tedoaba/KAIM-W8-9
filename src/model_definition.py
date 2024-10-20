from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.neural_network import MLPClassifier
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, SimpleRNN, LSTM
from tensorflow.keras.optimizers import Adam

def define_models():
    """Define a list of models to train."""
    models = [
        # Logistic Regression
        ("Logistic Regression", LogisticRegression(C=1, solver='liblinear')),
        
        # Random Forest
        ("Random Forest", RandomForestClassifier(n_estimators=30, max_depth=3)),
        
        # XGBoost
        ("XGBClassifier", XGBClassifier(use_label_encoder=False, eval_metric='logloss')),
        
        # Decision Tree
        ("Decision Tree", DecisionTreeClassifier(max_depth=5)),
        
        # MLP Classifier
        ("MLP Classifier", MLPClassifier(hidden_layer_sizes=(100,), max_iter=300)),
        
        # Deep Neural Network (DNN for tabular data)
        ("Deep Neural Network", compile_dnn_model),

        # RNN for tabular data
        ("RNN", compile_rnn_model),

        # LSTM for tabular data
        ("LSTM", compile_lstm_model)
    ]
    return models


def compile_dnn_model(input_shape):
    """Compile a simple deep neural network (DNN) model for tabular data."""
    model = Sequential([
        Dense(64, activation='relu', input_shape=(input_shape,)),
        Dense(32, activation='relu'),
        Dense(1, activation='sigmoid')  # Binary classification output
    ])
    # Compile the model
    model.compile(optimizer=Adam(), loss='binary_crossentropy', metrics=['accuracy'])
    return model


def compile_rnn_model(input_shape):
    """Compile an RNN model for tabular data with proper input shape."""
    model = Sequential([
        Dense(64, activation='relu', input_shape=(input_shape,)),  # Initial dense layer
        Dense(64, activation='relu'),  # Optional dense layers before RNN
        Dense(32, activation='relu'),
        # Reshape the input to add a time dimension for the RNN
        Dense(input_shape, activation='relu'),  # Another dense layer to expand features
        #SimpleRNN(50, activation='relu', input_shape=(1, input_shape)),  # Adjusted input for RNN
        Dense(1, activation='sigmoid')  # Binary classification output
    ])
    # Compile the model
    model.compile(optimizer=Adam(), loss='binary_crossentropy', metrics=['accuracy'])
    return model


def compile_lstm_model(input_shape):
    """Compile an LSTM model for tabular data."""
    model = Sequential([
        Dense(64, activation='relu', input_shape=(input_shape,)),
        LSTM(50, activation='relu'),
        Dense(1, activation='sigmoid')  # Binary classification output
    ])
    # Compile the model
    model.compile(optimizer=Adam(), loss='binary_crossentropy', metrics=['accuracy'])
    return model
