import random
import json
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.neural_network import MLPClassifier
from telegram import Update
from telegram.ext import ApplicationBuilder
from telegram.ext import MessageHandler
from telegram.ext import filters


def get_intent(text):
    """Преобразуем текст в числа"""
    text_vec = vectorizer.transform([text])
    # берем 0, чтобы избавиться от формата "список"
    return model_mlp.predict(text_vec)[0]


def get_response(intent):
    return random.choice(data[intent]['responses'])


def bot(text):
    intent = get_intent(text)
    answer = get_response(intent)
    return answer


async def reply(update: Update, context) -> None:
    user_text = update.message.text
    reply = bot(user_text)
    print('<-', user_text)
    print('->', reply)

    # ответ пользователю в чат
    await update.message.reply_text(reply)


with open('intents_dataset.json', 'r', encoding='UTF-8') as file:
    data = json.load(file)

x = list()
y = list()
for name in data:
    for phrase in data[name]['examples']:
        x.append(phrase)
        y.append(name)

# векторизация фраз из data
vectorizer = CountVectorizer()
# обучаем векторайзер
vectorizer.fit(x)
# преобразуем вектор в численное представление
x_vec = vectorizer.transform(x)

# подключение нейронной сети
model_mlp = MLPClassifier()
# обучаем нейронную сеть
model_mlp.fit(x_vec, y)

TOKEN = '5534866523:AAHi_7m0PZpysXBsG6rmxDfRfywTcAXS3jw'
# создаем приложение и привязываем к токену
app = ApplicationBuilder().token(TOKEN).build()

# создаем обработчик текстовых сообщений
handler = MessageHandler(filters.Text(), reply)

# добавляем обработчик в приложение
app.add_handler(handler)

# запускаем приложение
app.run_polling()
print('start')
