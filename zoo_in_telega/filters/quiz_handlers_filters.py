from aiogram import types

from commands.quiz_commands import CANCEL_COMMAND


"""
Хоть эти фильтры не несут никакой смысловой нагрузки, они были вынесены
в отдельный файл, для их будущей возможной кастомизации.
"""


async def cancel_inline_btn_filter(callback_query: types.CallbackQuery):
    if callback_query.data == f'/{CANCEL_COMMAND}':
        return callback_query


async def question_filter_1(callback_query: types.CallbackQuery):
    return callback_query


async def question_filter_2(callback_query: types.CallbackQuery):
    return callback_query


async def question_filter_3(callback_query: types.CallbackQuery):
    return callback_query


async def question_filter_4(callback_query: types.CallbackQuery):
    return callback_query


async def question_filter_5(callback_query: types.CallbackQuery):
    return callback_query