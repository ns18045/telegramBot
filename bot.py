import telebot
import datetime
from telebot import types
import mysql.connector
import ast
import time
import random
from recipe_scrapers import scrape_me

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="root",
    database = "bot"
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
# mycursor.execute("CREATE DATABASE Bot")
# mycursor.execute("CREATE TABLE Restaurant (id INT AUTO_INCREMENT PRIMARY KEY,Name VARCHAR(255), Address VARCHAR(255), Latitude FLOAT, Longitude FLOAT, Vegan BOOLEAN, Parking BOOLEAN)")

bot = telebot.TeleBot("1037730141:AAFBEbqNWoBdaEhKKDuKec5H-QjqJAWYwjM")

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

@bot.message_handler(commands=['calories'])
def type_of_product(message):
    if message.text == '/calories' :
        keyboard = types.InlineKeyboardMarkup()  # наша клавиатура
        key_mushroom = types.InlineKeyboardButton(text='Mushrooms', callback_data='mushrooms')
        keyboard.add(key_mushroom)  # добавляем кнопку в клавиатуру
        key_sausages = types.InlineKeyboardButton(text='Sausages', callback_data='sausages')
        keyboard.add(key_sausages)
        key_cereals_and_cereals = types.InlineKeyboardButton(text='Cereals and cereals', callback_data='cereals and cereals')
        keyboard.add(key_cereals_and_cereals)  # добавляем кнопку в клавиатуру
        key_oils_and_fats = types.InlineKeyboardButton(text='Oils and Fats', callback_data='Oils and Fats')
        keyboard.add(key_oils_and_fats)
        key_milk_products = types.InlineKeyboardButton(text='Milk products', callback_data='Milk products')
        keyboard.add(key_milk_products)  # добавляем кнопку в клавиатуру
        key_flour_and_flour_products = types.InlineKeyboardButton(text='Flour and flour products', callback_data='Flour and flour products')
        keyboard.add(key_flour_and_flour_products)
        key_meat_products = types.InlineKeyboardButton(text='Meat products', callback_data='Meat products')
        keyboard.add(key_meat_products)  # добавляем кнопку в клавиатуру
        key_vegetables = types.InlineKeyboardButton(text='Vegetables', callback_data='Vegetables')
        keyboard.add(key_vegetables)
        key_nuts_and_dried_fruits = types.InlineKeyboardButton(text='Mushrooms', callback_data='Nuts and dried fruits')
        keyboard.add(key_nuts_and_dried_fruits)  # добавляем кнопку в клавиатуру
        question = "Which product type you want to check?"
        bot.send_message(message.chat.id, text=question, reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: True)
