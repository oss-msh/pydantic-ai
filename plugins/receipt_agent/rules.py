from .models import Receipt

# 예시값임. 실제 회사 정산 규정으로 교체해서 쓸 것.
# ponytail: dict 하드코딩, 회사 늘어나면 DB/설정파일로 옮기기
COMPANY_ACCOUNT_RULES: dict[str, dict[str, str]] = {
    'default': {
        '카페': '복리후생비',
        '식당': '식대',
        '편의점': '복리후생비',
        '택시': '교통비',
        '숙박': '출장비',
        '기타': '기타경비',
    },
    'acme': {
        '카페': '회의비',
        '식당': '접대비',
        '편의점': '소모품비',
        '택시': '여비교통비',
        '숙박': '여비교통비',
        '기타': '기타경비',
    },
}


def assign_account_code(receipt: Receipt, company: str = 'default') -> str:
    """AI가 분류한 category를 회사별 정산 규정에 맞는 계정과목으로 매핑"""
    rules = COMPANY_ACCOUNT_RULES.get(company, COMPANY_ACCOUNT_RULES['default'])
    return rules.get(receipt.category, rules['기타'])
