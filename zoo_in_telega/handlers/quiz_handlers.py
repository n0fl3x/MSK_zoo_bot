import logging

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram import types, Dispatcher

from bot_settings import bot
from commands.quiz_commands import START_QUIZ_COMMAND, CANCEL_COMMAND
from texts.answer_buttons_text import *

from handler_filters import (
    cancel_inline_btn_filter,
    question_filter_1,
    question_filter_2,
    question_filter_3,
    question_filter_4,
    question_filter_5,
)

from texts.questions_text import (
    QUESTION_1,
    QUESTION_2,
    QUESTION_3,
    QUESTION_4,
    QUESTION_5,
    END_MESSAGE,
    ALREADY_ANSWERED,
    ALREADY_FINISHED,
)

from keyboards.quiz_kb import (
    inline_keyboard_1,
    inline_keyboard_2,
    inline_keyboard_3,
    inline_keyboard_4,
    inline_keyboard_5,
)

from texts.static_commands_text import (
    NOT_NONE_STATE_CANCEL_COMMAND_TEXT,
    NONE_STATE_CANCEL_COMMAND_TEXT,
)


# -------------
# Quiz handlers
class CurrentQuestion(StatesGroup):
    """Класс для фиксации состояний ожидания ответа на определённый по счёту вопрос."""

    question_1 = State()
    question_2 = State()
    question_3 = State()
    question_4 = State()
    question_5 = State()


async def cancel_command(message: types.Message, state: FSMContext) -> None:
    """Функция-обработчик команды /cancel, введённой вручную. Останавливает текущий опрос."""

    current_state = await state.get_state()

    if current_state is None:
        logging.info(f'User with ID {message.from_user.id} tried to cancel empty state.')
        await message.answer(text=NONE_STATE_CANCEL_COMMAND_TEXT)
        return

    logging.info(f'User with ID {message.from_user.id} cancelled quiz at {current_state} state by command.')
    await state.reset_state()
    await message.answer(text=NOT_NONE_STATE_CANCEL_COMMAND_TEXT)


async def cancel_inline_button(callback: types.CallbackQuery, state: FSMContext) -> None:
    """Функция-обработчик команды /cancel, вызванная через инлайн-кнопку. Останавливает текущий опрос."""

    current_state = await state.get_state()

    if current_state is None:
        logging.info(f'User with ID {callback.from_user.id} tried to cancel empty state.')
        await callback.answer()
        await callback.message.answer(text=NONE_STATE_CANCEL_COMMAND_TEXT)
        return

    logging.info(f'User with ID {callback.from_user.id} cancelled quiz at {current_state} state by inline button.')
    await state.reset_state()
    await callback.answer()
    await callback.message.answer(text=NOT_NONE_STATE_CANCEL_COMMAND_TEXT)


async def animal_command(message: types.Message, state: FSMContext) -> None:
    """Функция-обработчик команды запуска опроса."""

    current_state = await state.get_state()

    if current_state is None:
        logging.info(f'User with ID {message.from_user.id} started new quiz.')
    else:
        await message.answer(text='Вы начали опрос заново.')
        logging.info(f'User with ID {message.from_user.id} restarted quiz.')

    await message.answer(
        text=QUESTION_1,
        reply_markup=inline_keyboard_1
    )
    await CurrentQuestion.question_1.set()


