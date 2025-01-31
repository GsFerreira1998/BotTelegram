from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
import openpyxl
import os

#salvar a lista de mercado em um arquivo Excel
def salvar_lista(lista):
    # Criar uma planilha
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Lista de Mercado"
    
    #itens à planilha
    for index, item in enumerate(lista, start=1):
        ws[f"A{index}"] = item
    
    #arquivo Excel
    file_path = "lista_mercado.xlsx"
    wb.save(file_path)
    return file_path

#criar a lista de mercado
async def criar_lista(update: Update, context):
    # Receber a mensagem com os itens da lista separados por vírgula
    msg = update.message.text
    itens = msg.split(',')
    
    # Limpar e armazenar os itens em uma lista
    lista_mercado = [item.strip() for item in itens]
    
    # Salvar a lista em um arquivo Excel e obter o caminho do arquivo
    file_path = salvar_lista(lista_mercado)
    
    # Enviar o arquivo Excel para o usuário
    with open(file_path, 'rb') as file:
        await update.message.reply_document(document=file, filename="lista_mercado.xlsx")
    
    # Remover o arquivo após o envio para evitar acúmulo de arquivos
    os.remove(file_path)

#iniciar o bot
def main():
    # Substitua 'YOUR_TOKEN' pelo token que você obteve do BotFather
    application = Application.builder().token("********").build()

    # Adicionar manipuladores de comando
    application.add_handler(CommandHandler("start", lambda update, context: update.message.reply_text("Olá! Envie uma lista de mercado, separada por vírgula.")))
    
    # Adicionar manipulador para mensagens de texto
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, criar_lista))

    # Iniciar o bot
    application.run_polling()

if __name__ == "__main__":
    main()
