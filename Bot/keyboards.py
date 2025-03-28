from aiogram.types import KeyboardButton, InlineKeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from Bot.barcode import list_barcodes

# ----- Change of code -----

change_code = [[
    KeyboardButton(text='QR код'),
    KeyboardButton(text='Barcode')
]]

change_kb = ReplyKeyboardMarkup(keyboard=change_code,
                           resize_keyboard=True,
                           input_field_placeholder='Тип кода')

# ----- Help Button -----

help_builder = InlineKeyboardBuilder()
help_builder.add(InlineKeyboardButton(text='Help', callback_data='Help'))
help_builder.adjust(1,1)

# ----- Change type of barcode -----

inline_builder = InlineKeyboardBuilder()
for code in list_barcodes:
    inline_builder.button(text=f'{code.capitalize()}', callback_data=f'{code}')

inline_builder.adjust(3,3)


