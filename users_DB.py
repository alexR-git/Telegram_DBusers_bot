from telegram import Update, InputMediaDocument, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler, CallbackContext, PrefixHandler, ConversationHandler
import Token as btoken

token = btoken.token

print('Bot iniciado...')

# States
NAME, EMAIL = range(2)  # Conversación para configurar nombre e email

# global vars
global users
users = {}

# global key
# global value

def newuser(update: Update, callback: CallbackContext):

    update.message.reply_text('Hola, ¿cómo te llamas?')

    return NAME

def name_callback(update: Update, callback: CallbackContext):

    user_text = update.message.text
    global key
    key = user_text

    update.message.reply_text(f"Hola, {user_text}, ¿cuál es tu email?")

    return EMAIL    # y pasamos al estado EMAIL

def email_callback(update: Update, callback: CallbackContext):

    user_text = update.message.text
    global value
    value = user_text

    users[key] = value
    print(users)

    update.message.reply_text("Email recibido")

    return ConversationHandler.END

def fallback_callback(update: Update, callback: CallbackContext):

    update.message.reply_text("Disculpa, no te entiendo. Responde correctamente, por favor.")

def error(update: Update, context: CallbackContext) -> None:    #devuelve None

    """ Método de error """

    print(f'Update {update} caused error {context.error}')

def main():

    updater = Updater(token)  # objeto Updater: interfaz con el bot: nos permite interactuar con él
    print('updater creado')
    # updater = Updater(token, use_context=True)
    dp = updater.dispatcher  # objeto dispatcher: hacia donde se va a despachar todas las actualizaciones de mensajes que haga un usuario hacia nosotros
    print('dispatcher creado')

    #CONVERSATIONHANDLERS: conversación con el usuario

    entry_point = [CommandHandler("newuser", newuser)]   # comando + función de callback

    states = {
        NAME: [MessageHandler(filters=Filters.text, callback=name_callback)],
        EMAIL: [MessageHandler(filters=Filters.regex(r"^([a-z0-9_\.-]+)@([a-z0-9_\.-]+)\.([a-z0-9_\.-]+)$"), callback=email_callback)]
    }       # regex típico de un email. ^ = inicio; $ = fin.

    fallbacks = [MessageHandler(filters=Filters.all, callback=fallback_callback)]

    # entry points: comandos de entrada; states: estados de la conversación; fallbacks: callbacks de error;
    # allow_reentry: permitir o no recomienzo de la conversación (en cualquier momento de esta) al volver a enviar el comando de inicio.
    dp.add_handler(ConversationHandler(
        entry_points=entry_point,
        states=states,
        fallbacks=fallbacks,
        allow_reentry=True
    ))

    dp.add_error_handler(error)  # le especificamos que invoque el método error

    updater.start_polling(5)    # que el bot esté listo para escuchar de nuevo cada 5 segundos
    updater.idle()              # método para que el bot se quede escuchando

main()