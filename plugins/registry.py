import importlib
import inspect
from pathlib import Path

from core.base_agent import BaseAgent

_SKIP_FILES = {'registry.py'}
_SKIP_PREFIX = '_'


def list_plugins() -> list[str]:
    """plugins/ 아래 BaseAgent를 구현한 단일 파일·패키지 이름 목록"""
    plugin_dir = Path(__file__).parent
    names: list[str] = []
    for name in _discover_plugin_names(plugin_dir):
        if _find_plugin_class(name) is not None:
            names.append(name)
    return names


def load_plugin(name: str) -> type[BaseAgent]:
    """plugins/{name}.py 또는 plugins/{name}/ 에서 BaseAgent 서브클래스를 로드"""
    plugin_class = _find_plugin_class(name)
    if plugin_class is None:
        available = ', '.join(list_plugins()) or '(없음)'
        raise ValueError(f'플러그인 "{name}"을 찾을 수 없습니다. 사용 가능: {available}')
    return plugin_class


def _discover_plugin_names(plugin_dir: Path) -> list[str]:
    package_names = {
        path.name
        for path in plugin_dir.iterdir()
        if path.is_dir()
        and not path.name.startswith(_SKIP_PREFIX)
        and (path / '__init__.py').is_file()
    }

    file_names: list[str] = []
    for path in sorted(plugin_dir.glob('*.py')):
        if path.name.startswith(_SKIP_PREFIX) or path.name in _SKIP_FILES:
            continue
        if path.stem in package_names:
            continue
        file_names.append(path.stem)

    return sorted(file_names + list(package_names))


def _find_plugin_class(name: str) -> type[BaseAgent] | None:
    module = importlib.import_module(f'plugins.{name}')
    for _, obj in inspect.getmembers(module, inspect.isclass):
        if issubclass(obj, BaseAgent) and obj is not BaseAgent:
            return obj
    return None
