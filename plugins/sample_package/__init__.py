from core.base_agent import BaseAgent

from .tools import build_instructions


class SamplePackageAgent(BaseAgent):
    """패키지(폴더) 형태 플러그인 예시. 여러 파일로 로직을 나눌 때 참고하세요"""

    def __init__(self, model: str):
        super().__init__(model=model, instructions=build_instructions())

    def get_name(self) -> str:
        return 'sample_package'