def all(call):
    def type_of_product(call):
        if call.data == "Milk products":
            keyboard = types.InlineKeyboardMarkup()  # наша клавиатура
            key_milk = types.InlineKeyboardButton(text='Milk 3,2%', callback_data='Milk 3,2%')
            keyboard.add(key_milk)  # добавляем кнопку в клавиатуру
            key_coconut_milk = types.InlineKeyboardButton(text='Coconut milk Aroy-D', callback_data='Coconut milk')
            keyboard.add(key_coconut_milk)
            key_cream_9 = types.InlineKeyboardButton(text='Cream 9%', callback_data='Cream 9%')
            keyboard.add(key_cream_9)  # добавляем кнопку в клавиатуру
            key_cream_20 = types.InlineKeyboardButton(text='Cream 20%', callback_data='Cream 20%')
            keyboard.add(key_cream_20)
            key_sour_cream = types.InlineKeyboardButton(text='Sour cream 25%', callback_data='Sour cream 25%')
            keyboard.add(key_sour_cream)  # добавляем кнопку в клавиатуру
            key_caserole = types.InlineKeyboardButton(text='Cottage cheese casserole', callback_data='Cottage cheese casserole')
            keyboard.add(key_caserole)
            key_kefir = types.InlineKeyboardButton(text='Kefir 2%', callback_data='Kefir 2%')
            keyboard.add(key_kefir)  # добавляем кнопку в клавиатуру
            key_condensed_milk = types.InlineKeyboardButton(text='Сondensed milk', callback_data='Сondensed milk')
            keyboard.add(key_condensed_milk)
            question = 'Choose the product!'
            bot.send_message(call.message.chat.id, text=question, reply_markup=keyboard)
    def get_product(call):
        if call.data == "Milk 3,2%":
            bot.send_message(call.message.chat.id, "Milk 3,2%:\n Proteins, g: 2.9 \n Fats, g: 2.5\n Carbohydrates, g: 4.7 \n Kcal : 52\n")
        if call.data == "Coconut milk":
            bot.send_message(call.message.chat.id, "Coconut milk: \nProteins, g: 1.6 \n Fats, g: 18.5\n Carbohydrates, g: 2.0 \n Kcal : 181\n")
        if call.data == "Cream 9%":
            bot.send_message(call.message.chat.id, "Cream 9%:\n Proteins, g: 2.8 \n Fats, g: 9.0\n Carbohydrates, g: 4.0 \n Kcal : 107\n")
        if call.data == "Cream 20%":
            bot.send_message(call.message.chat.id, "Cream 20%:\nProteins, g: 2.8 \n Fats, g: 20.0\n Carbohydrates, g: 3.7 \n Kcal : 205\n")
        if call.data == "Sour cream 25%":
            bot.send_message(call.message.chat.id, "Sour cream 25%:\nProteins, g: 2.6 \n Fats, g: 25.0\n Carbohydrates, g: 2.5 \n Kcal : 248\n")
        if call.data == "Cottage cheese casserole":
            bot.send_message(call.message.chat.id, "Cottage cheese casserole:\n Proteins, g: 17.6\n Fats, g: 4.2\n Carbohydrates, g: 14.2 \n Kcal : 168\n")
        if call.data == "Kefir 2%":
            bot.send_message(call.message.chat.id, "Kefir 2%:\nProteins, g: 3.4 \n Fats, g: 2.0\n Carbohydrates, g: 4.7 \n Kcal : 50\n")
        if call.data == "Сondensed milk":
            bot.send_message(call.message.chat.id, "Сondensed milk:\nProteins, g: 7.2 \n Fats, g: 8.5\n Carbohydrates, g: 56.0 \n Kcal : 320\n")

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
    type_of_product(call)
    get_product(call)
    longname(call)

@bot.message_handler(content_types=['text'])
def find_restaurant(message):
    if(message.text == "Can you show the cafe next to me?" or message.text == "Can you show the restaurants next to me?"):
        bot.send_message(message.chat.id, "Send your location to me and i will do my best)")
        bot.register_next_step_handler(message, location)


@bot.message_handler(content_types=['location'])
def location(message):
        select = "SELECT * FROM Restaurant WHERE ((Latitude - %s) * (Latitude - %s)) + ((Longitude - %s) * (Longitude - %s)) <= 0.00001417945" % (message.location.latitude, message.location.latitude, message.location.longitude, message.location.longitude)
        mycursor.execute(select)
        myresult = mycursor.fetchall()
        count = "SELECT COUNT(*) FROM Restaurant WHERE ((Latitude - %s) * (Latitude - %s)) + ((Longitude - %s) * (Longitude - %s)) <= 0.00001417945" % (message.location.latitude, message.location.latitude, message.location.longitude, message.location.longitude)
        mycursor.execute(count)
        data = mycursor.fetchall()
        for x in data:
            if x[0] > 0:
                bot.send_message(message.chat.id, "There is " + str(x[0]) + "restaurant near you! Here is their adreses:")
                for adreses in myresult:
                    bot.send_message(message.chat.id, "Restaurant: " + adreses[1] + " Address: " + adreses[2])
            else:
                bot.send_message(message.chat.id, "Sorry, there is not any cafe or restourant near you(")

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
bot.polling()
