"""실제 LLM 호출 없이(FunctionModel로 가짜 응답) 검증/재시도/분기 로직을 확인하는 self-check"""

from pydantic_ai import Agent
from pydantic_ai.messages import ModelResponse, ToolCallPart
from pydantic_ai.models.function import FunctionModel

from .models import ExpenseCategory, Receipt, UnreadableReceipt
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


def test_agent_retries_after_bad_math_then_succeeds():
    call_count = {'n': 0}
    bad = _make_receipt(items=[{'name': '물', 'quantity': 2, 'unit_price': 1000, 'amount': 1000}], total=1000)
    good = _make_receipt(items=[{'name': '물', 'quantity': 2, 'unit_price': 1000, 'amount': 2000}], total=2000)

    def fake_model(messages, info):
        call_count['n'] += 1
        data = bad if call_count['n'] == 1 else good
        return ModelResponse(parts=[ToolCallPart(tool_name='final_result_Receipt', args=data)])

    agent = Agent(FunctionModel(fake_model), output_type=[Receipt, UnreadableReceipt], retries={'output': 2})
    result = agent.run_sync('영수증 읽어줘')
    assert call_count['n'] == 2, '검증 실패 후 재시도가 안 일어남'
    assert result.output.total == 2000


def test_agent_returns_unreadable_instead_of_hallucinating():
    def fake_model(messages, info):
        return ModelResponse(parts=[ToolCallPart(
            tool_name='final_result_UnreadableReceipt', args={'reason': '영수증이 아님'},
        )])

    agent = Agent(FunctionModel(fake_model), output_type=[Receipt, UnreadableReceipt], retries={'output': 2})
    result = agent.run_sync('이거 분석해줘')
    assert isinstance(result.output, UnreadableReceipt)
    assert result.output.reason == '영수증이 아님'


if __name__ == '__main__':
    test_valid_receipt_passes()
    test_item_math_error_rejected()
    test_total_math_error_rejected()
    test_assign_account_code_default_and_company()
    test_category_is_fixed_enum_not_free_text()
    test_every_company_covers_all_categories()
    test_repair_category_maps_correctly()
    test_agent_retries_after_bad_math_then_succeeds()
    test_agent_returns_unreadable_instead_of_hallucinating()
    print('[OK] receipt_agent self-check 통과')
