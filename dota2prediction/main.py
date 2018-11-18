from keras.models import Sequential
from keras.layers import Dense
import json
import numpy as np
from sklearn.preprocessing import StandardScaler

def main():
    model = Sequential()
    input_dim = 9  # number of data input properties
    # xp1, xp2, net_worth1, net_worth2, kills1, death1, kills2, death2, time, winner[0-rad, 1-dire]
    with open('./sample.json') as f:
        train_data = np.array(json.load(f)).astype('float32')
        train_data_x = train_data[:, :-2]
        train_data_y = train_data[:, -2:]

    scaler = StandardScaler()
    train_data_x = scaler.fit_transform(train_data_x)

    model.add(Dense(units=64, activation='relu', input_dim=input_dim, kernel_regularizer='l2'))
    model.add(Dense(units=30, activation='relu', kernel_regularizer='l2'))
    model.add(Dense(units=2, activation='softmax'))

    model.compile(loss='categorical_crossentropy',
                  optimizer='sgd',
                  metrics=['accuracy'])

    model.fit(train_data_x, train_data_y, epochs=1000, batch_size=32)
    loss_and_metrics = model.evaluate(train_data_x, train_data_y, batch_size=32)
    print(loss_and_metrics)

    test_x = np.array([[1300, 1200, 1000, 800, 7, 5, 5, 7, 600]]).astype('float32')
    norm_test_x = scaler.transform(test_x)
    govno = model.evaluate(norm_test_x, np.array([[1, 0]]).astype('float32'), batch_size=32)
    print(govno)
    pass


if __name__ == '__main__':
    main()
