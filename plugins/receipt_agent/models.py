from datetime import datetime

from pydantic import BaseModel, Field, model_validator


class ReceiptItem(BaseModel):
    name: str
    quantity: int = Field(gt=0)
    unit_price: int = Field(ge=0, description='원 단위 단가')
    amount: int = Field(ge=0, description='원 단위 금액 (quantity * unit_price)')


class Receipt(BaseModel):
    merchant: str
    purchased_at: datetime
    category: str = Field(description='가맹점 업종 한 단어 분류 (예: 카페, 식당, 택시, 숙박, 편의점, 기타)')
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
