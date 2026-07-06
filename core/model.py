import os
import sys


def resolve_model() -> str:
    if os.getenv('OPENAI_API_KEY'):
        return 'openai:gpt-4o-mini'
    if os.getenv('GEMINI_API_KEY') or os.getenv('GOOGLE_API_KEY'):
        return 'google:gemini-3.5-flash'
    if os.getenv('ANTHROPIC_API_KEY'):
        return 'anthropic:claude-sonnet-4-6'
    print('[Error] API 키가 없습니다. .env 파일을 확인해주세요.')
    sys.exit(1)
