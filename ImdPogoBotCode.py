import logging
from uuid import uuid4

from telegram import InlineQueryResultArticle, ParseMode, \
    InputTextMessageContent
from telegram.ext import Updater, InlineQueryHandler, CommandHandler
from telegram.utils.helpers import escape_markdown


azul =[]
vermelho =[]
amarelo =[]


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi!')


def help(update, context):
    """Send a message when the command /help is issued."""
    helpText="""
    /raid : Lista de raid;
    /acordo : TEXTÃO do acordo;
    /planilha : planilha de informações dos membros;
    /time (azul, vermelho, amarelo) : marca todos os membros do time;
    /entrar (azul, vermelho, amarelo) (SUA TAG) : adiciona sua tag ao time;
    /flys : Desenvolvendo;
    """
    update.message.reply_text(helpText)

def acordo(update, context):
    """Send a message when the command /start is issued."""
    acordoText="""
    Nós também temos um acordo de rodízio no ginásio que DEVE ser respeitada pelos membros do grupo (vide planilha):
1 - Só pode derrubar o ginásio após o primeiro defensor completar 3h de permanência;
1.1 - Esse defensor deve ser do grupo;
1.2 - Se o 1º defensor não for do grupo (principalmente os fly conhecidos) pode derrubar o gym todo ou até restar membros do grupo e assim já adiantar a contagem de suas horas;
1.3 - Sendo desrespeitado o ponto 1, quem perdeu a posição no gym pode derrubar imediatamente, RESETANDO O TEMPO de permanência dele.
2 - Após o gym ser derrubado, a cor determinada é daquele, DO GRUPO, que ocupar a vaga primeiro;
Recomendações para melhor proveito do acordo:
*Quando alguém tomar o ginásio, avisem para os outros membros de sua cor aproveitarem as moedas também, e evitar gente de fora no gym;
*Quando virem o gym ser atacado antes da hora, avisem para os defensores poderem alimentar os seus pokémons, e evitar o item 1.3;
*Se precisar batalhar no gym para cumprir missão, avise para que os defensores possam dar frutas e evitar que eles sejam derrubados antes da hora;
*Não dar frutas aos seus pokémons para não dificultar a derrubada do mesmo depois das 3h do gym;
*Não colocar seu pokemon no gym caso já tenha pego as 50 moedas diárias. Uma hora você consegue sua medalha de ouro no gym e temos mais 2 pokestops para você pegar itens. Salvo se você estiver indo embora ou for no fim do dia visando a possibilidade de permanência até o próximo dia;
*Viu alguma regra ser desrespeitada? Procure sempre a conversa antes da retaliação, pois no meio das ações pode ter ocorrido ações de terceiros que desconhecem o acordo e assim vamos mantendo a boa convivência. Sendo assim, está aberta a possibilidade de acordos temporários para soluções pontuais;
*Viu alguém jogando pokémon no IMD? Converse sobre o grupo e sobre nosso acordo convidando-o pro grupo. Se ele não quiser entrar ou não usar o telegram, pergunte se ele vai respeitar o acorde e coloque-o na lista das pessoas do IMD que não estão no grupo.
    """
    update.message.reply_text(acordoText)


def raid(update, context):
    """Send a message when the command /help is issued."""
    raidText="""
    🔰 RAID LEVEL ?
🐣 Chefe: ?
⏳ Hora: ?
🏟 Gym: ?
🌎 Local: ?

1. ?
2.

    """
    update.message.reply_text(raidText)
def planilha(update, context):
    """Send a message when the command /help is issued."""
    link_planilha="""
    https://bit.ly/2M0O29N
    """
    update.message.reply_text(link_planilha)

def entrar(update, context):
    """Send a message when the command /help is issued."""
    if str(context.args[0]) == "azul":
        azul.append(context.args[1])
    elif str(context.args[0]) == "vermelho":
        vermelho.append(context.args[1])
    elif str(context.args[0]) == "amarelo":
        amarelo.append(context.args[1])

def time(update, context):
    saida = ""
    if context.args[0] == "azul":
        for membro in azul:
            saida += " {}".format(str(membro))
    elif context.args[0] == "vermelho":
        for membro in vermelho:
            saida += " {}".format(str(membro))
    elif context.args[0] == "amarelo":
        for membro in amarelo:
            saida += " {}".format(str(membro))
    update.message.reply_text(saida)

def sair(update, context):
    """Send a message when the command /help is issued."""
    for arg in context.args:
        update.message.reply_text(arg)


def inlinequery(update, context):
    """Handle the inline query."""
    query = update.inline_query.query
    results = [
        InlineQueryResultArticle(
            id=uuid4(),
            title="Caps",
            input_message_content=InputTextMessageContent(
                query.upper())),
        InlineQueryResultArticle(
            id=uuid4(),
            title="Bold",
            input_message_content=InputTextMessageContent(
                "*{}*".format(escape_markdown(query)),
                parse_mode=ParseMode.MARKDOWN)),
        InlineQueryResultArticle(
            id=uuid4(),
            title="Italic",
            input_message_content=InputTextMessageContent(
                "_{}_".format(escape_markdown(query)),
                parse_mode=ParseMode.MARKDOWN))]

    update.inline_query.answer(results)


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():

    updater = Updater("647981294:AAHdUxrChSiecomkRcVxWZAtJWJHk1oM06g", use_context=True)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("acordo", acordo))
    dp.add_handler(CommandHandler("raid", raid))
    dp.add_handler(CommandHandler("planilha", planilha))
    dp.add_handler(CommandHandler("entrar", entrar, pass_args=True))
    dp.add_handler(CommandHandler("time", time, pass_args=True))
    dp.add_handler(CommandHandler("sair", sair, pass_args=True))

    dp.add_handler(InlineQueryHandler(inlinequery))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Block until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
