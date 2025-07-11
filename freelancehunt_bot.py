import feedparser
import telegram
import time
import os
from dotenv import load_dotenv
from datetime import datetime

# Загружаем переменные окружения из файла .env
load_dotenv()

# ✅ Настройки
RSS_URL = os.getenv("RSS_URL")
CATEGORIES = [
    "cms",
    "html и css верстка",
    "веб-программирование",
    "дизайн сайтов",
    "создание сайта под ключ"
]
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
SENT_FILE = "sent_links.txt"

# Проверка наличия переменных окружения
if not TELEGRAM_TOKEN or not CHAT_ID or not RSS_URL:
    print("Ошибка: Не все переменные окружения заданы!")
    exit(1)

bot = telegram.Bot(token=TELEGRAM_TOKEN)

# Загрузка уже отправленных ссылок из файла
if os.path.exists(SENT_FILE):
    with open(SENT_FILE, "r", encoding="utf-8") as f:
        sent_links = set(line.strip() for line in f)
else:
    sent_links = set()

def filter_and_send():
    start_time = datetime.now()  # Время начала работы функции
    
    feed = feedparser.parse(RSS_URL)
    new_links = []
    
    for entry in feed.entries:
        title = entry.title.lower()
        description = entry.description.lower()  # Описание для дополнительной фильтрации
        categories = [category.lower() for category in entry.get("category", [])]

        # Проверяем, если хотя бы одна категория из списка
        category_matches = any(category in categories for category in CATEGORIES)

        if category_matches:
            link = entry.link
            # Проверяем, была ли эта ссылка уже отправлена
            if link not in sent_links:
                message = f"<b>{entry.title}</b>\n{entry.link}"

                # Логируем перед отправкой в Telegram
                print(f"Подготовка к отправке сообщения в Telegram: {datetime.now()} для заявки: {entry.title}")

                try:
                    # Отправка сообщения в Telegram
                    bot.send_message(chat_id=CHAT_ID, text=message, parse_mode='HTML')
                    
                    # Логируем успешную отправку
                    print(f"✅ Сообщение отправлено в Telegram: {datetime.now()} для заявки: {entry.title}")
                    
                    sent_links.add(link)
                    new_links.append(link)
                except telegram.error.TelegramError as e:
                    print(f"⚠️ Ошибка отправки сообщения: {e.message}")
                except Exception as e:
                    print(f"⚠️ Общая ошибка при отправке: {e}")
    
    # Сохраняем новые отправленные ссылки в файл
    if new_links:
        with open(SENT_FILE, "a", encoding="utf-8") as f:
            for link in new_links:
                f.write(link + "\n")
    
    end_time = datetime.now()  # Время окончания работы функции
    duration = (end_time - start_time).total_seconds()
    print(f"Время обработки заявки: {duration} секунд")  # Логируем время обработки

if __name__ == "__main__":
    print("🤖 Бот запущен. Проверяю вакансии каждую минуту...")
    while True:
        # Логирование времени начала новой итерации
        start_iteration = datetime.now()
        filter_and_send()
        
        # Логируем время между итерациями
        iteration_duration = (datetime.now() - start_iteration).total_seconds()
        print(f"Время между итерациями: {iteration_duration} секунд")
        
        # Логируем задержку на 60 секунд
        print("Задержка на 60 секунд...")
        
        # Пауза 1 минута
        time.sleep(60)




# import feedparser
# import telegram
# import time
# import os

# # ✅ Настройки
# RSS_URL = "https://freelancehunt.com/projects.rss"
# KEYWORDS = [
#     "cms",
#     "html",
#     "css",
#     "верстка",
#     "веб",
#     "web",
#     "программирование",
#     "дизайн",
#     "дизайн сайтов",
#     "веб-дизайн",
#     "создание сайта",
#     "сайт под ключ"
# ]
# TELEGRAM_TOKEN = "7693244558:AAHWN-iXMa6NoF3ANGdJnV88pvXuBLW_Vo4"
# CHAT_ID = "671379373"

# bot = telegram.Bot(token=TELEGRAM_TOKEN)
# SENT_FILE = "sent_links.txt"

# # Загрузка уже отправленных ссылок из файла
# if os.path.exists(SENT_FILE):
#     with open(SENT_FILE, "r", encoding="utf-8") as f:
#         sent_links = set(line.strip() for line in f)
# else:
#     sent_links = set()

# def filter_and_send():
#     feed = feedparser.parse(RSS_URL)
#     new_links = []
#     for entry in feed.entries:
#         title = entry.title.lower()
#         categories = []
#         if 'tags' in entry:
#             categories = [tag.term.lower() for tag in entry.tags]

#         # Проверяем ключевые слова в названии или категориях
#         if any(keyword in title for keyword in KEYWORDS) or any(keyword in categories for keyword in KEYWORDS):
#             link = entry.link
#             if link not in sent_links:
#                 message = f"<b>{entry.title}</b>\n{entry.link}"
#                 try:
#                     bot.send_message(chat_id=CHAT_ID, text=message, parse_mode='HTML')
#                     print(f"✅ Отправлено: {entry.title}")
#                     sent_links.add(link)
#                     new_links.append(link)
#                 except Exception as e:
#                     print(f"⚠️ Ошибка отправки: {e}")

#     # Сохраняем новые отправленные ссылки в файл
#     if new_links:
#         with open(SENT_FILE, "a", encoding="utf-8") as f:
#             for link in new_links:
#                 f.write(link + "\n")

# if __name__ == "__main__":
#     print("🤖 Бот запущен. Проверяю вакансии каждую минуту...")
#     while True:
#         filter_and_send()
#         time.sleep(60)
