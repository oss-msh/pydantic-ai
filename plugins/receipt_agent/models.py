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


class UnreadableReceipt(BaseModel):
    """영수증이 아니거나 너무 흐려서 읽을 수 없을 때"""

    reason: str = Field(description='왜 못 읽었는지 (예: 영수증이 아님, 너무 흐림, 잘림)')


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
                    f'"{item.name}" 금액 불일치: 수량({item.quantity}) * 단가({item.unit_price}) '
                    f'= {expected}원인데 amount는 {item.amount}원으로 읽음. 수량/단가/금액 중 '
                    '하나를 이미지에서 잘못 읽었을 가능성이 높습니다. 값을 억지로 끼워맞추지 말고, '
                    '이미지를 다시 확인해서 실제로 인쇄된 숫자로 고치세요.'
                )

        items_sum = sum(item.amount for item in self.items)
        if items_sum != self.total:
            raise ValueError(
                f'총액 불일치: 품목 금액 합계는 {items_sum}원인데 total은 {self.total}원으로 읽음. '
                '품목 금액 또는 총액 중 하나를 이미지에서 잘못 읽었을 가능성이 높습니다. '
                '값을 억지로 끼워맞추지 말고, 이미지를 다시 확인해서 실제로 인쇄된 숫자로 고치세요.'
            )
        return self
