import mimetypes
from pathlib import Path

from pydantic import BaseModel
from pydantic_ai import Agent, BinaryContent, ImageUrl

from core.base_agent import BaseAgent

from .models import Receipt
from .rules import assign_account_code

INSTRUCTIONS = """당신은 영수증 이미지를 정제하는 어시스턴트입니다.
입력은 사진/스캔된 영수증 이미지입니다. 각도, 조명, 흐릿함 등으로 글자가 불규칙하게 보일 수 있습니다.

가맹점명, 결제일시, 품목 리스트(품목명/수량/단가/금액), 총액을 추출하세요.
- 품목별 금액은 반드시 수량 * 단가와 일치해야 합니다.
- 총액은 반드시 모든 품목 금액의 합과 일치해야 합니다.
- 검증 오류 메시지를 받으면 지시한 대로 다시 계산해서 고치세요.
- category는 정해진 목록 중에서만 골라야 합니다. 애매하면 "기타"로 분류하세요.
- 이미지에서 읽을 수 없는 값은 지어내지 마세요."""


class ExpenseResult(BaseModel):
    receipt: Receipt
    company: str
    account_code: str


def _to_image_content(image: str) -> ImageUrl | BinaryContent:
    if image.startswith('http://') or image.startswith('https://'):
        return ImageUrl(url=image)
    data = Path(image).read_bytes()
    media_type = mimetypes.guess_type(image)[0] or 'image/jpeg'
    return BinaryContent(data=data, media_type=media_type)


class ReceiptAgent(BaseAgent):
    """영수증 이미지를 구조화하고 회사별 계정과목으로 자동 매핑하는 플러그인"""

    def __init__(self, model: str):
        self.agent = Agent(model, instructions=INSTRUCTIONS, output_type=Receipt)

    def get_name(self) -> str:
        return 'receipt_agent'

    def run(self, image: str, company: str = 'default') -> ExpenseResult:
        """image: 이미지 URL(http/https) 또는 로컬 파일 경로"""
        content = ['이 영수증 이미지에서 정보를 추출해줘.', _to_image_content(image)]
        receipt: Receipt = self.agent.run_sync(content).output
        account_code = assign_account_code(receipt, company=company)
        return ExpenseResult(receipt=receipt, company=company, account_code=account_code)
