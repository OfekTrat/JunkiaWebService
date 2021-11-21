FROM python:3.9 as base

WORKDIR /junkia-service

COPY requirements.txt .
RUN pip install -r ./requirements.txt

COPY . .

###########################

FROM base as test
WORKDIR /junkia-service
RUN pip install pytest==6.2.5
COPY images /images
RUN pytest tests
#CMD [ "pytest", "tests" ]

##############  ##############

FROM base as deploy
WORKDIR /junkia-service
EXPOSE 3000
CMD [ "python", "main.py" ]