FROM python:2
COPY ./requirements.txt /requirements.txt
COPY ./prime_numpy.py /prime_numpy.py
RUN pip install --no-cache-dir -r /requirements.txt
CMD [ "python", "/prime_numpy.py" ]


