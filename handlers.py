#
from aiogram import types, Dispatcher
from aiogram.filters.command import Command
from aiogram import F
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from data.questions import QUESTIONS
from db import get_quiz_index, get_user_score, update_quiz_index, update_user_score

# Ф-ция генерации кнопок
def generate_options_keyboard(answer_options, right_answer):
    builder = InlineKeyboardBuilder()
    for option in answer_options:
        builder.add(types.InlineKeyboardButton(
            text=option,
            callback_data=f'{option}:{"right" if option == right_answer else "wrong"}'
        ))
    builder.adjust(1)
    return builder.as_markup()

async def right_answer(callback: types.CallbackQuery):
    selected_option = callback.data.split(':')[0]
    await callback.message.answer(f'Верно. Ваш ответ: {selected_option}')
    current_question_index = await get_quiz_index(callback.from_user.id)
    current_score = await get_user_score(callback.from_user.id)
    current_question_index += 1
    current_score += 1
    await update_quiz_index(callback.from_user.id, current_question_index)
    await update_user_score(callback.from_user.id, current_score)

    if current_question_index < len(QUESTIONS):
        await get_question(callback.message, callback.from_user.id)
    else:
        await callback.message.answer(f'Квиз завершен. Количество правильных ответов: {current_score}')

async def wrong_answer(callback: types.CallbackQuery):
    selected_option = callback.data.split(':')[0]
    current_question_index = await get_quiz_index(callback.from_user.id)
    current_score = await get_user_score(callback.from_user.id)
    correct_option = QUESTIONS[current_question_index]['correct_option']
    await callback.message.answer(f"Неверно. Ваш ответ: {selected_option}. Правильный ответ: {QUESTIONS[current_question_index]['options'][correct_option]}")
    current_question_index += 1
    await update_quiz_index(callback.from_user.id, current_question_index)
    await update_user_score(callback.from_user.id, current_score)

    if current_question_index < len(QUESTIONS):
        await get_question(callback.message, callback.from_user.id)
    else:
        await callback.message.answer(f'Квиз завершен. Количество правильных ответов: {current_score}')

async def cmd_start(message: types.Message):
    builder = ReplyKeyboardBuilder()
    builder.add(types.KeyboardButton(text='Начать игру'))
    await message.answer('Добро пожаловать!', reply_markup=builder.as_markup(resize_keyboard=True))

async def get_question(message, user_id):
    current_question_index = await get_quiz_index(user_id)
    correct_index = QUESTIONS[current_question_index]['correct_option']
    opts = QUESTIONS[current_question_index]['options']
    kb = generate_options_keyboard(opts, opts[correct_index])
    await message.answer(f"{QUESTIONS[current_question_index]['question']}", reply_markup=kb)

async def new_quiz(message):
    user_id = message.from_user.id
    current_question_index = 0 
    new_score = 0
    await update_quiz_index(user_id, current_question_index)
    await update_user_score(user_id, new_score)
    await get_question(message, user_id)

async def cmd_quiz(message: types.Message):
    await message.answer("Давайте начнем квиз!")
    await new_quiz(message)

def register_handlers(dp: Dispatcher):
    dp.message.register(cmd_start, Command("start"))
    dp.message.register(cmd_quiz, Command("quiz"))
    dp.message.register(cmd_quiz, F.text == "Начать игру")
    dp.callback_query.register(right_answer, F.data.contains(':right'))
    dp.callback_query.register(wrong_answer, F.data.contains(':wrong'))
