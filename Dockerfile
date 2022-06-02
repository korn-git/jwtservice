FROM python:3.9  

WORKDIR /app

COPY ./requirements.txt ./requirements.txt

RUN pip install --no-cache-dir --upgrade -r ./requirements.txt

# 
COPY ./main.py ./main.py

# 
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5555"]