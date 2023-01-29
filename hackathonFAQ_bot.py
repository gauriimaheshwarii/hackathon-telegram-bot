#IMPORTING ALL THE LIBRARIES & MODULES REQUIRED
from telegram.ext import *

print("Server is running....") #TO CHECK IF THE SERVER IS WORKING OR NOT

import nltk
import io
import os
import spacy
nltk.download('punkt')
from nltk.tokenize import word_tokenize
from nltk.metrics.distance import edit_distance
import requests
import telegram
from telegram import Bot
from telegram import InputFile
import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger()



#OUR BOT TOKEN 
bot = telegram.Bot(token='5813494687:AAG9nlGbNUWZ_hVzLvhRH-i60uAe1BO50JY')


#PREPROCESSING AND TOKENIZE FAQ DATA
faq = [("What are the dates?", "The hackathon is being held between 20 february 2022 to 22 february 2022"), 
       ("What is the time?", "It starts at 12 noon on 20 feb and ends on 11:59 pm on 22 feb"),
       ("What is the prize?","Prizes include swags from devfolio and github"),
       ("What is the theme?","It is an open innovation hackathon"),
       ("What is the schedule?","The hackathon is being held between 20 february 2022 to 22 february 2022,It starts at 12 noon on 20 feb and ends on 11:59 pm on 22 feb")
       ,("How many team members are allowed?","1-4 members are allowed"),
       ("How to register for the event?","Type /registration_info for all the registration details"),
       ("Where is the event taking place?","It is an online event"),
       ("What is the location?","It is an online event"),
       ("Is it offline?","It is an online event"),
       ("Give resources for the hackathon","Type /resources for more information")]
faq_tokens = [nltk.word_tokenize(x[0]) for x in faq]

#FUNCTION TO COMPARE USER'S INPUT TO PREPROCESSED DATA
def find_answer(text):
    text_tokens = nltk.word_tokenize(text)
    closest_match = min([(i, edit_distance(text_tokens, tokens)) for i, tokens in enumerate(faq_tokens)], key=lambda x: x[1])
    if closest_match[1] > 4:  # Threshold for edit distance
        return "I'm sorry, I don't understand your question. Please try with a different keyword or contact the organizers for further assistance."
    return faq[closest_match[0]][1]
 
#MESSAGE HANDLER
def answer(update, context):
    text = update.message.text
    if text == 'yes':
      update.message.reply_text("Type /registration_info to know how to register")
      return

    elif text == 'hi' or text == 'hello':
      image_url = 'https://res.cloudinary.com/drolg5ayv/image/upload/v1675007633/hello_lxtu0z.jpg'
  
      image = requests.get(image_url).content
      file = io.BytesIO(image)
      context.bot.send_photo(chat_id=update.effective_chat.id, photo=file)
      return

    elif text=='thanks' or text == 'thank you' :
      image_url = 'https://res.cloudinary.com/drolg5ayv/image/upload/v1675010176/thanks_v4d26g.webp'
  
      image = requests.get(image_url).content
      file = io.BytesIO(image)
      context.bot.send_photo(chat_id=update.effective_chat.id, photo=file)
      return

    elif text is None or text == "":
        update.message.reply_text("Please enter a valid text")
        return
    
    answer = find_answer(text)
    update.message.reply_text(answer)  

#COMMAND HANDLERS

#HELLO COMMAND
def hello(update,context):
    image_url = 'https://res.cloudinary.com/drolg5ayv/image/upload/v1675007633/hello_lxtu0z.jpg'
  
    image = requests.get(image_url).content
    file = io.BytesIO(image)
    context.bot.send_photo(chat_id=update.effective_chat.id, photo=file)

#START COMMAND
def start(update, context):
    chat_id = update.message.chat_id
    context.bot.send_message(chat_id=chat_id, text="Hello, I am here to answer your questions/queries about the upcoming hackathon. Type /help to see the available commands.")
    # update.message.reply_text("Hi! I'm a FAQ bot. Type /help to see the available commands")

#INFORMATION COMMAND
def information(update,context):
    update.message.reply_text("""
    Hi! Welcome to HackWave hackathon. 
    \nThis hackathon is being held from 20 february 2022 12 noon to 22 february 2022 11:59 pm. 
    \nIt is an online hackathon.
    \nWe donot have a theme. This is an open innovation hackathon. 
    \nThe prizes for the winners and 1st runner up include swags from github and devfolio. 
    \nWinner : 1000₹ per person of the team and swag kit from github & devfolio.
    \n1st Runner up: 500₹ per person of the team and swag kit from devfolio.
    \n\nWould you like to register?
     """)
 
#REGISTARTION INFORMATION COMMAND
def registration_info(update,context):
    update.message.reply_text("""You can register for the hackathon through the devfolio site. 
    \n Here is the link : https://devfolio.co/castor-2023/dashboard 
    \n After registering, you'll get a mail.
    \n Either you can create a team on devfolio, or join an existing team with custom team code which the team admin can share.
    \n Thanks.
    """)

#RESOURCES COMMAND
def resources(update,context):
  update.message.reply_text('''Following are the resources which could help you prepare for the hackathon: \nUse open source projects. \nRefer to youtube videos according to your tech stack.
   \nhttps://www.youtube.com/watch?v=vnmZAfIMNhA \nUse chatGPT to resolve errors \nHave fun!!!''')

#HELP COMMAND
def help_function(update, context):
  update.message.reply_text(
        """
    Available commands:

    /start : Starts up the bot
    /help : To see the available commands
    /information: To get all the details of the hackathon
    /registration_info : How to register for the hackathon
    /resources: Prepare for the hackathon and WIN AMAZING AND EXCITING PRIZES
    /hello: to say hello

    """
    )

#ERROR HANDLER
def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

# TELEGRAM API SETUP
updater = Updater("5813494687:AAG9nlGbNUWZ_hVzLvhRH-i60uAe1BO50JY", use_context=True)
dp = updater.dispatcher
dp.add_handler(CommandHandler("start", start))
dp.add_handler(CommandHandler("help",help_function))
dp.add_handler(CommandHandler("information",information))
dp.add_handler(CommandHandler("registration_info",registration_info))
dp.add_handler(MessageHandler(Filters.text, answer))
dp.add_handler(CommandHandler("hello",hello))
dp.add_handler(CommandHandler("resources",resources))
dp.add_error_handler(error)
updater.start_polling()
updater.idle()
