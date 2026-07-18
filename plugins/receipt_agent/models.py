from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field, model_validator

# rules.py의 COMPANY_ACCOUNT_RULES 키와 반드시 1:1로 맞출 것
ExpenseCategory = Literal[
    '카페', '식당', '택시', '숙박', '편의점', '마트', '주유소', '수리', '사무용품', '통신', '기타',
]


class ReceiptItem(BaseModel):
    name: str
    quantity: int = Field(gt=0)
    unit_price: int = Field(ge=0, description='원 단위 단가')
    amount: int = Field(ge=0, description='원 단위 금액 (quantity * unit_price)')


class Receipt(BaseModel):
    merchant: str
    purchased_at: datetime
    category: ExpenseCategory
    items: list[ReceiptItem]
    total: int = Field(ge=0, description='원 단위 총액')

    @model_validator(mode='after')
    def check_math(self) -> 'Receipt':
        for item in self.items:
            expected = item.quantity * item.unit_price
            if expected != item.amount:
                raise ValueError(
                    f'"{item.name}" 금액 오류: 수량({item.quantity}) * 단가({item.unit_price}) '
                    f'= {expected}원 이어야 하는데 {item.amount}원으로 기재됨. 다시 계산해서 amount를 고치세요.'
                )

        items_sum = sum(item.amount for item in self.items)
        if items_sum != self.total:
            raise ValueError(
                f'총액 오류: 품목 금액 합계는 {items_sum}원인데 total은 {self.total}원으로 기재됨. '
                '다시 계산해서 total을 고치세요.'
            )
        return self
