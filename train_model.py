# train_model.py
import pandas as pd
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import pickle

def train_and_save_model():
    # Memuat dataset Iris
    iris = load_iris()
    X = iris.data
    y = iris.target

    # Membagi data menjadi train dan test (opsional)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Inisialisasi dan melatih classifier
    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X_train, y_train)

    # Menyimpan model yang telah dilatih ke dalam file
    with open('iris_model.pkl', 'wb') as f:
        pickle.dump(clf, f)

    print("Model telah dilatih dan disimpan sebagai iris_model.pkl")

if __name__ == "__main__":
    train_and_save_model()