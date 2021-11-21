                                                           FROM python:3.9 as base

WORKDIR /finding-service
COPY requirements.txt ./requirements.txt
RUN pip install -r requirements.txt

COPY /views ./views
COPY /utils ./utils

COPY /initializers/__init__.py ./initializers/__init__.py
COPY /initializers/app_initializer_abs.py ./initializers/app_initializer_abs.py

COPY /models/imodel.py ./models/imodel.py
COPY /models/__init__.py ./models/__init__.py
COPY /models/location.py ./models/location.py

COPY /communicators/interfaces ./communicators/interfaces
COPY /communicators/__init__.py ./communicators/__init__.py
COPY /communicators/icommunicator.py ./communicators/icommunicator.py

COPY /services/__init__.py ./services/__init__.py
COPY /services/iservice.py ./services/iservice.py
COPY /services/exceptions/__init__.py ./services/exceptions/__init__.py
COPY /services/exceptions/location_exceptions.py ./services/exceptions/location_exceptions.py

# ---------------------------------------------------- #

FROM base as user-service-build
COPY /mains/user_main.py ./main.py
COPY /communicators/user_communicators ./communicators/user_communicators

COPY /models/user.py ./models/user.py

COPY /services/user_service.py ./services/user_service.py
COPY /services/exceptions/user_exceptions.py ./services/exceptions/user_exceptions.py

COPY /initializers/user_initializer.py ./initializers/user_initializer.py

# ---------------------------------------------------- #

FROM user-service-build as test-user-service
COPY /tests/__init__.py ./tests/__init__.py
COPY /tests/user_tests/ ./tests/user_tests/
COPY /tests/test_mysql_executor ./tests/test_mysql_executor
RUN pytest tests


FROM user-service-build as user-service
CMD ["python", "main.py"]
