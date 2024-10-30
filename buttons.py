from telebot import types
from telebot.types import InlineKeyboardButton


def phone_buttons():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button = types.KeyboardButton('Поделиться номером',
                                  request_contact=True)
    kb.add(button)
    return kb
def location_button():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button = types.KeyboardButton('Поделиться локацией',
                                  request_location=True)
    kb.add(button)
    return kb

def main_menu_kb():
    kb =types.ReplyKeyboardMarkup(resize_keyboard= True)
    menu = types.KeyboardButton(text="🍴Меню")
    cart = types.KeyboardButton(text= "🛒Корзина")
    feedback = types.KeyboardButton(text= "✒️Отзыв")
    kb.add(menu, cart)
    kb.row(feedback)
    return kb

def products_in(products):
    kb = types.InlineKeyboardMarkup(row_width=2)
    cart = types.InlineKeyboardButton(text="Корзина", callback_data="cart")
    back = types.InlineKeyboardButton(text="Назад", callback_data="back")
    all_products = [types.InlineKeyboardButton(text=f"{product[1]}", callback_data=f"prod_{product[0]}")
                    for product in products]
    kb.add(*all_products)
    kb.row(cart)
    kb.row(back)
    return kb

def plus_minus_in(plus_or_minus="", current_amount=1):
    kb = types.InlineKeyboardMarkup(row_width=3)
    back = types.InlineKeyboardButton(text="Назад", callback_data="main_menu")
    to_cart = types.InlineKeyboardButton(text="Добавить в корзину",
                                         callback_data="to_cart")
    minus = types.InlineKeyboardButton(text="➖", callback_data="minus")
    plus = types.InlineKeyboardButton(text="➕", callback_data="plus")
    count = types.InlineKeyboardButton(text=f"{current_amount}", callback_data="none")
    if plus_or_minus == "plus":
        new_amount = current_amount + 1
        count = types.InlineKeyboardButton(text=f"{new_amount}", callback_data="none")
    elif plus_or_minus == "minus":
        if current_amount > 1:
            new_amount = current_amount - 1
            count = types.InlineKeyboardButton(text=f"{new_amount}", callback_data="none")
    kb.row(minus, count, plus)
    kb.row(to_cart)
    kb.row(back)
    return kb
def get_cart_kb(products):
    kb = types.InlineKeyboardMarkup(row_width=1)
    clear = types.InlineKeyboardButton(text="Очистить корзину", callback_data="clear_cart")
    order = types.InlineKeyboardButton(text="Оформить заказ", callback_data="order")
    back = types.InlineKeyboardButton(text="Назад", callback_data="main_main")
    kb.add(order, clear, back)
    if products:
        all_products = [types.InlineKeyboardButton(text=f"❌ {product[1]}", callback_data=f"delete_{product[0]}") for product in
                        products]
        kb.add(*all_products)
    return kb

def agree_or_no():
    kb = types.InlineKeyboardMarkup(row_width=1)
    agree = types.InlineKeyboardButton(text="✅", callback_data="agree")
    disagree = types.InlineKeyboardButton(text="❌", callback_data="disagree")
    kb.add(agree, disagree)
