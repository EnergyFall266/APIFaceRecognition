FROM python:3.12


WORKDIR $APP_HOME
COPY . ./

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y
RUN pip install dlib==19.24.2
RUN pip install --no-cache-dir -r requirements.txt

# EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]