import keras.models as models
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from pathlib import Path


def main():
    processed_match_data = Path('D:/Magistracy/diss/processed_match_data.npy')
    all_match_data = np.load(processed_match_data)

    scaler = StandardScaler()

    X_train, X_test, y_train, y_test = custom_data_split(all_match_data, test_size=0.1)
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    model = models.load_model('D:/Magistracy/diss/model/weights.0052.hdf5')

    loss_and_metrics = model.evaluate(X_train, y_train, batch_size=128)
    print(loss_and_metrics)

    loss_and_metrics = model.evaluate(X_test, y_test, batch_size=128)
    print(loss_and_metrics)
    pass


def custom_data_split(all_match_data, test_size=0.3):
    start = 6
    end = 10
    match_id_column = all_match_data[:, -1]
    match_id_column = np.unique(match_id_column)

    match_id_len = len(match_id_column)
    pivot_match_id = int(match_id_len - match_id_len * test_size)
    train_ids = match_id_column[:pivot_match_id]
    test_ids = match_id_column[pivot_match_id:]

    train_match_data = all_match_data[np.isin(all_match_data[:, -1], train_ids)]
    test_match_data = all_match_data[np.isin(all_match_data[:, -1], test_ids)]
    test_match_data = test_match_data[(test_match_data[:, -4] > 60 * start) & (test_match_data[:, -4] < 60 * end)]

    return train_match_data[:, :-3], test_match_data[:, :-3], train_match_data[:, -3:-1], test_match_data[:, -3:-1]


if __name__ == '__main__':
    main()
