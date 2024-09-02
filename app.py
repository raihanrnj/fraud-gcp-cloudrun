# app.py
import streamlit as st
import pickle
import numpy as np
import pandas as pd

# Fungsi untuk memuat model yang telah dilatih
@st.cache_resource
def load_model():
    with open('iris_model.pkl', 'rb') as f:
        model = pickle.load(f)
    return model

model = load_model()

st.title("Prediksi Bunga Iris")

st.write("""
### Masukkan fitur-fitur berikut untuk memprediksi jenis bunga Iris:
""")

# Input untuk fitur-fitur Iris
sepal_length = st.number_input('Panjang Sepal (cm)', min_value=0.0, max_value=10.0, value=5.0)
sepal_width = st.number_input('Lebar Sepal (cm)', min_value=0.0, max_value=10.0, value=3.5)
petal_length = st.number_input('Panjang Petal (cm)', min_value=0.0, max_value=10.0, value=1.4)
petal_width = st.number_input('Lebar Petal (cm)', min_value=0.0, max_value=10.0, value=0.2)

# Tombol untuk melakukan prediksi
if st.button('Prediksi'):
    # Menyiapkan data input
    input_data = np.array([[sepal_length, sepal_width, petal_length, petal_width]])
    prediction = model.predict(input_data)
    prediction_proba = model.predict_proba(input_data)

    # Memetakan hasil prediksi ke nama kelas
    iris = ['Setosa', 'Versicolor', 'Virginica']
    predicted_class = iris[prediction[0]]

    st.write(f"### Prediksi: **{predicted_class}**")
    st.write("### Probabilitas Prediksi:")
    proba_df = pd.DataFrame(prediction_proba, columns=iris)
    st.write(proba_df)


if __name__ == "__main__":
    port = '8080'
    st.run_server(port=port, address="0.0.0.0")
