from aiogram import Router,   F
from aiogram.filters.command import Command
from aiogram.types.input_file import FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery
from aiogram.types import ReplyKeyboardRemove

import os

from Bot.barcode import gen, list_barcodes
from Bot.QRcode import qr
from Bot.keyboards import change_kb, inline_builder, help_builder

router = Router()

# ----- FSM forms -----

#Состояние для сохранения qr кода
class Qr_form(StatesGroup):
    code = State()

#Состояние для сохранения выбора типа и кода штрихкода
class Barcode_form(StatesGroup):
    barcode_type = State()
    code = State()

# ----- Command start -----

@router.message(Command("start"))
async def cmd_start(message:Message):
    await message.answer("Выберите тип кода", reply_markup=change_kb)
    
# ----- Command help -----
@router.message(Command('help'))
async def cmd_help(message: Message):
    help = """
    Привет ! Этот бот генерирует штрихкоды

    QR код - код может состоять из любых последовательностей цифр и букв.
    EAN13 - цифровой код из 12 цифр и 1 контрольной.
    EAN8 - цифровой код из 7 цифр и 1 контрольной.
    ISBN10 - цифровой код из 6 цифр и 1 контрольной.
    ISBN13 - цифровой код начинающийся с 978 или 979, состоящий из 12 цифр и 1 контрольной, если начало 979 то следующая цифра должна быть 1 или 8.
    ISSN - цифровой код из 5 цифр и 1 контрольной.
    PZN - цифровой код из 7 цифр и 1 контрольной.
    UPC - цифровой код из 11 цифр и 1 контрольной.
    UPCA - цифровой код из 12 цифр и 1 контрольной.
"""
    await message.answer(help)
    

# ----- Help -----

@router.callback_query(F.data == 'Help')
async def help(callback: CallbackQuery):
    await callback.answer()

    help = """
    Привет ! Этот бот генерирует штрихкоды

    QR код - код может состоять из любых последовательностей цифр и букв.
    EAN13 - цифровой код из 12 цифр и 1 контрольной.
    EAN8 - цифровой код из 7 цифр и 1 контрольной.
    ISBN10 - цифровой код из 6 цифр и 1 контрольной.
    ISBN13 - цифровой код начинающийся с 978 или 979, состоящий из 12 цифр и 1 контрольной, если начало 979 то следующая цифра должна быть 1 или 8.
    ISSN - цифровой код из 5 цифр и 1 контрольной.
    PZN - цифровой код из 7 цифр и 1 контрольной.
    UPC - цифровой код из 11 цифр и 1 контрольной.
    UPCA - цифровой код из 12 цифр и 1 контрольной.
"""
    await callback.message.answer(help, reply_markup=change_kb)

# ----- QR code branch -----

@router.message(F.text == 'QR код')
async def make_qr(message: Message, state: FSMContext):
    await state.set_state(Qr_form.code)
    await message.answer('Введите код :')

@router.message(Qr_form.code)
async def process_code(message: Message, state: FSMContext):
    """
    Запрашивает и генерирует qr код, пока пользователь не введет команду "Назад"
    """

    if message.text == 'Назад':
        await state.clear()
        await message.answer('Выберите тип кода', reply_markup=change_kb)
    else :
        await state.update_data(code = message.text)
        data = await state.get_data()

        qr(data['code'])

        file = FSInputFile('/Users/and/Documents/Development/bot_code/qr.png')
        await message.reply_document(document=file, caption='Для выхода введите \'Назад\'', reply_markup=ReplyKeyboardRemove())
        os.remove('/Users/and/Documents/Development/bot_code/qr.png')
        await state.set_state(Qr_form.code)
    
# ----- Barcode branch -----

@router.message(F.text == 'Barcode')
async def change(message: Message, state: FSMContext):
    await state.set_state(Barcode_form.barcode_type)
    await message.answer('Выберите тип штрих кода :', reply_markup=inline_builder.as_markup())
    ReplyKeyboardRemove()

@router.callback_query(F.text == 'Barcode')
async def change_type(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Barcode_form.barcode_type)
    await callback.message.answer('Выберите тип штрих кода :', reply_markup=inline_builder.as_markup())

@router.callback_query(Barcode_form.barcode_type)
async def process_type(callback: CallbackQuery, state: FSMContext):
    await state.update_data(barcode_type = callback.data)
    await state.set_state(Barcode_form.code)
    await callback.answer('')
    await callback.message.edit_text('Введите код :')
    
