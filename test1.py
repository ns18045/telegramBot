import telebot
from telebot import types
import datetime
from recipe_scrapers import scrape_me
import mysql.connector
import ast
import time
import random

# #region Database Info
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="",
    database="chatbot"
)

mycursor = mydb.cursor()
# mycursor.execute("CREATE TABLE recipes4 (id INT AUTO_INCREMENT PRIMARY KEY,title VARCHAR(255), ingredients longtext, instructions longtext, foodtype VARCHAR(50))")
# sql = "INSERT INTO recipes4 (title, ingredients, instructions, foodtype) VALUES (%s, %s, %s, %s)"
#
# links = []
#
# f = open("links.txt", "r")
# for x in f:
#     links.append(x)
# links = list(dict.fromkeys(links))
#
# for i in links:
#     split_link = i.split()
#     #print(split_link[1])
#     link = scrape_me(split_link[0])
#     #print(split_link[0])
#     input_ing = ''
#
#     ingredients = link.ingredients()
#     for ing in ingredients:
#         input_ing += ('* ' + ing + ' \n')
#
#     val = (link.title(), input_ing, link.instructions(), split_link[1])
#     mycursor.execute(sql, val)
# print('done execution')
# #endregion

mycursor.execute("SELECT * FROM recipes4")
myresult = mycursor.fetchall()
#print(myresult)
bot = telebot.TeleBot("1286885038:AAHuk0L97NqMKAx8DvuFgydntd73ivXgmG0")


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

breakfast = []
lunch=[]
dinner=[]
desserts=[]
drink=[]

for x in myresult:
    if x[4]=="breakfast":
        recipe = 'Title: \n' + x[1] + '\n\n' + 'Ingredients: \n' + x[2] + '\n\n' + 'Instruction: \n' + x[3]
        breakfast.append(recipe)
    if x[4]=="lunch":
        recipe = 'Title: \n' + x[1] + '\n\n' + 'Ingredients: \n' + x[2] + '\n\n' + 'Instruction: \n' + x[3]
        lunch.append(recipe)
    if x[4]=="dinner":
        recipe = 'Title: \n' + x[1] + '\n\n' + 'Ingredients: \n' + x[2] + '\n\n' + 'Instruction: \n' + x[3]
        dinner.append(recipe)
    if x[4]=="desserts":
        recipe = 'Title: \n' + x[1] + '\n\n' + 'Ingredients: \n' + x[2] + '\n\n' + 'Instruction: \n' + x[3]
        desserts.append(recipe)
    else:
        recipe = 'Title: \n' + x[1] + '\n\n' + 'Ingredients: \n' + x[2] + '\n\n' + 'Instruction: \n' + x[3]
        drink.append(recipe)


@bot.message_handler(commands=['random'])
def start(message):


    markup = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton(text="Breakfast", callback_data="Breakfast")
    button2 = types.InlineKeyboardButton(text="Lunch", callback_data="Lunch")
    button3 = types.InlineKeyboardButton(text="Dinner", callback_data="Dinner")
    button4 = types.InlineKeyboardButton(text="Desserts", callback_data="Desserts")
    button5 = types.InlineKeyboardButton(text="Drink", callback_data="Drink")
    markup.add(button1, button2, button3, button4, button5)
    bot.send_message(chat_id=message.chat.id, text="Select a category", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def longname(call):
    br = breakfast[random.randint(0, len(breakfast) - 1)]
    lu = lunch[random.randint(0, len(lunch) - 1)]
    di = dinner[random.randint(0, len(dinner) - 1)]
    de = desserts[random.randint(0, len(desserts) - 1)]
    dr = drink[random.randint(0, len(drink) - 1)]

    if call.data == "Breakfast":
        bot.send_message(chat_id=call.message.chat.id, text=br)
    elif call.data == "Lunch":
        bot.send_message(chat_id=call.message.chat.id, text=lu)
    elif call.data == "Dinner":
        bot.send_message(chat_id=call.message.chat.id, text=di)
    elif call.data == "Desserts":
        bot.send_message(chat_id=call.message.chat.id, text=de)
    elif call.data == "Drink":
        bot.send_message(chat_id=call.message.chat.id, text=di)


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
#mycursor.execute("DELETE FROM recipes4")

bot.polling()
