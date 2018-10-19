FROM python:3

COPY . /app
WORKDIR /app

RUN pip install pipenv
RUN pipenv install

EXPOSE 5000

ENTRYPOINT ["pipenv", "run"]
CMD ["serve"]