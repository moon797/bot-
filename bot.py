import telebot
from telebot.apihelper import send_message
import buttons as bt
import database as db
from geopy import Photon, Nominatim
geolocator = Nominatim(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36")
bot = telebot.TeleBot(token="7859392860:AAEllWXqIxzXLkQ3Kq_gITL4wV100toslf0")
users= {}
#db.add_product('Cheeseburger', '15000', 'лучший бургер', '4' , 'https://www.google.com/imgres?q=burgers&imgurl=https%3A%2F%2Fwww.seriouseats.com%2Fthmb%2Fe16lLOoVEix_JZTv7iNyAuWkPn8%3D%2F1500x0%2Ffilters%3Ano_upscale()%3Amax_bytes(150000)%3Astrip_icc()%2F__opt__aboutcom__coeus__resources__content_migration__serious_eats__seriouseats.com__recipes__images__2014__09__20140918-jamie-olivers-comfort-food-insanity-burger-david-loftus-f7d9042bdc2a468fbbd50b10d467dafd.jpg&imgrefurl=https%3A%2F%2Fwww.seriouseats.com%2Finsanity-burger-from-jamie-olivers-comfort-food&docid=86wZPegcyr7JMM&tbnid=VKdMerLcdsrdyM&vet=12ahUKEwjsvN76jqyJAxXlKRAIHaQ7O0gQM3oECBcQAA..i&w=1500&h=1125&hcb=2&ved=2ahUKEwjsvN76jqyJAxXlKRAIHaQ7O0gQM3oECBcQAA')
#db.add_product('Hotdog', '20000', 'лучший бургер' , '5' , 'https://www.google.com/imgres?q=burgers&imgurl=https%3A%2F%2Fassets.epicurious.com%2Fphotos%2F5c745a108918ee7ab68daf79%2F1%3A1%2Fw_2560%252Cc_limit%2FSmashburger-recipe-120219.jpg&imgrefurl=https%3A%2F%2Fwww.epicurious.com%2Frecipes%2Ffood%2Fviews%2Fclassic-smashed-cheeseburger-51261810&docid=zF63VJti-aMYyM&tbnid=mBVqgdIRxF3l2M&vet=12ahUKEwjsvN76jqyJAxXlKRAIHaQ7O0gQM3oECFYQAA..i&w=2503&h=2503&hcb=2&ved=2ahUKEwjsvN76jqyJAxXlKRAIHaQ7O0gQM3oECFYQAA')
#db.add_product('Бургер', '3300', 'лучший бургер' , '0','https://www.google.com/imgres?q=burgers&imgurl=https%3A%2F%2Fwww.foodandwine.com%2Fthmb%2FDI29Houjc_ccAtFKly0BbVsusHc%3D%2F1500x0%2Ffilters%3Ano_upscale()%3Amax_bytes(150000)%3Astrip_icc()%2Fcrispy-comte-cheesburgers-FT-RECIPE0921-6166c6552b7148e8a8561f7765ddf20b.jpg&imgrefurl=https%3A%2F%2Fwww.foodandwine.com%2Frecipes%2Fcrispy-comte-cheeseburgers&docid=lPAsBqpdsxWgvM&tbnid=81aE112Ti0KgUM&vet=12ahUKEwjsvN76jqyJAxXlKRAIHaQ7O0gQM3oFCIgBEAA..i&w=1500&h=1001&hcb=2&ved=2ahUKEwjsvN76jqyJAxXlKRAIHaQ7O0gQM3oFCIgBEAA')
@bot.message_handler(commands=["start"])

def start(message):
    user_id = message.from_user.id
    bot.send_message(user_id, "Добро пожаловать в бот доставки!")
    checker = db.check_user(user_id)
    if checker == True:
        bot.send_message(user_id, "Главное меню:" , reply_markup=bt.main_menu_kb())
    elif checker== False:
        bot.send_message(user_id, "Введите своё имя для регистрации")
        print(message.text)
        bot.register_next_step_handler(message, get_name)
def get_name(message):
    user_id = message.from_user.id
    name = message.text
    print(message.text)
    bot.send_message(user_id, "Теперь поделитесь своим номером",
                     reply_markup=bt.phone_buttons())
    bot.register_next_step_handler(message, get_phone_number, name)
def get_phone_number(message, name):
    user_id = message.from_user.id
    if message.contact:
        phone_number = message.contact.phone_number
        print(phone_number)
        bot.send_message(user_id, "Отправьте свою локацию", reply_markup=bt.location_button())
        bot.register_next_step_handler(message, get_location, name, phone_number)
    else:
        bot.send_message(user_id, "Отправьте свой номер через кнопку в меню")
        bot.register_next_step_handler(message, get_phone_number, name)
def get_location(message, name, phone_number):
    user_id = message.from_user.id
    if message.location:
        latitude = message.location.latitude
        longitude = message.location.longitude
        address = (latitude, longitude)
        print(name, phone_number, address)
        db.add_user(name=name, phone_number=phone_number, user_id=user_id)
        bot.send_message(user_id, "Вы успешно зарегистрировались!")
        bot.send_message(user_id, "Главное меню: ", reply_markup=bt.main_menu_kb())
    else:
        bot.send_message(user_id, "Send your location")
        bot.register_next_step_handler(message, get_location, name , phone_number)
@bot.callback_query_handler(lambda call: call.data in ["cart", "back", "plus", "minus",
                                                       "to_cart", "main_menu", "order", "clear_cart", "agree", "disagree"])
def all_cals(call):
    user_id = call.message.chat.id
    if call.data == "cart":
        cart = db.get_user_cart(user_id)
        full_text = "Ваша корзина: \n"
        count = 0
        total_price = 0
        for product in cart:
            count += 1
            full_text += f"{count}. {product[0]}x {product[1]} = {product[2]}\n"
            total_price += product[2]
        cart_for_buttons = db.get_card_id_name(user_id)
        bot.send_message(user_id, full_text +f"\n\n Total price: {total_price} sum", reply_markup=bt.get_cart_kb(cart_for_buttons))
        bot.delete_message(user_id, call.message.message_id)
    elif call.data == "agree":
        bot.delete_message(user_id, call.message.message_id)
        bot.edit_message_text(chat_id=-4504031843, message_id=call.message.message_id,
                              text="Принято✅",
                              reply_markup=bt.agree_or_no())
    elif call.data == "disagree":
        bot.delete_message(user_id, call.message.message_id)
        bot.edit_message_text(chat_id=-4504031843, message_id=call.message.message_id,
                              text="Отклонено❌",
                              reply_markup=bt.agree_or_no())
    elif call.data == "back":
        bot.delete_message(user_id, call.message.message_id)
        bot.send_message(user_id, "Главное меню: ", reply_markup=bt.main_menu_kb())
    elif call.data == "plus":
        current_amount = users[user_id]["pr_count"]
        users[user_id]["pr_count"] += 1
        bot.edit_message_reply_markup(chat_id=user_id, message_id=call.message.message_id, reply_markup=bt.plus_minus_in("plus", current_amount))
    elif call.data == "minus":
        current_amount = users[user_id]["pr_count"]
        if current_amount > 1:
            users[user_id]["pr_count"] -= 1
            bot.edit_message_reply_markup(chat_id=user_id, message_id=call.message.message_id,
                                      reply_markup=bt.plus_minus_in("minus", current_amount))

    elif call.data == "to_cart":
        db.add_to_cart(user_id, users[user_id]["pr_id"], users[user_id]["pr_name"], users[user_id]["pr_count"],
                   users[user_id]["pr_price"])
        users.pop(user_id)
        bot.delete_message(user_id, call.message.message_id)
        all_products = db.get_pr_id_name()
        bot.send_message(user_id, "Продукт добавлен! Хотите ещё...", reply_markup=bt.products_in(all_products))
    elif call.data == "main_menu":
        all_products = db.get_pr_id_name()
        bot.send_message(user_id, "Выберите продукт", reply_markup=bt.products_in(all_products))
    elif call.data == "order":
        bot.delete_message(user_id, call.message.message_id)
        number = db.get_phone_number(user_id)
        name = db.get_name(user_id)
        cart = db.get_user_cart(user_id)
        full_text = f"Новый заказать от пользователя с {user_id}: \n"
        count = 0
        total_price = 0
        for product in cart:
            count += 1
            full_text += f"{count}. {product[0]}x {product[1]} = {product[2]}\n"
            total_price += product[2]
        bot.send_message(-4504031843, full_text+f"\n\n Total price: {total_price} sum\n Имя клиента: {name} \n Телефон номер клиента: {number}  ")
        bot.send_message(user_id, "Ваш заказ принят и обрабатывается оператором", reply_markup=bt.main_menu_kb())
        db.delete_user_cart(user_id)
    elif call.data == "clear_cart":
        bot.delete_message(user_id, call.message.message_id)
        bot.send_message(user_id, "Ваша корзина очищена")
        db.delete_user_cart(user_id)

@bot.callback_query_handler(lambda call: "prod_" in call.data)
def get_prod_info(call):
    user_id = call.message.chat.id
    bot.delete_message(user_id , call.message.message_id)
    product_id = int(call.data.replace("prod_", ""))
    product_info = db.get_exact_product(product_id)
    users[user_id] = {"pr_id": product_id, "pr_name": product_info[0], "pr_count": 1, "pr_price": product_info[1]}
    bot.send_photo(user_id, photo=product_info[3], caption=f"{product_info[0]}\n\n"
                                                           f"{product_info[2]}\n"
                                                           f"Цена: {product_info[1]}", reply_markup=bt.plus_minus_in())

@bot.callback_query_handler(lambda call: "delete_" in call.data)
def delete_product_from_cart(call):
    user_id = call.message.chat.id
    product_id = int(call.data.replace("delete_", ""))
    db.delete_exact_product(user_id, product_id)
    cart = db.get_user_cart(user_id)
    full_text = "Ваша корзина: \n"
    count = 0
    total_price = 0
    for product in cart:
        count += 1
        full_text += f"{count}. {product[0]} x {product[1]} = {product[2]}\n"
        total_price += product[2]
    cart_for_buttons = db.get_card_id_name(user_id)
    bot.edit_message_text(chat_id=user_id, message_id=call.message.message_id, text=full_text + f"\n\nИтоговая сумма: {total_price} сум",
                     reply_markup=bt.get_cart_kb(cart_for_buttons))

@bot.message_handler(content_types=["text"])
def main_menu(message):
    user_id = message.from_user.id
    if message.text == "🍴Меню":
        all_products = db.get_pr_id_name()
        bot.send_message(user_id, "Выберите продукт: ", reply_markup=bt.products_in(all_products))
    elif message.text == "🛒Корзина":
        cart = db.get_user_cart(user_id)
        full_text = "Ваша корзина: \n"
        count = 0
        total_price = 0
        for product in cart:
            count += 1
            full_text += f"{count}. {product[0]}x {product[1]} = {product[2]}\n"
            total_price += product[2]
        cart_for_buttons = db.get_card_id_name(user_id)
        bot.send_message(user_id, full_text + f"\n\n Total price: {total_price} sum",
                         reply_markup=bt.get_cart_kb(cart_for_buttons))

    elif message.text == "✒️Отзыв":
        user_id = message.from_user.id
        bot.send_message( user_id, "Ваш отзыв? ")
        bot.register_next_step_handler(message, report)

def report(message):
    user_id = message.from_user.id
    name = message.text
    print(message.text)
    bot.send_message(-4504031843, f"{user_id} : {name}" , reply_markup=bt.agree_or_no())
    bot.send_message(user_id,"Благодарим, вам за вашу отзыв!")

bot.infinity_polling()