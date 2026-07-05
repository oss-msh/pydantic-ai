> **템플릿 사용 방법**
> 1. https://github.com/oss-msh/template 에서 "Use this template"을 선택하면 oss-msh organization에 새로운 repository가 생성됩니다.
> 2. 스터디 리더는 새로 만들어진 repository에 접속 후 아래 내용을 참고하여 가이드를 수정합니다.
> 3. 기본 세팅법 및 가이드 정리가 완료됐다면, 팀원들은 해당 repository 주소를 공유해주세요.

# 🚀 [선정된 기술 스택 이름]

[선정된 기술 스택 이름](해당 github 주소)을 활용하여 개발자들이 실무에서 바로 재사용할 수 있는 [플러그인/에이전트/템플릿]을 모아놓은 모듈형 오픈소스 리포지토리입니다.

<br/>

## 🛠️ Prerequisites (사전 준비)

프로젝트를 실행하기 위해 로컬 환경에 아래 도구들이 설치되어 있어야 합니다.
* **Language:** Python 3.10+ 이상
* **AI Environment (택 1 또는 필수 기재):**
  * 로컬 LLM 구동을 위한 [Ollama](https://ollama.com/) (모델: `llama3`, `deepseek-coder` 등)
  * Google AI Studio에서 발급받은 [Gemini API Key](https://aistudio.google.com/) (무료 티어)

<br/>

## 💻 Local Setup (로컬 환경 세팅)

### 1. Repository Fork & Clone
organization 메인 레포를 본인의 개인 계정으로 **Fork**한 뒤, 로컬 PC로 클론합니다.
```bash
git clone https://github.com/[본인-유저네임]/[레포-이름].git
cd [레포-이름]
```

### 2. 가상환경 구축 및 의존성 설치
사용하시는 패키지 매니저(Poetry, venv, pipenv 등)에 맞는 명령어를 적어주세요.

- 예시: venv 기준
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 3. 환경 변수 세팅 (.env)
프로젝트 루트 디렉토리에 .env 파일을 생성하고 필요한 API 키를 입력합니다.
```plaintext
# 필요한 API 키 예시 (선택된 주제에 맞게 남겨두세요)
GEMINI_API_KEY=your_gemini_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
```

<br/>

## 🏃‍♂️ How to Run (기본 예시 실행 방법)
```bash
python main.py

# 성공 출력 예시:
# [System] 기본 에이전트 환경 세팅 완료! Ollama/Gemini 모델 연결에 성공했습니다.
```

<br/>

## 📂 Directory Structure (폴더 구조)
각자 독립된 환경에서 충돌 없이 작업할 수 있도록 아래와 같이 폴더 구조가 설계되어 있습니다.
```bash
[project-root]/
├── core/                 # 리더가 세팅한 핵심 베이스 엔진 및 공통 인터페이스
├── plugins/              # 멤버들이 각자 폴더/파일을 파서 기여할 공간
│   ├── __init__.py
│   ├── sample_plugin.py  # 리더가 작성해 둔 참고용 샘플 코드
│   └── [개인_프로젝트명]/    # (2주차에 각자 생성할 공간)
├── requirements.txt
└── README.md
```

<br/>

## 🤝 Contribution Guide (기여 방법)

Single Repo + 개인 Fork 방식으로 협업합니다. 코드 충돌을 방지하기 위해 아래 규칙을 지켜주세요.
- plugins/ 폴더 밑에 본인의 기능 이름으로 파이썬 파일(또는 폴더)을 생성합니다.
- core/에 정의된 베이스 인터페이스(BaseTool 또는 BaseAgent)를 상속받아 기능을 구현합니다.
- 로컬 테스트가 완료되면 본인 레포에 푸시 후, Org 레포의 main 브랜치로 PR(Pull Request)을 날려주세요.
- 리뷰 품앗이: PR을 날린 후 다른 멤버들의 PR 코드를 구경하며 최소 1개 이상의 코멘트(응원, 질문, 피드백 등)를 남겨주세요 😊

<br/>

## 🏆 명예의 전당 (Upstream 기여 내역)
외부 공식 오픈소스 본진(Upstream)에 직접 PR을 꽂아 머지된 자랑스러운 내역입니다. (머지 시 커밋 해시 싱크 및 링크 박제 공간)

@멤버이름 - [외부 레포 이름] 공식 버그 수정 및 기능 추가 PR (#PR번호)
