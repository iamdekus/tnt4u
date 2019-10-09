import logging
from telegram import ParseMode, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
from csvp import csvp
import requests


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

CSV = csvp("dump/tntvillage.csv")


def b_to_mb(b):
    return float(b)/float(1024)/float(1024)


def get_magnet_shorted(magnet):
    mgnetme_api = "http://mgnet.me/api/create?m="
    magnet_shorted_request = requests.get(mgnetme_api + magnet)
    return magnet_shorted_request.json()["shorturl"]


def get_magnet_download(hash):
    magnet_template = "magnet:?xt=urn:btih:{}&dn=&tr=udp%3A%2F%2Ftracker.openbittorrent.com%3A80&tr=udp%3A%2F%2Fopentor.org%3A2710&tr=udp%3A%2F%2Ftracker.ccc.de%3A80&tr=udp%3A%2F%2Ftracker.blackunicorn.xyz%3A6969&tr=udp%3A%2F%2Ftracker.coppersurfer.tk%3A6969&tr=udp%3A%2F%2Ftracker.leechers-paradise.org%3A6969"
    return magnet_template.format(hash)


def get_content(content):
    content_template = "*Titolo:* {}\n*Descrizione:* {}\n*Dimensione:* {} MB"
    return content_template.format(content["TITOLO"], content["DESCRIZIONE"], b_to_mb(content["DIMENSIONE"]))


def start(update, context):
    update.message.reply_text("Benvenuto su *tnt4u*, puoi utilizzarmi per ottenere\n"
                              "le informazioni che situano sul dump rilasciato da\n"
                              "*tntvillage.com* in modo rapido e veloce.\n\n"
                              "*Come puoi utilizzarmi?\n*"
                              "E' molto semplice, ti bastera utilizzare il comando _/search_ e le parole chiavi che possono interessare il contenuto.\n\n"
                              "*Come scarico un contenuto?*\n"
                              "Anche questo è molto semplice, infatti grazie a *mgnet.me* abbiamo messo a disposizione un piccolo bottone che ti permettera di avere un short redirect link al magnet!",
                              parse_mode=ParseMode.MARKDOWN)


def search_callback(update, context):
    query = update.callback_query
    content = CSV.findElement("TOPIC", query.data)
    p = [[InlineKeyboardButton("🧲 Magnet Download", url=get_magnet_shorted(get_magnet_download(content["HASH"])))]]
    query.edit_message_text(text=get_content(content), parse_mode=ParseMode.MARKDOWN, reply_markup=InlineKeyboardMarkup(p))


def search(update, context):
    if len(context.args) >= 1:
        TITOLO = " ".join(context.args)
        data = CSV.findElements("TITOLO", TITOLO)
        ndata = len(data)
        if ndata > 0:
            if ndata <= 100:
                k = [[InlineKeyboardButton(row["TITOLO"], callback_data=row["TOPIC"])] for row in data]
                reply_markup = InlineKeyboardMarkup(k)
                update.message.reply_text("*{}* contenut{} individuat{}.".format(ndata, "i" if ndata > 1 else "o", "i" if ndata > 1 else "o"), # Probably not the best solution
                                          parse_mode=ParseMode.MARKDOWN,
                                          reply_markup=reply_markup)
            else:
                update.message.reply_text("Sono stati individuati *{}* contenuti, si prega di utilizzare più parole chiavi dato che non si possono mostrare più di 100 contenuti.".format(ndata),
                                          parse_mode=ParseMode.MARKDOWN)
        else:
            update.message.reply_text("Non sono stati individuati contenuti tramite le parole chiavi inserite.")
    else:
        update.message.reply_text("Per cercare correttamente dei contenuti devi inserire delle parole chiavi.")


def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    updater = Updater(TOKEN,
                      use_context=True)
    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CommandHandler('search', search))
    updater.dispatcher.add_handler(CallbackQueryHandler(search_callback))
    updater.dispatcher.add_error_handler(error)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()

