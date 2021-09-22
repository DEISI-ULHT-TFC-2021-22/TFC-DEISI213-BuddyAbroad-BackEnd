FROM python:3.9
ENV PYTHONUNBUFFERED 1

RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
RUN unzip awscliv2.zip
RUN ./aws/install

WORKDIR /app
RUN pip install pipenv
COPY Pipfile* ./
RUN pipenv install --system --deploy --ignore-pipfile
COPY ./buddyAbroadAPI ./

EXPOSE 8000

CMD ["bash", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
