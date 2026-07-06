# 🚀 Pydantic AI

[Pydantic AI](https://github.com/pydantic/pydantic-ai)를 활용하여 개발자들이 실무에서 바로 재사용할 수 있는 에이전트/플러그인을 모아놓은 모듈형 오픈소스 리포지토리입니다.

공식 문서: [ai.pydantic.dev](https://ai.pydantic.dev)

<br/>

## 🛠️ Prerequisites (사전 준비)

프로젝트를 실행하기 위해 로컬 환경에 아래 도구들이 설치되어 있어야 합니다.

* **Language:** Python 3.10+ 이상
* **Package Manager:** pip 또는 [uv](https://docs.astral.sh/uv/)
* **LLM API Key (택 1):**
  * [OpenAI API Key](https://platform.openai.com/api-keys)
  * [Google AI Studio API Key](https://aistudio.google.com/) (Gemini)
  * [Anthropic API Key](https://console.anthropic.com/)

<br/>

## 💻 Local Setup (로컬 환경 세팅)

### 1. Repository Fork & Clone

organization 메인 레포를 본인의 개인 계정으로 **Fork**한 뒤, 로컬 PC로 클론합니다.

```bash
git clone https://github.com/[본인-유저네임]/pydantic-ai.git
cd pydantic-ai
```

### 2. 가상환경 구축 및 의존성 설치

**pip + venv**

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

**uv 사용 시**

```bash
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt
```

> 특정 모델만 쓸 경우 가벼운 설치도 가능합니다.
>
> ```bash
> pip install "pydantic-ai-slim[openai]"    # OpenAI만
> pip install "pydantic-ai-slim[google]"     # Gemini만
> pip install "pydantic-ai-slim[anthropic]"  # Claude만
> ```

### 3. 환경 변수 세팅 (.env)

`.env.example`을 복사해 `.env` 파일을 만들고, 사용할 API 키 하나를 입력합니다.

```bash
cp .env.example .env
```

```plaintext
# 사용하는 키만 채워서 사용하세요
OPENAI_API_KEY=your_openai_api_key_here
GEMINI_API_KEY=your_gemini_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here
```

<br/>

## 🏃‍♂️ How to Run (기본 예시 실행 방법)

```bash
# 기본 샘플 플러그인 실행
python main.py

# 특정 플러그인 실행 (main.py 수정 불필요)
python main.py sample_plugin

# 등록된 플러그인 목록 확인
python main.py --list

# 플러그인 파일만 단독 실행 (로컬 테스트용)
python plugins/sample_plugin.py
```

성공 시 아래와 비슷하게 출력됩니다. 똑같은 모델을 사용하더라도 결과물이 달라질 수 있습니다.

```plaintext
[System] 플러그인: sample_plugin | 모델: google:gemini-3.5-flash
[Agent] Pydantic AI는 Pydantic 기반의 타입 안전 Python AI 에이전트 프레임워크입니다.
```

<br/>

## 📖 Quick Start (핵심 사용법)

```python
from pydantic_ai import Agent

agent = Agent(
    'google:gemini-3.5-flash',
    instructions='Be concise, reply in Korean.',
)

result = agent.run_sync('pydantic-ai가 뭐야?')
print(result.output)
```

### 자주 쓰는 모델 문자열

| 프로바이더 | 모델 문자열 예시 |
|-----------|-----------------|
| OpenAI | `openai:gpt-4o-mini`, `openai:gpt-4o` |
| Google (Gemini) | `google:gemini-3.5-flash` |
| Anthropic (Claude) | `anthropic:claude-sonnet-4-6` |

더 많은 예제는 [공식 Examples](https://pydantic.dev/docs/ai/models/overview/)를 참고하세요.

<br/>

## 📂 Directory Structure (폴더 구조)

```bash
pydantic-ai/
├── plugins/              # 멤버들이 각자 폴더/파일을 파서 기여할 공간
│   ├── __init__.py
│   ├── registry.py       # 플러그인 자동 탐색 (수정 불필요)
│   ├── sample_plugin.py  # 단일 파일 플러그인 예시
│   ├── sample_package/   # 패키지(폴더) 플러그인 예시
│   │   ├── __init__.py
│   │   ├── __main__.py
│   │   └── tools.py
│   └── my_plugin.py      # 예: 본인 단일 파일 플러그인
│   └── my_plugin/        # 예: 본인 패키지 플러그인
│       ├── __init__.py
│       └── ...
├── core/
│   ├── base_agent.py
│   └── model.py          # AI API 키 로드
├── docs/
│   ├── plugin-readme.template.md
│   └── plugins/          # 플러그인별 문서
├── main.py
├── requirements.txt
├── .env.example
└── README.md
```

<br/>

## 🤝 Contribution Guide (기여 방법)

Single Repo + 개인 Fork 방식으로 협업합니다. 코드 충돌을 방지하기 위해 아래 규칙을 지켜주세요.

### 플러그인 만들기

`BaseAgent`를 상속받아 구현합니다. **단일 파일** 또는 **패키지(폴더)** 둘 다 가능합니다.

#### 방식 A: 단일 파일 (간단할 때)

1. `plugins/sample_plugin.py`를 복사해 `plugins/my_plugin.py` 생성
2. **파일당 `BaseAgent` 서브클래스 1개**만 작성

> `my_plugin`은 템플릿 예시 이름입니다. 실제 구현 시에는 주제에 맞게 이름을 바꿔주세요.
> 예: `plugins/news_summarizer.py`, `plugins/code_reviewer.py`

```python
# plugins/my_plugin.py
import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from core.base_agent import BaseAgent

class MyPlugin(BaseAgent):
    def __init__(self, model: str):
        super().__init__(model=model, instructions='...')

    def get_name(self) -> str:
        return 'my_plugin'
```

#### 방식 B: 패키지 (파일이 많아질 때)

1. `plugins/sample_package/`를 참고해 `plugins/my_plugin/` 폴더 생성
2. `__init__.py`에 `MyPlugin(BaseAgent)` 클래스를 1개 정의
3. 나머지 로직은 `tools.py`, `prompts.py` 등으로 분리

> 패키지도 동일하게 주제 기반 이름을 사용하세요.
> 예: `plugins/news_summarizer/`, `plugins/code_reviewer/`

```bash
plugins/my_plugin/
├── __init__.py    # MyPlugin(BaseAgent) 정의 및 외부 노출(export) 공간
├── __main__.py    # 로컬 단독 실행용 (선택): python -m plugins.my_plugin
├── tools.py
└── prompts.py
```

> 같은 이름의 `my_plugin.py`와 `my_plugin/` 폴더를 동시에 두지 마세요. 이름이 겹치면 **폴더(패키지)가 우선하여 인식됩니다.**

### 실행 & 테스트

**`main.py`를 수정할 필요 없습니다.** `plugins/`에 추가하면 자동으로 인식됩니다.

```bash
python main.py --list              # 단일 파일·패키지 모두 목록에 표시
python main.py my_plugin           # 플러그인 실행
python main.py sample_package      # 패키지 플러그인 실행

# 로컬 단독 테스트
python plugins/my_plugin.py        # 단일 파일
python -m plugins.my_plugin        # 패키지 방식 실행 (프로젝트 루트 디렉터리 기준)
python -m plugins.sample_package   # 패키지 예시
```

### PR 올리기

- `plugins/`에 본인 파일·폴더만 추가/수정합니다. **`main.py`, `core/`는 건드리지 않습니다.**
- PR 본문에 **간단 사용법**만 적어주세요:
  - 플러그인 이름
  - 뭐 하는 플러그인인지 (1~2줄)
  - 실행 명령 (`python main.py xxx`)

  예시:
  ```markdown
  - 플러그인: news_summarizer
  - 설명: 뉴스 URL을 3줄로 요약해줍니다
  - 실행: python main.py news_summarizer
  ```
- 로컬 테스트가 완료되면 본인 레포에 푸시 후, Org 레포의 main 브랜치로 PR을 날려주세요.
- PR을 날린 후 다른 멤버들의 PR 코드를 구경하며 최소 1개 이상의 코멘트(응원, 질문, 사용후기, 피드백 등)를 남겨주세요 😊

### 마지막 주차: 플러그인 문서 정리

1. [`docs/plugins/README.md`](docs/plugins/README.md) 기여자 소개 표에서 본인 칸 채우기 (플러그인 문서 **링크** 연결)
2. `docs/plugins/본인플러그인.md` 파일 **새로 추가**

- 템플릿: [`docs/plugin-readme.template.md`](docs/plugin-readme.template.md)
- 예시: [`docs/plugins/sample_plugin.md`](docs/plugins/sample_plugin.md)

<br/>

## 🏆 명예의 전당 (Upstream 기여 내역)

외부 공식 오픈소스 본진(Upstream)에 직접 PR을 꽂아 머지된 자랑스러운 내역입니다. (머지 시 커밋 해시 싱크 및 링크 박제 공간)

ex) @멤버이름 - [pydantic/pydantic-ai](https://github.com/pydantic/pydantic-ai) 공식 버그 수정 및 기능 추가 PR (#PR번호)
