FROM python:3.9

WORKDIR /junkia-service

COPY requirements.txt .
RUN pip install -r ./requirements.txt

COPY . .

EXPOSE 3000

CMD [ "python", "main.py" ]