import sys
from pathlib import Path

# 단독 실행(python plugins/xxx.py) 시에도 core import가 되도록 경로 추가
_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from dotenv import load_dotenv

from core.base_agent import BaseAgent
from core.model import resolve_model

DEFAULT_PROMPT = 'pydantic-ai를 한 문장으로 소개해줘'


class SamplePlugin(BaseAgent):
    """참고용 샘플 플러그인. 새 플러그인 작성 시 이 파일을 복사해 시작하세요"""

    def __init__(self, model: str):
        super().__init__(
            model=model,
            instructions='You are a helpful assistant. Reply in Korean',
        )

    def get_name(self) -> str:
        return 'sample_plugin'


if __name__ == '__main__':
    load_dotenv()
    model = resolve_model()
    plugin = SamplePlugin(model=model)
    print(f'[System] 플러그인: {plugin.get_name()} | 모델: {model}')
    response = plugin.run(DEFAULT_PROMPT)
    print(f'[Agent] {response}')
