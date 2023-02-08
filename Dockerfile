FROM python:3
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV TZ=Asia/Kuala_Lumpur
WORKDIR /app
COPY Pipfile /app/
COPY Pipfile.lock /app/
RUN pip install pipenv
RUN pipenv install --system --deploy --ignore-pipfile
COPY . /code/ 
