import logging.config
import os
from pathlib import Path

import yaml

log = logging.getLogger(__name__)


def setup_logging(
        default_path: str = './../logging.yaml',
        default_level: int = logging.DEBUG
) -> None:
    """Функция для загрузки конфигурации логирования из файла YAML"""
    log.info(f'Путь к конфигурационному файлу logging: {default_path}')

    try:
        log_dir = Path("logs")
        log_dir.mkdir(parents=True, exist_ok=True)

        with open(default_path, encoding='utf-8') as f:
            config = yaml.safe_load(f)
            logging.config.dictConfig(config)

    except FileNotFoundError:
        log.warning(
            f'Лог файл {default_path} не найден.'
            f' Применяется уровень по умолчанию.',
        )
        logging.basicConfig(
            level=default_level,
            format='%(asctime)s - %(name)s'
                   ' - %(levelname)s - %(message)s',
        )

    except yaml.YAMLError as exc:
        log.warning(f'Ошибка при загрузке YAML-конфигурации: {exc}')
        logging.basicConfig(
            level=default_level,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        )

    except Exception as e:
        log.warning(f'Неожиданная ошибка при настройке логирования: {e}')
        logging.basicConfig(
            level=default_level,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        )
