import telebot
import os
import subprocess
import eyed3

# Inserisci il token del tuo bot Telegram
bot_token = 'insert bot token'

# Crea un oggetto bot
bot = telebot.TeleBot(bot_token)

path="insert path to download file"
test = os.listdir(path)

# Funzione per gestire il comando /start
@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id, "Benvenuto! Inviami il link m3u8 da convertire.")


# Funzione per gestire i messaggi di testo
@bot.message_handler(func=lambda message: True)
def handle_text(message):
    try:
        # Ottieni il testo del messaggio (il link m3u8)
        input_link = message.text.strip()

        # Chiedi all'utente il nome del file di output
        bot.send_message(message.chat.id, "Inserisci il nome del file di output:")

        # Aspetta una risposta dall'utente
        bot.register_next_step_handler(message, handle_output_name, input_link)
    except Exception as e:
        bot.send_message(message.chat.id, f"Si è verificato un errore: {str(e)}")


# Funzione per gestire il nome del file di output
def handle_output_name(message, input_link):
    bot.send_message(message.chat.id, "Download e conversione in corso")
    try:
        output_name = message.text.strip()

        # Aggiungi l'estensione .mp3 al nome di output
        output_name = f"{output_name}.mp3"

        # Esegui la conversione utilizzando FFmpeg
        subprocess.run(['ffmpeg', '-i', input_link,'-b:a', '320k','-metadata', f'title={output_name}', output_name])


        # Verifica se la conversione è riuscita
        if os.path.exists(output_name):
            # Invia il file mp3 a Telegram
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


# Avvia il bot
bot.polling()
