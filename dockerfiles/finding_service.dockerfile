FROM python:3.9 as base

WORKDIR /finding-service
COPY requirements.txt ./requirements.txt
RUN pip install -r requirements.txt

COPY /views ./views
COPY /utils ./utils
COPY /services/iservice.py ./services/iservice.py
COPY /models/location.py ./models/location.py
COPY /models/imodel.py ./models/imodel.py
COPY /communicators/interfaces ./communicators/interfaces
COPY /services/exceptions/location_exceptions.py ./services/exceptions/location_exceptions.py
COPY /initializers ./initializers

# ---------------------------------------------------- #

FROM base as finding-service-build

COPY /mains/finding_main.py ./main.py
COPY /communicators/finding_communicators ./communicators/finding_communicators
COPY /communicators/icommunicator.py ./communicators/icommunicator.py
COPY /communicators/__init__.py ./communicators/__init__.py

COPY /models/finding.py ./models/finding.py
COPY /models/__init__.py ./models/__init__.py

COPY /services/finding_service.py ./services/finding_service.py
COPY /services/__init__.py ./services/__init__.py
COPY /services/exceptions/finding_exceptions.py ./services/exceptions/finding_exceptions.py
COPY /services/exceptions/__init__.py ./services/exceptions/__init__.py

# ---------------------------------------------------- #

FROM finding-service-build as test-finding-service
RUN ls models
COPY /tests/__init__.py ./tests/__init__.py
COPY /tests/finding_tests/ ./tests/finding_tests/
COPY /tests/test_mysql_executor ./tests/test_mysql_executor
RUN pytest tests


FROM finding-service-build as finding-service
CMD ["python", "main.py"]
