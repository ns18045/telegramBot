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
        input_ing += ('* ' + ing + ' \n')

    val = (link.title(), input_ing, link.instructions())
    mycursor.execute(sql, val)

mycursor.execute("SELECT * FROM recipes")
myresult = mycursor.fetchall()

bot = telebot.TeleBot("1286885038:AAFAjr5TiqBCQfyfnspIMMRMVKp7p5l9a5k")


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Options: \n'
                                      '* /ingredients ingredient1 ingredient2 ... ingredientn NUM - '
                                      'to find recipes by ingredients (optional). '
                                      'NUM - how many recipes You want to see (optional) \n'
                                      '* /recipes food - '
                                      'to find recipe by food`s title (one word, optional) NUM, '
                                      'for example, "pancakes". '
                                      'NUM - how many recipes You want to see (optional) '
                                      'Try both - plural and singular \n')

    # @bot.message_handler(commands=['start'])
    # def print(message):
    #     for x in myresult:
    #         bot.send_message(message.chat.id, 'Title: ' + x[1] + 'Ingredients: ' + x[2] + 'Instruction: ' + x[3])

    @bot.message_handler(commands=['ingredients'], content_types=['text'])
    def recipe_by_ingredients(message):
        res_count = 0
        output_count = len(myresult)
        ingredient_in = message.text.split()
        ingredient_in.remove('/ingredients')
        if ingredient_in[len(ingredient_in)-1].isdigit():
            output_count = int(ingredient_in[len(ingredient_in)-1])
            ingredient_in.pop(-1)
            if output_count > len(myresult):
                output_count = len(myresult)
        print(output_count)
        for x in myresult:
            # res = [ele for ele in ingredient_in if (ele in x[2])]
            ingredient_out = x[2].split()
            res = all(item in ingredient_out for item in ingredient_in)
            if res is True:
                res_count += 1
                if res_count > output_count:
                    break
                recipe = 'Title: \n' + x[1] + '\n\n' + 'Ingredients: \n' + x[2] + '\n\n' + 'Instruction: \n' + x[3]
                bot.send_message(message.chat.id, recipe)
        if res_count == 0:
            for x in myresult:
                res = [ele for ele in ingredient_in if (ele in x[2])]
                # ingredient_out = x[2].split()
                # res = all(item in ingredient_out for item in ingredient_in)
                if str(bool(res)) == 'True':
                    res_count += 1
                    if res_count > output_count:
                        break
                    recipe = 'Title: \n' + x[1] + '\n\n' + 'Ingredients: \n' + x[2] + '\n\n' + 'Instruction: \n' + x[3]
                    bot.send_message(message.chat.id, recipe)
            if res_count == 0:
                google_link = 'https://www.google.com/search?q='
                for ing in range(0,len(ingredient_in)):
                    google_link += ingredient_in[ing]+'+'
                google_link += 'recipe'
                bot.send_message(message.chat.id, 'Couldn`t find anything. Use this link and I hope You will find '
                                                  'something useful: ' + google_link)

    @bot.message_handler(commands=['recipes'], content_types=['text'])
    def recipe_by_title(message):
        res_count = 0
        output_count = len(myresult)
        title_in = message.text.split()
        if title_in[len(title_in) - 1].isdigit() and len(title_in) >= 2:
            output_count = int(title_in[2])
            if output_count > int(len(myresult)):
                output_count = len(myresult)
        print(output_count)
        food = ''
        title_in = message.text.split()
        if len(title_in) >= 2:
            food = title_in[1]
        for x in myresult:
            if food.lower() in x[1].lower():
                print(x[1])
                res_count += 1
                if output_count:
                    if res_count > output_count:
                        break
                recipe = 'Title: \n' + x[1] + '\n\n' + 'Ingredients: \n' + x[2] + '\n\n'+ 'Instruction: \n' + x[3]
                bot.send_message(message.chat.id, recipe)
        if res_count == 0:
            google_link = 'https://www.google.com/search?q='+ food +'+recipe'
            bot.send_message(message.chat.id, 'Couldn`t find anything. Use this link and I hope You will find '
                                                  'something useful: ' + google_link)
#mycursor.execute("DELETE FROM recipes")

bot.polling()

