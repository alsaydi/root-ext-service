# Root Extraction Service
This is a web service that returns a list of possible roots for an Arabic word. It's written in Python and uses flask. 
It uses the [Tashaphyne library](https://github.com/linuxscout/tashaphyne). 

It augments the result with roots that are looked in a database, currently a [flat file](./data/word-root-table.txt). The flat file is built using a utility that can be found here [https://github.com/alsaydi/sarf](https://github.com/alsaydi/sarf).

## Running the service locally

You can run the service in development mode like so:

1. create a python virtual environment, optional but highly recommended

```
python3 -m venv .pyenv
source ./.pyenv/bin/activate
pip3 install -r requirements.txt 
```
The above snippets creates the virtual environment and installs the dependencies used by this service.

2. To run the service do:
```
export FLASK_APP=main.py
flask run
```
3. To test, use wget or a browser
```
wget -O- http://localhost:5000/تمم 2> /dev/null
wget -O- http://localhost:5000/مساهم
```

## Running the docker image

This service is also in a container. You can built the container locally `docker build -t rootext .` or you can use `docker run --rm -p 8090:8090 alsaydi/rootext:1.0`.
See https://hub.docker.com/r/alsaydi/rootext.
