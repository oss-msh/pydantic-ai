"""LLM 호출 없이 순수 로직(금액 검증, 계정과목 매핑)만 확인하는 self-check"""

from .models import Receipt
from .rules import assign_account_code


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
        assert '금액 오류' in str(e)


def test_total_math_error_rejected():
    try:
        Receipt.model_validate(_make_receipt(total=99999))
        raise AssertionError('총액 불일치를 잡아내지 못함')
    except ValueError as e:
        assert '총액 오류' in str(e)


def test_assign_account_code_default_and_company():
    receipt = Receipt.model_validate(_make_receipt())
    assert assign_account_code(receipt, company='default') == '복리후생비'
    assert assign_account_code(receipt, company='acme') == '회의비'


def test_assign_account_code_unknown_category_falls_back():
    receipt = Receipt.model_validate(_make_receipt(category='알수없음'))
    assert assign_account_code(receipt, company='default') == '기타경비'


if __name__ == '__main__':
    test_valid_receipt_passes()
    test_item_math_error_rejected()
    test_total_math_error_rejected()
    test_assign_account_code_default_and_company()
    test_assign_account_code_unknown_category_falls_back()
    print('[OK] receipt_agent self-check 통과')
