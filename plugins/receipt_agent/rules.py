from .models import ExpenseCategory, Receipt

# 예시값임. 실제 회사 정산 규정으로 교체해서 쓸 것.
# ponytail: dict 하드코딩, 회사 늘어나면 DB/설정파일로 옮기기
# models.ExpenseCategory 전체를 다 커버해야 함 (self_check가 검증)
COMPANY_ACCOUNT_RULES: dict[str, dict[str, str]] = {
    'default': {
        '카페': '복리후생비',
        '식당': '식대',
        '편의점': '복리후생비',
        '택시': '교통비',
        '숙박': '출장비',
        '마트': '소모품비',
        '주유소': '차량유지비',
        '수리': '수선비',
        '사무용품': '소모품비',
        '통신': '통신비',
        '기타': '기타경비',
    },
    'acme': {
        '카페': '회의비',
        '식당': '접대비',
        '편의점': '소모품비',
        '택시': '여비교통비',
        '숙박': '여비교통비',
        '마트': '소모품비',
        '주유소': '차량유지비',
        '수리': '수선비',
        '사무용품': '소모품비',
        '통신': '통신비',
        '기타': '기타경비',
    },
}


def assign_account_code(receipt: Receipt, company: str = 'default') -> str:
    """AI가 분류한 category를 회사별 정산 규정에 맞는 계정과목으로 매핑"""
    if company not in COMPANY_ACCOUNT_RULES:
        known = ', '.join(COMPANY_ACCOUNT_RULES)
        raise ValueError(f'등록 안 된 회사: "{company}". 등록된 회사: {known}')
    return COMPANY_ACCOUNT_RULES[company][receipt.category]


def missing_categories(company: str) -> set[ExpenseCategory]:
    """해당 회사 규정에서 빠진 카테고리 확인용 (신규 회사 등록 시 체크)"""
    rules = COMPANY_ACCOUNT_RULES.get(company, {})
    return set(ExpenseCategory.__args__) - set(rules)
