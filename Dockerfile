FROM python:3.8-slim

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ARG TOKEN
ENV TOKEN=$TOKEN
ARG CHANNEL
ENV CHANNEL=$CHANNEL
ARG SCRIPT_NAME
ENV SCRIPT_NAME=$SCRIPT_NAME

CMD ["sh", "-c", "echo $SCRIPT_NAME; echo $TOKEN; echo $CHANNEL; python $SCRIPT_NAME $TOKEN $CHANNEL"]