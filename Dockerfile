# Kullandığınız Python sürümü
FROM python:3.9

# Çalışma dizini
WORKDIR /app

# Gerektiğiniz bağımlılıkları kopyalayalım
COPY requirements.txt /app/
RUN python -m venv venv
RUN apt-get update && apt-get install -y iputils-ping
# Sanal ortamı etkinleştirip ve PATH'e ekleyelim
ENV PATH="/app/venv/bin:$PATH"

# Bağımlılıkları yükleyin
RUN pip install --no-cache-dir -r requirements.txt

# Celery'i kurun
RUN pip install celery

# Projenizin dosyalarını çalışma dizinine kopyalayın
COPY . /app/

# Celery işçilerini başlatın
# CMD ["celery", "-A", "mycelery", "worker", "-l", "info"]

# Uygulamayı çalıştırın (uygulamamızı başlatalım)
CMD ["/app/venv/bin/python", "manage.py", "runserver", "0.0.0.0:8000"]


