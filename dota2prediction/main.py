from keras.models import Sequential
from keras.layers import Dense
import json
import numpy as np
from sklearn.preprocessing import StandardScaler
import pandas as pd
from pathlib import Path
from keras import callbacks
from keras import optimizers
from keras import regularizers
import datetime


def main():
    # With time
    processed_match_data = Path('D:/Magistracy/diss/processed_match_data.npy')

    # Without time
    # processed_match_data = Path('D:/Magistracy/diss/processed_match_data_without_time.npy')
    all_match_data = []

    if not processed_match_data.exists():
        with open('D:/Magistracy/diss/replays_data.json', 'r') as f:
            replays_data = json.load(f)

        root_folder = sorted(Path('D:/Magistracy/diss/parsed_replays').glob('*.dem.txt'))

        for i, f in enumerate(root_folder):
            match_data = pd.read_json(str(f), lines=True).values
            if len(match_data) <= 5 * 60:
                continue

            id_match = f.name[: f.name.find('_')]
            result_radiant = replays_data[id_match]['radiantWins']
            result_dire = not result_radiant
            match_data = match_data[300:, :-1]
            match_data_len = len(match_data)
            match_data = match_data.astype('float32')

            radiant_result_row = np.full((match_data_len, 1), result_radiant, dtype='float32')
            dire_result_row = np.full((match_data_len, 1), result_dire, dtype='float32')
            id_match_row = np.full((match_data_len, 1), float(id_match), dtype='float32')

            match_data = np.append(match_data, radiant_result_row, axis=1)
            match_data = np.append(match_data, dire_result_row, axis=1)
            match_data = np.append(match_data, id_match_row, axis=1)
            all_match_data.append(match_data)
            print(i)

        all_match_data = np.vstack(all_match_data)
        np.save(processed_match_data, all_match_data)
    else:
        all_match_data = np.load(processed_match_data)

    print(len(all_match_data))

    model = Sequential()
    scaler = StandardScaler()

    X_train, X_test, y_train, y_test = custom_data_split(all_match_data, test_size=0.1)
    input_dim = X_train.shape[1]
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    model.add(Dense(units=64, activation='selu', kernel_initializer='lecun_normal', input_dim=input_dim,
                    kernel_regularizer=regularizers.l1(0.001)))
    model.add(Dense(units=64, activation='selu', kernel_initializer='lecun_normal',
                    kernel_regularizer=regularizers.l2(0.1)))
    model.add(Dense(units=64, activation='selu', kernel_initializer='lecun_normal',
                    kernel_regularizer=regularizers.l2(0.1)))
    model.add(Dense(units=2, activation='softmax'))

    model.compile(loss='categorical_crossentropy',
                  optimizer=optimizers.SGD(lr=0.0001, momentum=0.9),
                  metrics=['accuracy'])

    run_number = f'{int(datetime.datetime.now().timestamp())}'

    model.fit(X_train, y_train, validation_data=[X_test, y_test], epochs=50, batch_size=128, callbacks=[
        callbacks.TensorBoard(log_dir=f'D:/Magistracy/diss/logs/run{run_number}'
                              # write_grads=True, write_images=True,
                              # histogram_freq=1, embeddings_data=X_train, embeddings_layer_names=['dense_3']
                              ),
        callbacks.ModelCheckpoint(filepath=f'D:/Magistracy/diss/logs/run{run_number}' + '/weights.{epoch:04d}.hdf5')
    ])
    loss_and_metrics = model.evaluate(X_train, y_train, batch_size=128)
    print(loss_and_metrics)

    loss_and_metrics = model.evaluate(X_test, y_test, batch_size=128)
    print(loss_and_metrics)
    pass


def custom_data_split(all_match_data, test_size=0.3):
    np.random.shuffle(all_match_data)
    match_id_column = all_match_data[:, -1]
    match_id_column = np.unique(match_id_column)

    match_id_len = len(match_id_column)
    pivot_match_id = int(match_id_len - match_id_len * test_size)
    train_ids = match_id_column[:pivot_match_id]
    test_ids = match_id_column[pivot_match_id:]

    train_match_data = all_match_data[np.isin(all_match_data[:, -1], train_ids)]
    test_match_data = all_match_data[np.isin(all_match_data[:, -1], test_ids)]
    return train_match_data[:, :-3], test_match_data[:, :-3], train_match_data[:, -3:-1], test_match_data[:, -3:-1]


if __name__ == '__main__':
    main()
