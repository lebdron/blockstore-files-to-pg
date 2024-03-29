FROM python:3.7.5
WORKDIR /usr/app
COPY . .
RUN pip3 install -r requirements.txt
ENTRYPOINT ["/usr/app/blockstore-files-to-pg.py"]
