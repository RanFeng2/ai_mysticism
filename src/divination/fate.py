from fastapi import HTTPException
from src.models import DivinationBody
from .base import DivinationFactory

SYS_PROMPT = "你是一个姻缘助手，我给你发两个人的名字，用逗号隔开，"\
    "你来随机说一下，这两个人之间的缘分如何？"\
    "如果你认为双方合适，请你说明原因。"\
    "如果双方不合适，也请列出原因。"

class Fate(DivinationFactory):

    divination_type = "fate"

    def build_prompt(self, divination_body: DivinationBody) -> tuple[str, str]:
        fate = divination_body.fate
        if not fate:
            raise HTTPException(status_code=400, detail="Fate is required")
        if len(fate.name1) > 40 or len(fate.name2) > 40:
            raise HTTPException(status_code=400, detail="Prompt too long")
        prompt = f'{fate.name1}, {fate.name2}'
        return prompt, SYS_PROMPT
