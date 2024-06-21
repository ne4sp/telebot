import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F, Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
import texting
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup, InlineKeyboardButton
from config import Config, load_config
# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)
config: Config = load_config()
BOT_TOKEN: str = config.tg_bot.token
bot = Bot(BOT_TOKEN)
# Диспетчер
dp = Dispatcher()
router = Router()
user_data = {}
curr_lang = 'ru'



def isNum(num):
    try:
        num = int(num)
        flag = True
    except Exception:
        flag = False
    return flag


class Talking(StatesGroup):
    CheckingID = State()
    setID = State()
    inputID = State()
    WrongID = State()
    RightID = State()


@dp.message(Command('start'))
async def choose_language(message: types.Message):
    buttons = [
        [
            types.InlineKeyboardButton(text="Русский🇷🇺", callback_data="ru_lang"),
            types.InlineKeyboardButton(text='Украинский🇺🇦', callback_data="ua_lang")
        ],
        [types.InlineKeyboardButton(text='ВСТУПИТЬ В VIP ✅', callback_data='acceptVIP_ru')],
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    await message.answer(
        texting.text1,
        reply_markup=keyboard
    )


@dp.callback_query(F.data == "ru_lang")
async def set_ua_lang(callback: types.CallbackQuery, state: FSMContext):
    global curr_lang
    curr_lang = 'ru'
    buttons = [
        [
            types.InlineKeyboardButton(text="Русский🇷🇺", callback_data="ru_lang"),
            types.InlineKeyboardButton(text='Украинский🇺🇦', callback_data="ua_lang")
        ],
        [types.InlineKeyboardButton(text='ВСТУПИТЬ В VIP ✅', callback_data='acceptVIP_ru')],
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    try:
        await callback.message.edit_text(text=texting.text1, reply_markup=keyboard)
    except Exception:
        await callback.answer()


@dp.callback_query(F.data == "ua_lang")
async def set_ua_lang(callback: types.CallbackQuery, state: FSMContext):
    global curr_lang
    curr_lang = 'ua'
    buttons = [
        [
            types.InlineKeyboardButton(text="Російська🇷🇺", callback_data="ru_lang"),
            types.InlineKeyboardButton(text='Українська🇺🇦', callback_data="ua_lang")
        ],
        [types.InlineKeyboardButton(text='ВСТУПИТИ У VIP ✅', callback_data='acceptVIP_ua')],
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    try:
        await callback.message.edit_text(text=texting.text1_ua, reply_markup=keyboard)
    except Exception:
        await callback.answer()

# @dp.message(Talking.CheckingID)
# async def choose_language(message: types.Message):
#     await message.answer(
#         texting.text2_ru
#         )


@dp.callback_query(F.data == "acceptVIP_ru")
async def give_id_ru(callback: types.CallbackQuery, state: FSMContext):
    buttons = [
        [
            types.InlineKeyboardButton(text="Русский🇷🇺", callback_data="ru_lang_give_id"),
            types.InlineKeyboardButton(text='Украинский🇺🇦', callback_data="ua_lang_give_id")
        ],
        [types.InlineKeyboardButton(text='Проверить ID ', callback_data='agreeID_ru')],
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    await callback.message.answer(texting.text211_ru, reply_markup=keyboard)
    await callback.message.answer_video(
        video='BQACAgIAAxkBAAIByWZ0xMbrv_Ts54nS7rCeO700Y67NAAIvUgACauUAAUu_1-xCNtjo_zUE')
    await state.set_state(Talking.inputID)
    await callback.answer()


@dp.callback_query(F.data == "acceptVIP_ua")
async def give_id_ua(callback: types.CallbackQuery, state: FSMContext):
    global curr_lang
    if curr_lang == 'ru':

        return 0
    buttons = [
        [
            types.InlineKeyboardButton(text="Російська🇷🇺", callback_data="ru_lang_give_id"),
            types.InlineKeyboardButton(text='Українська🇺🇦', callback_data="ua_lang_give_id")
        ],
        [types.InlineKeyboardButton(text='Перевiрити ID', callback_data='agreeID_ua')],
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    await callback.message.answer(texting.text211_ua, reply_markup=keyboard)
    await callback.message.answer_video(
        video='BQACAgIAAxkBAAIByWZ0xMbrv_Ts54nS7rCeO700Y67NAAIvUgACauUAAUu_1-xCNtjo_zUE')
    await state.set_state(Talking.inputID)
    await callback.answer()


@dp.callback_query(F.data == "ru_lang_give_id")
async def set_ru_lang(callback: types.CallbackQuery):
    buttons = [
        [
            types.InlineKeyboardButton(text="Русский🇷🇺", callback_data="ru_lang_give_id"),
            types.InlineKeyboardButton(text='Украинский🇺🇦', callback_data="ua_lang_give_id")
        ],
        [types.InlineKeyboardButton(text='Проверить ID', callback_data='agreeID_ru')],
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    try:
        await callback.message.edit_text(text=texting.text211_ru, reply_markup=keyboard)
    except Exception:
        await callback.answer()


@dp.callback_query(F.data == "ua_lang_give_id")
async def set_ua_lang(callback: types.CallbackQuery):
    buttons = [
        [
            types.InlineKeyboardButton(text="Російська🇷🇺", callback_data="ru_lang_give_id"),
            types.InlineKeyboardButton(text='Українська🇺🇦', callback_data="ua_lang_give_id")
        ],
        [types.InlineKeyboardButton(text='Перевiрити ID', callback_data='agreeID_ua')],
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    try:
        await callback.message.edit_text(text=texting.text211_ua, reply_markup=keyboard)
    except Exception:
        await callback.answer()


@dp.callback_query(F.data == "agreeID_ru", Talking.inputID)
async def input_id(callback: types.CallbackQuery, state: FSMContext):
    global curr_lang
    curr_lang = 'ru'
    buttons = [
        [
            types.InlineKeyboardButton(text="Русский🇷🇺", callback_data="ru_lang_input_id"),
            types.InlineKeyboardButton(text='Украинский🇺🇦', callback_data="ua_lang_input_id")
        ]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    await callback.message.answer(texting.text21_ru, reply_markup=keyboard)
    await state.set_state(Talking.setID)
    await callback.answer()


@dp.callback_query(F.data == "agreeID_ua", Talking.inputID)
async def input_id(callback: types.CallbackQuery, state: FSMContext):
    global curr_lang
    curr_lang = 'ua'
    buttons = [
        [
            types.InlineKeyboardButton(text="Російська🇷🇺", callback_data="ru_lang_input_id"),
            types.InlineKeyboardButton(text='Українська🇺🇦', callback_data="ua_lang_input_id")
        ]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    await callback.message.answer(texting.text21_ua, reply_markup=keyboard)
    await state.set_state(Talking.setID)
    await callback.answer()


@dp.callback_query(F.data == "ua_lang_input_id")
async def set_ua_lang(callback: types.CallbackQuery):
    global curr_lang
    curr_lang = 'ua'
    buttons = [
        [
            types.InlineKeyboardButton(text="Російська🇷🇺", callback_data="ru_lang_input_id"),
            types.InlineKeyboardButton(text='Українська🇺🇦', callback_data="ua_lang_input_id")
        ]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    try:
        await callback.message.edit_text(text=texting.text21_ua, reply_markup=keyboard)
    except Exception:
        await callback.answer()


@dp.callback_query(F.data == "ru_lang_input_id")
async def set_ru_lang(callback: types.CallbackQuery):
    global curr_lang
    curr_lang = 'ru'
    buttons = [
        [
            types.InlineKeyboardButton(text="Русский🇷🇺", callback_data="ru_lang_input_id"),
            types.InlineKeyboardButton(text='Украинский🇺🇦', callback_data="ua_lang_input_id")
        ]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    try:
        await callback.message.edit_text(text=texting.text21_ru, reply_markup=keyboard)
    except Exception:
        await callback.answer()


@dp.message(Talking.setID)
async def set_id(message: types.Message, state: FSMContext):
    global curr_lang
    if curr_lang == 'ru':
        buttons = [
            [
                types.InlineKeyboardButton(text="Русский🇷🇺", callback_data="ru_wrong_lang"),
                types.InlineKeyboardButton(text='Украинский🇺🇦', callback_data="ua_wrong_lang")
            ]
        ]
        keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
        id = message.text
        if isNum(id) is True:
            print('otherflag = requests.get(link id)')
            if 5 > 3:
                buttons = [
                    [
                        types.InlineKeyboardButton(text="Русский🇷🇺", callback_data="ru_right_lang"),
                        types.InlineKeyboardButton(text='Украинский🇺🇦', callback_data="ua_right_lang")
                    ]
                ]
                keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
                await message.answer(text=texting.text3_right_ru, reply_markup=keyboard)
                await message.answer_video(
                    video='BQACAgIAAxkBAAIBx2Z0xLpyHAmlVhSxU-bLYavWwqS9AAIuUgACauUAAUtL1FSCrR0tajUE')
                await state.clear()
                return 1
        await message.answer(text=texting.text3_wrong_ru, reply_markup=keyboard)
        await message.answer_video(video='BQACAgIAAxkBAAIBxWZ0xJSXeaQC0Cmgc_CX03RRvw3bAAIrUgACauUAAUt-FPa8zvs6kjUE')
    else:
        buttons = [
            [
                types.InlineKeyboardButton(text="Російська🇷🇺", callback_data="ru_wrong_lang"),
                types.InlineKeyboardButton(text='Українська🇺🇦', callback_data="ua_wrong_lang")
            ]
        ]
        keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
        id = message.text
        if isNum(id) is True:
            print('otherflag = requests.get(link id)')
            if 5 > 3:
                buttons = [
                    [
                        types.InlineKeyboardButton(text="Російська🇷🇺", callback_data="ru_right_lang"),
                        types.InlineKeyboardButton(text='Українська🇺🇦', callback_data="ua_right_lang")
                    ]
                ]
                keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
                await message.answer(text=texting.text3_right_ua, reply_markup=keyboard)
                await message.answer_video(
                    video='BQACAgIAAxkBAAIBx2Z0xLpyHAmlVhSxU-bLYavWwqS9AAIuUgACauUAAUtL1FSCrR0tajUE')
                await state.clear()
                return 1
        await message.answer(text=texting.text3_wrong_ua, reply_markup=keyboard)
        await message.answer_video(video='BQACAgIAAxkBAAIBxWZ0xJSXeaQC0Cmgc_CX03RRvw3bAAIrUgACauUAAUt-FPa8zvs6kjUE')


@dp.callback_query(F.data == "ru_wrong_lang")
async def ru_wrong_set(callback: types.CallbackQuery, state: FSMContext):
    buttons = [
        [
            types.InlineKeyboardButton(text="Русский🇷🇺", callback_data="ru_wrong_lang"),
            types.InlineKeyboardButton(text='Украинский🇺🇦', callback_data="ua_wrong_lang")
        ]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    try:
        await callback.message.edit_text(text=texting.text3_wrong_ru, reply_markup=keyboard)
    except Exception:
        await callback.answer()


@dp.callback_query(F.data == "ua_wrong_lang")
async def ua_wrong_set(callback: types.CallbackQuery, state: FSMContext):
    buttons = [
        [
            types.InlineKeyboardButton(text="Російська🇷🇺", callback_data="ru_wrong_lang"),
            types.InlineKeyboardButton(text='Українська🇺🇦', callback_data="ua_wrong_lang")
        ]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    try:
        await callback.message.edit_text(text=texting.text3_wrong_ua, reply_markup=keyboard)
    except Exception:
        await callback.answer()


@dp.callback_query(F.data == "ru_right_lang")
async def ru_right_set(callback: types.CallbackQuery, state: FSMContext):
    buttons = [
        [
            types.InlineKeyboardButton(text="Русский🇷🇺", callback_data="ru_right_lang"),
            types.InlineKeyboardButton(text='Украинский🇺🇦', callback_data="ua_right_lang")
        ]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    if 5 > 3:
        try:
            await callback.message.edit_text(text=texting.text3_right_ru, reply_markup=keyboard)
        except Exception:
            await callback.answer()
        await state.clear()


@dp.callback_query(F.data == "ua_right_lang")
async def ua_right_set(callback: types.CallbackQuery, state: FSMContext):
    buttons = [
        [
            types.InlineKeyboardButton(text="Російська🇷🇺", callback_data="ru_right_lang"),
            types.InlineKeyboardButton(text='Українська🇺🇦', callback_data="ua_right_lang")
        ]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    if 5 > 3:
        try:
            await callback.message.edit_text(text=texting.text3_right_ua, reply_markup=keyboard)
        except Exception:
            await callback.answer()
        await state.clear()


# Запуск процесса поллинга новых апдейтов
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())