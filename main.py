import hashlib
import sys
from telegram.ext.dispatcher import run_async
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import Update, Bot, ParseMode
import os


#-----------------------------GLOBAL VARIABLES---------------------------------
DOWNLOADED_FILE_NAME = ""
NO_FILE="NO FILE FOUND"
#MALWARE ="MALWARE DETECTED"
#NO_MALWARE = "NO MALWARE DETECTED"
MD5_HASH = ""
RESULT = []
#-------------------------------------------------------------------------------


#-----------------------CHECK VIRUS FUNCTION------------------------------------
def FileAnalyzer(filename):
    global RESULT, MD5_HASH
    md5_hash = hashlib.md5()
    try:
        inputFile = open(filename, "rb")
        FILE_OPEN=inputFile.read()
        md5_hash.update(FILE_OPEN)
        MD5_HASH=md5_hash.hexdigest()
        inputFile.close()
        try:
            virus_file=open("virus.txt","r")
            if MD5_HASH in virus_file.read():
                #RESULT = RESULT + "MALWARE DETECTED"
                RESULT.append("MALWARE DETECTED")
                #print(MALWARE)
            else:
                #RESULT = RESULT + "NO MALWARE DETECTED, YOUR SYSTEM IS CLEAN"
                RESULT.append("NO MALWARE DETECTED, YOUR SYSTEM IS SAFE")
                #print(NO_MALWARE)
        except IOError:
            print(NO_FILE)
        print(MD5_HASH)

    except IOError:
        print(NO_FILE)

#--------------------VIRUS CHECK FUNTION END-----------------------
#f = input("Enter name of input file: ")
#md(f)
#-------------------------------------------------------------------


def start(update, context):
    """Send a message when the command /start is issued."""
    #update.message.reply_text('Hi! \n\nWelcome to TeleBot AntiVirus. \n\nJust send a file which you want to get analized to the bot and it will check for any malware present!\n')
    update.message.reply_text("Hi, " + str(update.message.from_user.first_name) + "!!")
    update.message.reply_text("you can use following commands\n • /start -> To start the bot.\n • /help -> To see how to use this bot.\n")
#-----------------------------------------------------------------------------

def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Just send a file which you want to get analyzed to the bot and it will check for any malware present!!\n')
#------------------------------------------------------------------------------

def echo(update, context):
    """Echo the user message"""
    query = update.message.text
    update.message.reply_text('     •••••••••••••••••         \n   ♥        ♥     \n ♥ ♥  ♥ ♥     \n  ♥♥ ♥♥    \n     ♥♥♥    \n         ♥\n\n You Sent--->'+query+ '\n'+'Sorry we don\'t accept text messages!!')
#-------------------------------------------------------------------------------
def auto_generate(update, context):
    """Echo the user message"""

    update.message.reply_text('     •••••••••••••••••         \n   ♥        ♥     \n ♥ ♥  ♥ ♥     \n  ♥♥ ♥♥    \n     ♥♥♥    \n         ♥\n\n\n'+'Sorry we only accept files!!')
#-------------------------------------------------------------------------------
def photo(update, context):
    """Send reply of user's message."""
    update.message.reply_text('File Uploaded Successfully👍👍')
    photo_file = context.bot.get_file(update.message.photo[-1].file_id)#[-1] used to select the high resulution image
    photo_file_name = str(update.message.photo[-1].file_id)+'_testing'
    photo_file.download(photo_file_name)

    try:
        FileAnalyzer(photo_file_name)

        update.message.reply_text('REPORT:\n♦♦'+RESULT[0])
        update.message.reply_text('Thankyou for using our AntiVirus!!!\n\nMade with ♥ AntiVirus Bot')
        RESULT.clear()
    except Exception as e:
        update.message.reply_text(e)
    try:

        os.remove(photo_file_name)
    except Exception:
        pass


#-------------------------------------------------------------------------------
def document_fetch(update,context):

    #Send reply of user's message.
    update.message.reply_text('File Uploaded Successfully👍👍')
    file_id = update.message.document.file_id
    new_file = context.bot.get_file(file_id)
    filename = str(update.message.chat_id)+'_'+str(update.message.document.file_name)
    filesize = (int(update.message.document.file_size)/1024)
    if (filesize < 1024):
        filesize=str(filesize)+"KB"
    else:
        filesize=str(int(filesize)/1024)+ "MB"
    new_file.download(filename,timeout=300)
    DOWNLOADED_FILE_NAME=filename
    #call the FileAnalyzer function
    FileAnalyzer(DOWNLOADED_FILE_NAME)
    #Send the reply to thre from_user
    update.message.reply_text('REPORT:\n♦♦'+RESULT[0])
    update.message.reply_text('Thankyou for using our AntiVirus!!!\n\nMade with ♥ AntiVirus Bot')
    RESULT.clear()
#Delete the downloaded file
    try:
        os.remove(DOWNLOADED_FILE_NAME)

    except Exception:
        pass
#-------------------------------------------------------------------------------


def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    TELE_TOKEN = os.environ.get("BOT_TOKEN","")
    updater = Updater(TELE_TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help))


    # on noncommand i.e message - echo the message on Telegram
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))
    dispatcher.add_handler(MessageHandler(Filters.audio & ~Filters.command, auto_generate))
    dispatcher.add_handler(MessageHandler(Filters.video & ~Filters.command, auto_generate))
    dispatcher.add_handler(MessageHandler(Filters.photo & ~Filters.command, photo))
    dispatcher.add_handler(MessageHandler(Filters.document & ~Filters.command, document_fetch))
    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if  __name__=='__main__':
    main()
