FROM python:3.7

WORKDIR /bot
COPY . .

RUN pip install -r requirements.txt

CMD [ "python", "src/bot.py"]