@router.message(Barcode_form.code)
async def process_barcode(message: Message, state: FSMContext):
        await state.update_data(code = message.text.replace("-", ""))
        data = await state.get_data()
        type = data['barcode_type']

        if message.text != 'Назад':
            if (type == 'ean13') and (len(message.text.strip()) >=12) and (message.text.strip().isdigit()):
                gen(list_barcodes.index(type), int(data['code']))
                file = FSInputFile(f'/Users/and/Documents/Development/bot_code/code{type}.png')
                await message.reply_document(document=file, caption='Для выхода введите \'Назад\'', reply_markup=ReplyKeyboardRemove())
                await state.set_state(Barcode_form.code)
                os.remove(f'/Users/and/Documents/Development/bot_code/code{type}.png') 

            elif (type == 'ean8') and (len(message.text.strip()) >= 7) and (message.text.strip().isdigit()):
                gen(list_barcodes.index(type), int(data['code']))
                file = FSInputFile(f'/Users/and/Documents/Development/bot_code/code{type}.png')
                await message.reply_document(document=file, caption='Для выхода введите \'Назад\'', reply_markup=ReplyKeyboardRemove())
                await state.set_state(Barcode_form.code)
                os.remove(f'/Users/and/Documents/Development/bot_code/code{type}.png')

            elif (type == 'isbn10') and (len(message.text.strip()) >= 6) and (message.text.strip().isdigit()):# and (message.text.strip().startswith('978')):
                gen(list_barcodes.index(type), int(data['code']))
                file = FSInputFile(f'/Users/and/Documents/Development/bot_code/code{type}.png')
                await message.reply_document(document=file, caption='Для выхода введите \'Назад\'', reply_markup=ReplyKeyboardRemove())
                await state.set_state(Barcode_form.code)
                os.remove(f'/Users/and/Documents/Development/bot_code/code{type}.png')

            elif (type == 'isbn13') and (len(message.text.strip()) >= 12) and (message.text.strip().isdigit()) and ((message.text.strip().startswith('978')) or (message.text.strip().startswith('979') and message.text.strip()[3:4] in ("1", "8"))):
                gen(list_barcodes.index(type), int(data['code']))
                file = FSInputFile(f'/Users/and/Documents/Development/bot_code/code{type}.png')
                await message.reply_document(document=file, caption='Для выхода введите \'Назад\'', reply_markup=ReplyKeyboardRemove())
                await state.set_state(Barcode_form.code)
                os.remove(f'/Users/and/Documents/Development/bot_code/code{type}.png')

            elif (type == 'issn') and (len(message.text.strip()) >= 5)and (message.text.strip().isdigit()):# and (message.text.strip().startswith('977')):
                
                gen(list_barcodes.index(type), int(data['code']))
                file = FSInputFile(f'/Users/and/Documents/Development/bot_code/code{type}.png')
                await message.reply_document(document=file, caption='Для выхода введите \'Назад\'', reply_markup=ReplyKeyboardRemove())
                await state.set_state(Barcode_form.code)
                os.remove(f'/Users/and/Documents/Development/bot_code/code{type}.png')

            elif (type == 'pzn') and (len(message.text.strip()) >= 7) and (message.text.strip().isdigit()):
                gen(list_barcodes.index(type), int(data['code']))
                file = FSInputFile(f'/Users/and/Documents/Development/bot_code/code{type}.png')
                await message.reply_document(document=file, caption='Для выхода введите \'Назад\'', reply_markup=ReplyKeyboardRemove())
                await state.set_state(Barcode_form.code)
                os.remove(f'/Users/and/Documents/Development/bot_code/code{type}.png')

            elif (type == 'upc') and (len(message.text.strip()) >= 11) and (message.text.strip().isdigit()):
                gen(list_barcodes.index(type), int(data['code']))
                file = FSInputFile(f'/Users/and/Documents/Development/bot_code/code{type}.png')
                await message.reply_document(document=file, caption='Для выхода введите \'Назад\'', reply_markup=ReplyKeyboardRemove())
                await state.set_state(Barcode_form.code)
                os.remove(f'/Users/and/Documents/Development/bot_code/code{type}.png')

            elif (type == 'upca') and (len(message.text.strip()) >= 12) and (message.text.strip().isdigit()):
                gen(list_barcodes.index(type), int(data['code']))
                file = FSInputFile(f'/Users/and/Documents/Development/bot_code/code{type}.png')
                await message.reply_document(document=file, caption='Для выхода введите \'Назад\'', reply_markup=ReplyKeyboardRemove())
                await state.set_state(Barcode_form.code)
                os.remove(f'/Users/and/Documents/Development/bot_code/code{type}.png')

            else :
                await message.answer('Что то пошло не так, проверьте правильность ввода.', reply_markup=help_builder.as_markup())
                await state.set_state(Barcode_form.code)

        else :
            await state.clear()
            await message.answer('Выберите тип кода', reply_markup=change_kb)
    

