from dotenv import load_dotenv

from core.model import resolve_model
from plugins.receipt_agent import ReceiptAgent

SAMPLE_OCR_TEXT = """스타벅스 강남점
2024.03.15  14:32

아메리카노(T)   2   4500   9000
카페라떼(T)     1   5000   5000

합계          14000원"""


def main() -> None:
    load_dotenv()
    model = resolve_model()
    plugin = ReceiptAgent(model=model)
    print(f'[System] 플러그인: {plugin.get_name()} | 모델: {model}')
    result = plugin.run(SAMPLE_OCR_TEXT, company='default')
    print(result.model_dump_json(indent=2))


if __name__ == '__main__':
    main()
