from cobe.brain import Brain
from flask import Flask, request
import telebot, logging
from random import randint
import ConfigParser

app = Flask(__name__)

Config = ConfigParser.ConfigParser()
Config.read('/config/config.ini')
key = Config.get('Main', 'key')
url = Config.get('Main', 'url')
master = Config.get('Main', 'master')
global bot
bot = telebot.TeleBot(key)
logger = telebot.logger
telebot.logger.setLevel(logging.INFO)
global brain
global percent
global violence
percent = 5
violence = False

@app.route(url, methods=['GET', 'POST'])
def hook():
    if request.method == "POST":
        # retrieve the message in JSON and then transform it to Telegram object
        json_string = request.get_data()
        update = telebot.types.Update.de_json(json_string)
        if "edited_message" in json_string:
            return ''
        else:
            bot.process_new_messages([update.message])
            return ''


@bot.message_handler(commands=['setfun'])
def setfun(message):
    if str(message.from_user.id) == master:
      try:
          global percent
          percent = int(message.text.split()[1])
          bot.reply_to(message, "Fun set to " + str(percent) + "%, you crazy man.")
      except:
          bot.reply_to(message, "Damn, it doesn't work.")


@bot.message_handler(commands=['toggleviolence'])
def setfun(message):
    if str(message.from_user.id) == master:
      try:
          global violence
          violence = not violence
          if violence:
            bot.reply_to(message, "Violence activated")
          else:
            bot.reply_to(message, "Violence deactivated")
      except:
          bot.reply_to(message, "Damn, it doesn't work.")

@bot.message_handler(func=lambda message: True)
def fun(message):
    print message.text
    brain = Brain("/db/" + str(message.chat.id)[1:] + ".br")
    # Telegram understands UTF-8, so encode text for unicode compatibility
    brain.learn(message.text)
    if "tagueul" in message.text.lower() or "tg" in message.text.lower() or "ta gueule" in message.text.lower():
        bot.reply_to(message, "Non, toi ta gueule.")
    elif (randint(1, 100) < percent):
        if violence : 
          bot.reply_to(message, brain.reply(message.text.upper(), 3000))
        else :
          bot.reply_to(message, brain.reply(message.text, 3000))
    return 'ok'

if __name__ == '__main__':
    app.run(port=80, debug=True)
