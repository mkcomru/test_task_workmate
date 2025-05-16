# Скрипт подсчёта зарплаты сотрудников

Скрипт для чтения данных сотрудников из CSV файлов и формирования отчётов по заработной плате.

## Требования

- Python 3.6+
- pytest (для запуска тестов)

## Установка

Клонируйте репозиторий:

```bash
git clone https://github.com/mkcomru/test_task_workmate
cd employee-payroll
```

### Запуск скрипта

```bash
python main.py data1.csv data2.csv data3.csv --report payout
```

### Параметры

- `files`: Один или несколько CSV файлов с данными сотрудников
- `--report`: Тип отчёта (например, `payout`)

### Формат CSV файлов

CSV файлы должны содержать следующие столбцы:
- `id`: Идентификатор сотрудника
- `email`: Электронная почта сотрудника
- `name`: Имя сотрудника
- `department`: Отдел
- `hours_worked`: Отработанные часы
- `hourly_rate` или `rate` или `salary`: Часовая ставка

## Запуск тестов

```bash
pytest
```

Для проверки покрытия кода тестами:

```bash
pytest --cov=.
```

## Добавление новых типов отчётов

Чтобы добавить новый тип отчёта:

1. Создайте новый класс, наследующийся от `ReportGenerator`:

```python
class NewReportGenerator(ReportGenerator):
    def generate(self, data: List[Dict[str, Any]]) -> str:
        # Реализация генерации отчёта
        return "Новый отчёт"
```

2. Зарегистрируйте новый генератор в фабрике:

```python
ReportFactory.register_generator('new_report', NewReportGenerator)
```

3. Используйте новый тип отчёта при запуске скрипта:

```bash
python main.py data1.csv --report new_report
```