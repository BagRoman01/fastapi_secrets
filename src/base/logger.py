import logging.config
import os
import yaml

log = logging.getLogger(__name__)


def setup_logging(
        default_path='./../logging.yaml',
        default_level=logging.DEBUG
):
    """Функция для загрузки конфигурации логирования из файла YAML"""
    absolute_path = os.path.abspath(default_path)
    log.info(f'Путь к конфигурационному файлу logging: {absolute_path}')

    try:
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
