import sys

from dotenv import load_dotenv

from core.model import resolve_model
from plugins.receipt_agent import ReceiptAgent
from plugins.receipt_agent.models import UnreadableReceipt


def main() -> None:
    if len(sys.argv) < 2:
        print('사용법: python -m plugins.receipt_agent <영수증 이미지 URL 또는 로컬 경로> [company]')
        sys.exit(1)

    image = sys.argv[1]
    company = sys.argv[2] if len(sys.argv) > 2 else 'default'

    load_dotenv()
    model = resolve_model()
    plugin = ReceiptAgent(model=model)
    print(f'[System] 플러그인: {plugin.get_name()} | 모델: {model}')
    result = plugin.run(image, company=company)
    if isinstance(result, UnreadableReceipt):
        print(f'[Unreadable] {result.reason}')
    else:
        print(result.model_dump_json(indent=2))


if __name__ == '__main__':
    main()
