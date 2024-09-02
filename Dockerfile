# Dockerfile
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install dependencies
RUN pip install --upgrade pip

# Membuat direktori kerja
WORKDIR /app

# Menyalin file requirements dan menginstalnya
COPY requirements.txt /app/
RUN pip install -r requirements.txt

# Menyalin model dan kode aplikasi
COPY iris_model.pkl /app/
COPY app.py /app/

# Membuka port yang digunakan oleh Streamlit
EXPOSE 8080

# Perintah untuk menjalankan aplikasi Streamlit
CMD ["streamlit", "run", "app.py", "--server.port=8080", "--server.address=0.0.0.0"]
