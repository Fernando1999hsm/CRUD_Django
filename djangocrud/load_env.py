import os
from pathlib import Path


def load_env():
    env_path = Path(__file__).resolve().parent.parent / '.env'
    if not env_path.exists():
        return

    with open(env_path, encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            if '=' not in line:
                continue
            key, _, value = line.partition('=')
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            if key and not os.environ.get(key):
                os.environ.setdefault(key, value)
