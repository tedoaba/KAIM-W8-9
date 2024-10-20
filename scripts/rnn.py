
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from keras.models import Sequential
from keras.layers import LSTM, Dense, Dropout
from keras.utils import to_categorical
from keras.optimizers import Adam

# Assume we have a DataFrame 'df' with tabular data
# Let's assume we want to predict the last column as our target
df = pd.read_csv('../data/cleaned_data_1.csv')
# Normalize the data
scaler = StandardScaler()
normalized_data = scaler.fit_transform(df.drop(df.columns[-1], axis=1))

# Create sequences
sequence_length = 10  # Number of past time steps to consider
X, y = [], []
for i in range(sequence_length, len(normalized_data)):
    X.append(normalized_data[i-sequence_length:i])
    y.append(normalized_data[i])

X = np.array(X)
y = np.array(y)

# Reshape input to be [samples, time_steps, features]
X = np.reshape(X, (X.shape[0], sequence_length, normalized_data.shape[1]))

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# One-hot encode the target variable
num_classes = 2

# Define the model architecture
model = Sequential([
    LSTM(64, activation='relu', input_shape=(sequence_length, normalized_data.shape[1]), return_sequences=True),
    Dropout(0.2),
    LSTM(32, activation='relu'),
    Dropout(0.2),
    Dense(1, activation='sigmoid')
])

# Compile the model
optimizer = Adam(learning_rate=0.001, decay=1e-6)
model.compile(optimizer=optimizer, loss='binary_crossentropy', metrics=['accuracy'])

# Train the model
history = model.fit(
    X_train,
    y_train,
    epochs=100,
    batch_size=32,
    validation_split=0.2,
    verbose=1
)

# Evaluate the model
test_loss, test_acc = model.evaluate(X_test, y_test)
print(f'Test accuracy: {test_acc:.2f}')

# Make predictions
predictions = model.predict(X_test)
