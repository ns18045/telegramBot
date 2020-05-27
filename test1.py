import telebot
import datetime
from recipe_scrapers import scrape_me
import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="",
    database="chatbot"
)
mycursor = mydb.cursor()
# mycursor.execute("CREATE TABLE recipes (id INT AUTO_INCREMENT PRIMARY KEY,title VARCHAR(255), ingredients longtext, instructions longtext)")
sql = "INSERT INTO recipes (title, ingredients, instructions) VALUES (%s, %s, %s)"

links = ['https://www.101cookbooks.com/pasta-with-smashed-zucchini-cream/',
         'https://www.101cookbooks.com/biscotti-recipe/']

f = open("links.txt", "r")
for x in f:
    links.append(x)
links = list(dict.fromkeys(links))

for i in links:
    link = scrape_me(i)
    input_ing = ''

    ingredients = link.ingredients()
    for ing in ingredients:
        input_ing += (ing + ' / ')

    val = (link.title(), input_ing, link.instructions())
    mycursor.execute(sql, val)

mycursor.execute("SELECT * FROM recipes")
myresult = mycursor.fetchall()

bot = telebot.TeleBot("1286885038:AAHBVo2-FkZ0tSor2p6Lk9acY_9tUJ4DYIk")


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Options: '
                                      '/ingredients ingredient1 ingredient2 ... ingredientn - '
                                      'to find recipes by ingredients. '
                                      '/recipes food - '
                                      'to find recipe by food`s title, for example, "pancakes".'
                                      'Try both - plural and singular')

    # @bot.message_handler(commands=['start'])
    # def print(message):
    #     for x in myresult:
    #         bot.send_message(message.chat.id, 'Title: ' + x[1] + 'Ingredients: ' + x[2] + 'Instruction: ' + x[3])

    @bot.message_handler(commands=['ingredients'], content_types=['text'])
    def recipe_by_ingredients(message):
        count = 0
        ingredient_in = message.text.split()
        ingredient_in.remove('/ingredients')
        print(ingredient_in)
        for x in myresult:
            # res = [ele for ele in ingredient_in if (ele in x[2])]
            ingredient_out = x[2].split()
            res = all(item in ingredient_out for item in ingredient_in)
            if res is True:
                count = 1
                bot.send_message(message.chat.id, x[1])
        if count == 0:
            for x in myresult:
                res = [ele for ele in ingredient_in if (ele in x[2])]
                # ingredient_out = x[2].split()
                # res = all(item in ingredient_out for item in ingredient_in)
                if str(bool(res)) == 'True':
                    count += 1
                    bot.send_message(message.chat.id, 'Title: ' + x[1] + 'Ingredients: ' + x[2] + 'Instruction: ' + x[3])
            if count == 0:
                google_link = 'https://www.google.com/search?q='
                for ing in range(0,len(ingredient_in)):
                    google_link += ingredient_in[ing]+'+'
                google_link += 'ŗecipe'
                bot.send_message(message.chat.id, 'Couldn`t find anything. Use this link and I hope You will find '
                                                  'something useful: ' + google_link)

    @bot.message_handler(commands=['recipes'], content_types=['text'])
    def recipe_by_title(message):
        count = 0
        title_in = message.text.split()
        food = title_in[1]
        print(food)
        for x in myresult:
            print(x[1])
            if food.lower() in x[1].lower():
                count += 1
                bot.send_message(message.chat.id, x[1])
        if count == 0:
            google_link = 'https://www.google.com/search?q='+ food +'+recipe'
            bot.send_message(message.chat.id, 'Couldn`t find anything. Use this link and I hope You will find '
                                                  'something useful: ' + google_link)


bot.polling()
