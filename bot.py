import os
import re
import json
import telebot
import urllib.parse

# Récupération du Token de manière sécurisée depuis l'hébergeur
API_TOKEN = os.environ.get('TELEGRAM_TOKEN')
bot = telebot.TeleBot(API_TOKEN)

def extract_value(text, pattern):
    match = re.search(pattern, text)
    return match.group(1) if match else ""

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Salut Donald ! Envoie-moi ton texte JSON ou le clipboard décrypté d'un fichier VPN, et je vais te générer un lien VLESS universel en 1 seconde ! ⚡")

@bot.message_handler(func=lambda message: True)
def convert_to_vless(message):
    text = message.text
    try:
        # Recherche des identifiants et variables réseaux par expressions régulières (Regex)
        uuid = extract_value(text, r'"id":\s*"([^"]+)"') or extract_value(text, r'"password":\s*"([^"]+)"')
        address = extract_value(text, r'"address":\s*"([^"]+)"') or "142.250.151.138"
        port = extract_value(text, r'"port":\s*(\d+)') or "443"
        path = extract_value(text, r'"path":\s*"([^"]+)"')
        sni = extract_value(text, r'"serverName":\s*"([^"]+)"') or extract_value(text, r'"sni":\s*"([^"]+)"')
        host = extract_value(text, r'"Host":\s*"([^"]+)"') or extract_value(text, r'"host":\s*"([^"]+)"')

        if not uuid:
            bot.reply_to(message, "❌ Erreur : Impossible de trouver un UUID ou un Password valide dans ce texte.")
            return

        # Encodage propre du chemin (Path) pour le format d'URL
        encoded_path = urllib.parse.quote(path)

        # Assemblage de la chaîne VLESS universelle
        vless_link = f"vless://{uuid}@{address}:{port}?path={encoded_path}&security=tls&sni={sni}&type=ws&host={host}#DONALD_CONVERT_⚡"

        # Envoi de la réponse formatée et cliquable
        response = f"✅ **Lien VLESS généré avec succès :**\n\n`{vless_link}`\n\n_Clique sur le lien pour le copier directement dans NapsternetV ou DarkTunnel !_"
        bot.reply_to(message, response, parse_mode='Markdown')

    except Exception as e:
        bot.reply_to(message, "❌ Une erreur est survenue lors de l'analyse du texte.")

if __name__ == "__main__":
    bot.polling(none_stop=True)