# TODO: реализовать проверку ответа на каждый НЕ последний вопрос, когда опрос уже завершён
async def process_question_1(callback_query: types.CallbackQuery, state: FSMContext):
    cur_state = await state.get_state()

    if (callback_query.data == f'{answer_1_1}'
        or callback_query.data == f'{answer_1_2}'
        or callback_query.data == f'{answer_1_3}'
        or callback_query.data == f'{answer_1_4}') \
            and cur_state == 'CurrentQuestion:question_1':
        await bot.answer_callback_query(callback_query.id)
        await bot.send_message(
            chat_id=callback_query.from_user.id,
            text=callback_query.data,
        )
        logging.info(f'User with ID {callback_query.from_user.id} answered '
                     f'({callback_query.data}) the 1st question.')
        await CurrentQuestion.next()
        await bot.send_message(
            chat_id=callback_query.from_user.id,
            text=QUESTION_2,
            reply_markup=inline_keyboard_2,
        )

    elif (callback_query.data == f'{answer_1_1}'
          or callback_query.data == f'{answer_1_2}'
          or callback_query.data == f'{answer_1_3}'
          or callback_query.data == f'{answer_1_4}') \
            and cur_state != 'CurrentQuestion:question_1':
        await bot.answer_callback_query(callback_query.id)
        await bot.send_message(
            chat_id=callback_query.from_user.id,
            text=f'{ALREADY_ANSWERED}',
        )
        logging.info(f'User with ID {callback_query.from_user.id} tried to '
                     f'answer ({callback_query.data}) the 1st question again.')

    else:
        await process_question_2(callback_query=callback_query, state=state)


async def process_question_2(callback_query: types.CallbackQuery, state: FSMContext):
    cur_state = await state.get_state()

    if (callback_query.data == f'{answer_2_1}'
        or callback_query.data == f'{answer_2_2}'
        or callback_query.data == f'{answer_2_3}'
        or callback_query.data == f'{answer_2_4}') \
            and cur_state == 'CurrentQuestion:question_2':
        await bot.answer_callback_query(callback_query.id)
        await bot.send_message(
            chat_id=callback_query.from_user.id,
            text=callback_query.data,
        )
        logging.info(f'User with ID {callback_query.from_user.id} answered '
                     f'({callback_query.data}) the 2nd question.')
        await CurrentQuestion.next()
        await bot.send_message(
            chat_id=callback_query.from_user.id,
            text=QUESTION_3,
            reply_markup=inline_keyboard_3,
        )

    elif (callback_query.data == f'{answer_2_1}'
          or callback_query.data == f'{answer_2_2}'
          or callback_query.data == f'{answer_2_3}'
          or callback_query.data == f'{answer_2_4}') \
            and cur_state != 'CurrentQuestion:question_2':
        await bot.answer_callback_query(callback_query.id)
        await bot.send_message(
            chat_id=callback_query.from_user.id,
            text=f'{ALREADY_ANSWERED}',
        )
        logging.info(f'User with ID {callback_query.from_user.id} tried to '
                     f'answer ({callback_query.data}) the 2nd question again.')

    else:
        await process_question_3(callback_query=callback_query, state=state)


async def process_question_3(callback_query: types.CallbackQuery, state: FSMContext):
    cur_state = await state.get_state()

    if (callback_query.data == f'{answer_3_1}'
        or callback_query.data == f'{answer_3_2}'
        or callback_query.data == f'{answer_3_3}'
        or callback_query.data == f'{answer_3_4}') \
            and cur_state == 'CurrentQuestion:question_3':
        await bot.answer_callback_query(callback_query.id)
        await bot.send_message(
            chat_id=callback_query.from_user.id,
            text=callback_query.data,
        )
        logging.info(f'User with ID {callback_query.from_user.id} answered '
                     f'({callback_query.data}) the 3rd question.')
        await CurrentQuestion.next()
        await bot.send_message(
            chat_id=callback_query.from_user.id,
            text=QUESTION_4,
            reply_markup=inline_keyboard_4,
        )

    elif (callback_query.data == f'{answer_3_1}'
          or callback_query.data == f'{answer_3_2}'
          or callback_query.data == f'{answer_3_3}'
          or callback_query.data == f'{answer_3_4}') \
            and cur_state != 'CurrentQuestion:question_3':
        await bot.answer_callback_query(callback_query.id)
        await bot.send_message(
            chat_id=callback_query.from_user.id,
            text=f'{ALREADY_ANSWERED}',
        )
        logging.info(f'User with ID {callback_query.from_user.id} tried to '
                     f'answer ({callback_query.data}) the 3rd question again.')

    else:
        await process_question_4(callback_query=callback_query, state=state)


