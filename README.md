# Расчёт A/B-теста на Python

Воспроизводимый пример XNova рассчитывает конверсию двух групп, абсолютное и относительное изменение, двусторонний z-тест двух долей и 95% интервал Вальда. Отдельная функция проверяет sample ratio mismatch (SRM) для запланированного распределения 50/50.

Все входные данные синтетические: в группе A — 1000 пользователей и 120 конверсий, в группе B — 1000 пользователей и 160 конверсий. Проект не обращается к сети, внешним API, пользовательским файлам или секретам.

## Что понадобится

- Python 3.12;
- Git;
- терминал.

## Установка

```bash
git clone https://github.com/xnova-tech/ab-testing-python-example.git
cd ab-testing-python-example
python3.12 -m venv .venv
```

Активируйте окружение:

- macOS и Linux: `source .venv/bin/activate`;
- Windows PowerShell: `.venv\Scripts\Activate.ps1`;
- Windows cmd: `.venv\Scripts\activate.bat`.

Установите закреплённые зависимости для проверки:

```bash
python -m pip install -r requirements-dev.txt
```

## Запуск расчёта

```bash
python ab_test_calculation.py
```

Ожидаемый результат:

```text
a_conversion_percent: 12.00
b_conversion_percent: 16.00
absolute_change_pp: 4.00
relative_change_percent: 33.33
pooled_probability: 0.1400
z_statistic: 2.577696
p_value: 0.009946
ci_95_low_pp: 0.96
ci_95_high_pp: 7.04
```

## Проверки

```bash
python -m ruff format --check .
python -m ruff check .
python -m pytest -q
```

21 pytest-сценарий проверяет основной расчёт, различие процентных пунктов и относительных процентов, граничные и ошибочные входные данные, нулевую базовую конверсию и SRM. Тот же набор запускается в GitHub Actions на Linux, macOS и Windows.

## Структура

- `ab_test_calculation.py` — типизированные входные данные и расчёт результата;
- `srm_check.py` — независимая проверка распределения пользователей 50/50;
- `tests/` — положительные и отрицательные pytest-сценарии;
- `.github/workflows/check.yml` — одинаковая проверка на трёх операционных системах.

Пример иллюстрирует механику расчёта и не заменяет планирование мощности, проверку качества данных и предметное решение о запуске изменения.

Исходники распространяются по Apache-2.0; условия находятся в `LICENSE`.
