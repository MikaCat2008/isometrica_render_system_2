from typing import Any

from ..base import Update


class AnswerUpdate(Update):
    result: Any
    answer_id: int
