import mimetypes
from pathlib import Path

from pydantic import BaseModel
from pydantic_ai import Agent, BinaryContent, ImageUrl

from core.base_agent import BaseAgent

from .models import Receipt, UnreadableReceipt
from .rules import assign_account_code

INSTRUCTIONS = """당신은 영수증 이미지를 정제하는 어시스턴트입니다.
입력은 사진/스캔된 영수증 이미지입니다. 각도, 조명, 흐릿함 등으로 글자가 불규칙하게 보일 수 있습니다.

가맹점명, 결제일시, 품목 리스트(품목명/수량/단가/금액), 총액을 추출하세요.
- 품목별 금액은 반드시 수량 * 단가와 일치해야 합니다.
- 총액은 반드시 모든 품목 금액의 합과 일치해야 합니다.
- 검증 오류 메시지를 받으면, 산수만 맞춰서 값을 지어내지 말고 이미지를 다시 판독해서 잘못 읽은 숫자를 찾아 고치세요.
- category는 정해진 목록 중에서만 골라야 합니다. 애매하면 "기타"로 분류하세요.
- 이미지에서 읽을 수 없는 값은 지어내지 마세요.
- 이미지가 영수증이 아니거나, 너무 흐리거나 잘려서 핵심 정보(가맹점/금액)를 읽을 수 없으면
  절대 값을 지어내지 말고 반드시 실패 응답으로 이유를 알리세요."""


class ExpenseResult(BaseModel):
    receipt: Receipt
    company: str
    account_code: str


# Gemini/OpenAI 등 주요 vision 모델이 공통으로 받는 포맷. HEIC(아이폰 기본), PDF 등은 여기서 걸러냄
_SUPPORTED_IMAGE_TYPES = {'image/jpeg', 'image/png', 'image/webp', 'image/gif'}
# Gemini inline data 제한(20MB) 기준. 넘으면 리사이즈 필요
_MAX_LOCAL_IMAGE_BYTES = 20 * 1024 * 1024


def _check_media_type(image: str, media_type: str | None) -> None:
    if media_type is not None and media_type not in _SUPPORTED_IMAGE_TYPES:
        raise ValueError(
            f'지원 안 하는 이미지 포맷: "{media_type}" ({image}). '
            f'{", ".join(sorted(_SUPPORTED_IMAGE_TYPES))} 중 하나로 변환해서 다시 시도하세요.'
        )


def _to_image_content(image: str) -> ImageUrl | BinaryContent:
    if image.startswith('http://') or image.startswith('https://'):
        _check_media_type(image, mimetypes.guess_type(image)[0])
        return ImageUrl(url=image)

    media_type = mimetypes.guess_type(image)[0] or 'image/jpeg'
    _check_media_type(image, media_type)

    size = Path(image).stat().st_size
    if size > _MAX_LOCAL_IMAGE_BYTES:
        raise ValueError(
            f'이미지 용량 초과: {size / 1024 / 1024:.1f}MB ({image}). '
            f'{_MAX_LOCAL_IMAGE_BYTES // 1024 // 1024}MB 이하로 리사이즈해서 다시 시도하세요.'
        )

    return BinaryContent(data=Path(image).read_bytes(), media_type=media_type)


class ReceiptAgent(BaseAgent):
    """영수증 이미지를 구조화하고 회사별 계정과목으로 자동 매핑하는 플러그인"""

    def __init__(self, model: str):
        self.agent = Agent(
            model,
            instructions=INSTRUCTIONS,
            output_type=[Receipt, UnreadableReceipt],
            retries={'output': 2},
        )

    def get_name(self) -> str:
        return 'receipt_agent'

    def run(self, image: str, company: str = 'default') -> ExpenseResult | UnreadableReceipt:
        """image: 이미지 URL(http/https) 또는 로컬 파일 경로"""
        content = ['이 영수증 이미지에서 정보를 추출해줘.', _to_image_content(image)]
        output = self.agent.run_sync(content).output
        if isinstance(output, UnreadableReceipt):
            return output
        account_code = assign_account_code(output, company=company)
        return ExpenseResult(receipt=output, company=company, account_code=account_code)
