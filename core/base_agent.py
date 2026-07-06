from abc import ABC, abstractmethod

from pydantic_ai import Agent


class BaseAgent(ABC):
    """멤버 플러그인이 상속받을 베이스 에이전트 인터페이스"""

    def __init__(self, model: str, instructions: str):
        self.agent = Agent(model, instructions=instructions)

    @abstractmethod
    def get_name(self) -> str:
        """플러그인 식별 이름"""

    def run(self, prompt: str) -> str:
        result = self.agent.run_sync(prompt)
        return result.output
