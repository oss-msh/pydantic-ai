from pydantic import BaseModel
from pydantic_ai import Agent

from core.base_agent import BaseAgent

from .models import Receipt
from .rules import assign_account_code

INSTRUCTIONS = """당신은 영수증 OCR 텍스트를 정제하는 어시스턴트입니다.
입력은 OCR로 스캔되어 줄바꿈/공백/오타가 불규칙한 영수증 텍스트입니다.

가맹점명, 결제일시, 품목 리스트(품목명/수량/단가/금액), 총액을 추출하세요.
- 품목별 금액은 반드시 수량 * 단가와 일치해야 합니다.
- 총액은 반드시 모든 품목 금액의 합과 일치해야 합니다.
- 검증 오류 메시지를 받으면 지시한 대로 다시 계산해서 고치세요.
- category는 정해진 목록 중에서만 골라야 합니다. 애매하면 "기타"로 분류하세요.
- OCR 텍스트에 없는 값은 지어내지 마세요."""


class ExpenseResult(BaseModel):
    receipt: Receipt
    company: str
    account_code: str


class ReceiptAgent(BaseAgent):
    """영수증 OCR 텍스트를 구조화하고 회사별 계정과목으로 자동 매핑하는 플러그인"""

    def __init__(self, model: str):
        self.agent = Agent(model, instructions=INSTRUCTIONS, output_type=Receipt)

    def get_name(self) -> str:
        return 'receipt_agent'

    def run(self, prompt: str, company: str = 'default') -> ExpenseResult:
        receipt: Receipt = self.agent.run_sync(prompt).output
        account_code = assign_account_code(receipt, company=company)
        return ExpenseResult(receipt=receipt, company=company, account_code=account_code)
