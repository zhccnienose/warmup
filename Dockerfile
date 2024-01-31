FROM alpine

LABEL authors="72947"

WORKDIR /warmup

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

ENTRYPOINT ["python","-m","flask","--app","app.py","run","--host=0.0.0.0","--port=8000"]