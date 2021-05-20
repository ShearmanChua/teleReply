import time
from telethon import TelegramClient, events
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer


# sample API_ID from https://github.com/telegramdesktop/tdesktop/blob/f98fdeab3fb2ba6f55daf8481595f879729d1b84/Telegram/SourceFiles/config.h#L220
# or use your own
api_id = 1234567
api_hash = '78a6b613459cb02df7a6ab23f5233bfd'

# fill in your own details here
phone = '+6585797336'
session_file = '@Username'  # use your username if unsure
password = 'YOUR_PASSWORD'  # if you have two-step verification enabled

# content of the automatic reply
message = "Sorry, I'll be away until next week!"

chatbot = ChatBot("shearman")

# Create a new trainer for the chatbot
trainer = ChatterBotCorpusTrainer(chatbot)


# Train based on the english corpus
trainer.train("chatterbot.corpus.english")

# Train based on english greetings corpus
trainer.train("chatterbot.corpus.english.greetings")

# Train based on the english conversations corpus
trainer.train("chatterbot.corpus.english.conversations")

# Train based on the chinese corpus
trainer.train("chatterbot.corpus.chinese")


if __name__ == '__main__':
    # Create the client and connect
    # use sequential_updates=True to respond to messages one at a time
    client = TelegramClient(session_file, api_id, api_hash, sequential_updates=True)


    @client.on(events.NewMessage(incoming=True))
    async def handle_new_message(event):
        if event.is_private:  # only auto-reply to private chats
            from_ = await event.client.get_entity(event.from_id)  # this lookup will be cached by telethon
            if not from_.bot:  # don't auto-reply to bots
                print(time.asctime(), '-', event.message)  # optionally log time and message
                time.sleep(1)  # pause for 1 second to rate-limit automatic replies
                print(event.message.message)
                print(chatbot.get_response(event.message.message))
                await event.respond(chatbot.get_response(event.message.message).text)
        else:
            chat_from = event.chat if event.chat else (await event.get_chat())  # telegram MAY not send the chat enity
            chat_title = chat_from.title
            print(chat_title)






    print(time.asctime(), '-', 'Auto-replying...')
    client.start(phone, password)
    client.run_until_disconnected()
    print(time.asctime(), '-', 'Stopped!')
