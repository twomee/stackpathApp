FROM python:3.8

MAINTAINER "ido" "12ido350@gmail.com"

RUN apt-get update -y && \
    apt-get install -y python3-pip python-dev

# We copy just the requirements.txt first to leverage Docker cache
COPY requirements.txt /app/requirements.txt

EXPOSE 5000

WORKDIR /app

RUN pip3 install -r requirements.txt

COPY . /app

ENTRYPOINT [ "python" ]

CMD [ "stackpath_controller.py" ]


#to run it: sudo docker build -t stackpath:latest .