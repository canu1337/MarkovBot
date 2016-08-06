from cobe.brain import Brain
from flask import Flask, request
import telebot, logging
from random import randint

app = Flask(__name__)

global bot
bot = telebot.TeleBot('bottoken')
logger = telebot.logger
telebot.logger.setLevel(logging.INFO)
global brain
global percent
percent = 5
@app.route('/path', methods=['GET', 'POST'])
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
    if str(message.from_user.id) == "userid":
      try:
          global percent
          percent = int(message.text.split()[1])
          bot.reply_to(message, "Fun set to " + str(percent) + "%, you crazy man.")
      except:
          bot.reply_to(message, "Damn, it doesn't work.")

@bot.message_handler(func=lambda message: True)
def fun(message):
    print message.text
    brain = Brain("./" + str(message.chat.id)[1:] + ".br")
    # Telegram understands UTF-8, so encode text for unicode compatibility
    brain.learn(message.text)
    if (randint(1, 100) < percent):
        bot.reply_to(message, brain.reply(message.text, 3000))
    return 'ok'

if __name__ == '__main__':
    app.run(port=7777, debug=True)
