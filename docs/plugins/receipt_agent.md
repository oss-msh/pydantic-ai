# receipt_agent

영수증 이미지(URL 또는 로컬 경로)를 읽어 가맹점/일시/품목/부가세/봉사료/할인/총액을 구조화된 스키마로 추출하고, 회사별 정산 규정에 맞는 계정과목으로 자동 분류해주는 플러그인입니다.

- **기여자**: [ruby-kim](https://github.com/ruby-kim)
- **역할**: 영수증 이미지에서 가맹점/일시/품목/부가세/봉사료/할인/총액을 추출하고, 금액 불일치 시 재판독을 유도하며, 읽을 수 없는 이미지는 실패 응답으로 처리하고, 회사별 계정과목으로 자동 매핑
- **실행**: `python -m plugins.receipt_agent <이미지 URL 또는 로컬 경로> [company]`

```bash
python -m plugins.receipt_agent <이미지 URL 또는 로컬 경로> [company]

# self-check (LLM 호출 없이 검증/재시도/매핑 로직 확인)
python -m plugins.receipt_agent.test_receipt_agent
```

`company`를 생략하면 `default` 규정을 사용합니다.

## 입력

- **URL**: `http://`, `https://`로 시작하는 이미지 주소
- **로컬 경로**: 파일 시스템 상의 이미지 경로

허용 포맷은 `image/jpeg`, `image/png`, `image/webp`, `image/gif`뿐입니다. HEIC(아이폰 기본 포맷)나 PDF 등은 `ValueError`로 거부됩니다. 로컬 파일은 20MB(Gemini inline data 제한 기준)를 넘으면 역시 거부되며, 리사이즈 후 재시도해야 합니다.

## 출력

### 정상 인식: `ExpenseResult`

```python
class ExpenseResult(BaseModel):
    receipt: Receipt
    company: str
    account_code: str
```

`Receipt`는 다음을 포함합니다.

- `merchant`, `purchased_at`, `category`(고정 enum), `items`(품목별 이름/수량/단가/금액)
- `tax`, `service_charge`, `discount`(없으면 0)
- `total`

Pydantic `model_validator`가 다음 두 조건을 강제합니다. 어긋나면 `ValueError`가 발생하고 에이전트는 이미지를 다시 판독합니다(억지로 산수만 맞춰 값을 지어내지 않도록 프롬프트에 명시).

1. 품목별 `amount == quantity * unit_price`
2. `total == sum(items.amount) + tax + service_charge - discount`

### 읽을 수 없는 영수증: `UnreadableReceipt`

영수증이 아니거나, 너무 흐리거나 잘려서 가맹점/금액을 읽을 수 없으면 값을 지어내는 대신 이 브랜치로 응답합니다.

```python
class UnreadableReceipt(BaseModel):
    reason: str  # 예: "영수증이 아님", "너무 흐림", "잘림"
```

CLI에서는 `[Unreadable] <reason>` 형태로 출력됩니다.

## 회사별 계정과목 매핑

`rules.py`의 `COMPANY_ACCOUNT_RULES`가 회사(`company`)별로 `category → 계정과목` 매핑을 갖고 있습니다.  
현재 `default`, `acme` 두 예시가 등록되어 있으며, 등록 안 된 회사를 넘기면 `ValueError`(등록된 회사 목록 포함)가 발생합니다. 실제 사용 시에는 이 dict를 회사 정산 규정으로 교체하세요.

## 재시도

`Agent`는 `retries={'output': 2}`로 설정되어 있어, 검증 오류(금액 불일치 등) 발생 시 최대 2회까지 이미지를 다시 판독합니다.
