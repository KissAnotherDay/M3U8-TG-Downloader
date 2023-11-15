import telebot
import os
import subprocess
import eyed3


bot_token = 'insert bot token'


bot = telebot.TeleBot(bot_token)

path="insert path to download file"
test = os.listdir(path)


@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id, "Benvenuto! Inviami il link m3u8 da convertire.")


@bot.message_handler(func=lambda message: True)
def handle_text(message):
    try:
        input_link = message.text.strip()

        bot.send_message(message.chat.id, "Inserisci il nome del file di output:")

        bot.register_next_step_handler(message, handle_output_name, input_link)
    except Exception as e:
        bot.send_message(message.chat.id, f"Si è verificato un errore: {str(e)}")


def handle_output_name(message, input_link):
    bot.send_message(message.chat.id, "Download e conversione in corso")
    try:
        output_name = message.text.strip()

        output_name = f"{output_name}.mp3"

        subprocess.run(['ffmpeg', '-i', input_link,'-b:a', '320k','-metadata', f'title={output_name}', output_name])


        if os.path.exists(output_name):
            with open(output_name, 'rb') as audio_file:
                bot.send_audio(message.chat.id, audio_file)
                bot.send_message(message.chat.id, "Conversione completata con successo.")
            for item in test:
                if item.endswith('.mp3'):
                    os.remove(output_name)
        else:
            bot.send_message(message.chat.id, "Conversione fallita.")
    except Exception as e:
        bot.send_message(message.chat.id, f"Si è verificato un errore: {str(e)}")


bot.polling()