async def process_question_4(callback_query: types.CallbackQuery, state: FSMContext):
    cur_state = await state.get_state()

    if (callback_query.data == f'{answer_4_1}'
        or callback_query.data == f'{answer_4_2}'
        or callback_query.data == f'{answer_4_3}'
        or callback_query.data == f'{answer_4_4}') \
            and cur_state == 'CurrentQuestion:question_4':
        await bot.answer_callback_query(callback_query.id)
        await bot.send_message(
            chat_id=callback_query.from_user.id,
            text=callback_query.data,
        )
        logging.info(f'User with ID {callback_query.from_user.id} answered '
                     f'({callback_query.data}) the 4th question.')
        await CurrentQuestion.next()
        await bot.send_message(
            chat_id=callback_query.from_user.id,
            text=QUESTION_5,
            reply_markup=inline_keyboard_5,
        )

    elif (callback_query.data == f'{answer_4_1}'
          or callback_query.data == f'{answer_4_2}'
          or callback_query.data == f'{answer_4_3}'
          or callback_query.data == f'{answer_4_4}') \
            and cur_state != 'CurrentQuestion:question_4':
        await bot.answer_callback_query(callback_query.id)
        await bot.send_message(
            chat_id=callback_query.from_user.id,
            text=f'{ALREADY_ANSWERED}',
        )
        logging.info(f'User with ID {callback_query.from_user.id} tried to '
                     f'answer ({callback_query.data}) the 4th question again.')

    else:
        await process_question_5(callback_query=callback_query, state=state)


async def process_question_5(callback_query: types.CallbackQuery, state: FSMContext):
    cur_state = await state.get_state()

    if (callback_query.data == f'{answer_5_1}'
        or callback_query.data == f'{answer_5_2}'
        or callback_query.data == f'{answer_5_3}'
        or callback_query.data == f'{answer_5_4}') \
            and cur_state == 'CurrentQuestion:question_5':
        await bot.answer_callback_query(callback_query.id)
        await bot.send_message(
            chat_id=callback_query.from_user.id,
            text=callback_query.data,
        )
        logging.info(f'User with ID {callback_query.from_user.id} answered '
                     f'({callback_query.data}) the 5th question.')
        await state.finish()
        await bot.send_message(
            chat_id=callback_query.from_user.id,
            text=END_MESSAGE,
        )

    else:
        await bot.answer_callback_query(callback_query.id)
        await bot.send_message(
            chat_id=callback_query.from_user.id,
            text=f'{ALREADY_FINISHED}',
        )
        logging.info(f'User with ID {callback_query.from_user.id} tried to '
                     f'answer ({callback_query.data}) the 5th question again.')


# ---------------------
# Handlers registration
def register_static_command_handlers(disp: Dispatcher):
    disp.register_message_handler(
        cancel_command,
        commands=[f'{CANCEL_COMMAND}'],
        state='*',
    )
    disp.register_callback_query_handler(
        cancel_inline_button,
        cancel_inline_btn_filter,
        state='*',
    )
    disp.register_message_handler(
        animal_command,
        commands=[f'{START_QUIZ_COMMAND}'],
        state='*',
    )
    disp.register_callback_query_handler(
        process_question_1,
        question_filter_1,
        state='*',
    )
    disp.register_callback_query_handler(
        process_question_2,
        question_filter_2,
        state='*',
    )
    disp.register_callback_query_handler(
        process_question_3,
        question_filter_3,
        state='*',
    )
    disp.register_callback_query_handler(
        process_question_4,
        question_filter_4,
        state='*',
    )
    disp.register_callback_query_handler(
        process_question_5,
        question_filter_5,
        state='*',
    )