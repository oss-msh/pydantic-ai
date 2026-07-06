from dotenv import load_dotenv

from core.model import resolve_model
from plugins.sample_package import SamplePackageAgent

DEFAULT_PROMPT = 'pydantic-ai를 한 문장으로 소개해줘.'


def main() -> None:
    load_dotenv()
    model = resolve_model()
    plugin = SamplePackageAgent(model=model)
    print(f'[System] 플러그인: {plugin.get_name()} | 모델: {model}')
    response = plugin.run(DEFAULT_PROMPT)
    print(f'[Agent] {response}')


if __name__ == '__main__':
    main()
