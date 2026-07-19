"""LLM 호출 없이 순수 로직(금액 검증, 계정과목 매핑)만 확인하는 self-check"""

from .models import ExpenseCategory, Receipt
from .rules import COMPANY_ACCOUNT_RULES, assign_account_code, missing_categories


def _make_receipt(**overrides) -> dict:
    base = dict(
        merchant='스타벅스 강남점',
        purchased_at='2024-03-15T14:32:00',
        category='카페',
        items=[{'name': '아메리카노', 'quantity': 2, 'unit_price': 4500, 'amount': 9000}],
        total=9000,
    )
    base.update(overrides)
    return base


def test_valid_receipt_passes():
    Receipt.model_validate(_make_receipt())


def test_item_math_error_rejected():
    bad_item = {'name': '아메리카노', 'quantity': 2, 'unit_price': 4500, 'amount': 8000}
    try:
        Receipt.model_validate(_make_receipt(items=[bad_item]))
        raise AssertionError('금액 불일치를 잡아내지 못함')
    except ValueError as e:
        assert '금액 불일치' in str(e)


def test_total_math_error_rejected():
    try:
        Receipt.model_validate(_make_receipt(total=99999))
        raise AssertionError('총액 불일치를 잡아내지 못함')
    except ValueError as e:
        assert '총액 불일치' in str(e)


def test_assign_account_code_default_and_company():
    receipt = Receipt.model_validate(_make_receipt())
    assert assign_account_code(receipt, company='default') == '복리후생비'
    assert assign_account_code(receipt, company='acme') == '회의비'


def test_category_is_fixed_enum_not_free_text():
    try:
        Receipt.model_validate(_make_receipt(category='알수없음업종'))
        raise AssertionError('목록에 없는 category를 거르지 못함')
    except ValueError:
        pass


def test_every_company_covers_all_categories():
    for company in COMPANY_ACCOUNT_RULES:
        missing = missing_categories(company)
        assert not missing, f'{company}에 빠진 카테고리: {missing}'


def test_repair_category_maps_correctly():
    receipt = Receipt.model_validate(_make_receipt(
        merchant='컴프코리아 컴퓨터수리센터',
        category='수리',
        items=[{'name': 'SSD 교체', 'quantity': 1, 'unit_price': 80000, 'amount': 80000}],
        total=80000,
    ))
    assert assign_account_code(receipt, company='default') == '수선비'


if __name__ == '__main__':
    test_valid_receipt_passes()
    test_item_math_error_rejected()
    test_total_math_error_rejected()
    test_assign_account_code_default_and_company()
    test_category_is_fixed_enum_not_free_text()
    test_every_company_covers_all_categories()
    test_repair_category_maps_correctly()
    print('[OK] receipt_agent self-check 통과')
