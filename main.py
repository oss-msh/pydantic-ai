import sys

from dotenv import load_dotenv

from core.model import resolve_model
from plugins.registry import list_plugins, load_plugin

DEFAULT_PLUGIN = 'sample_plugin'
DEFAULT_PROMPT = 'pydantic-ai를 한 문장으로 소개해줘.'


def print_usage() -> None:
    plugins = ', '.join(list_plugins())
    print('사용법:')
    print('  python main.py                  # sample_plugin 실행')
    print('  python main.py <plugin_name>    # 특정 플러그인 실행')
    print('  python main.py --list           # 플러그인 목록')
    print(f'  등록된 플러그인: {plugins}')


def main() -> None:
    load_dotenv()

    if len(sys.argv) > 1 and sys.argv[1] in ('--list', '-l'):
        for name in list_plugins():
            print(name)
        return

    if len(sys.argv) > 1 and sys.argv[1] in ('--help', '-h'):
        print_usage()
        return

    plugin_name = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_PLUGIN
    prompt = sys.argv[2] if len(sys.argv) > 2 else DEFAULT_PROMPT

    plugin_class = load_plugin(plugin_name)
    model = resolve_model()
    plugin = plugin_class(model=model)

    print(f'[System] 플러그인: {plugin.get_name()} | 모델: {model}')
    response = plugin.run(prompt)
    print(f'[Agent] {response}')


if __name__ == '__main__':
    main()
