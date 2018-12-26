#!/usr/bin/env python
# -*-coding=utf-8 -*-

from services.TelegramService import Telegram 
import sys, getopt
import time

telegramService = Telegram()

def main(argv):
   chat_id = ''
   question_id = ''
   title = ''
   content = ''
   source = ''
   try:
      opts, args = getopt.getopt(argv,"i:q:t:c:w:",["id=","questionid=","title=","content=", "source="])
   except getopt.GetoptError:
      sys.exit(2)
   for opt, arg in opts:
      if opt in ("-i", "--id"):
         chat_id = arg
      elif opt in ("-q", "--questionid"):
         question_id = arg
      elif opt in ("-t", "--title"):
            title = arg
      elif opt in ("-c", "--content"):
            content = arg
      elif opt in ("-w", "--source"):
            source = arg
   print title, content, source
   if source == "tele":
      telegramService.tele_push_message(chat_id, question_id, title, content)
   elif source == "web":
      telegramService.web_push_message(chat_id, question_id, title, content)


if __name__ == "__main__":
   main(sys.argv[1:])

# telegramService = Telegram()

# telegramService.tele_push_message(chat_id, question_id, title, content)