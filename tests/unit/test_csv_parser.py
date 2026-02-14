import pytest
from app.utils.csv_parser import parse_csv
from app.grades.schemas import GradeCSVRow


def test_parse_valid_csv(csv_factory):
    content = csv_factory(["01.01.2025;101;Иванов Иван;5"])
    rows = parse_csv(content)
    assert len(rows) == 1
    assert rows[0].full_name == "Иванов Иван"

def test_parse_empty_file():
    with pytest.raises(ValueError):
        parse_csv("")

def test_parse_missing_columns():
    content = "ФИО;Оценка\nИванов;5"
    with pytest.raises(ValueError, match="В файле не найдена колонка"):
        parse_csv(content)

def test_parse_invalid_date(csv_factory):
    content = csv_factory(["32.01.2025;101;Тест;5"])
    with pytest.raises(ValueError, match="Неверный формат даты"):
        parse_csv(content)


def test_parse_invalid_grade(csv_factory):
    for grade in ["0", "6"]:
        content = csv_factory([f"01.01.2025;101;Тест;{grade}"])
        with pytest.raises(ValueError):
            parse_csv(content)

def test_parse_dirty_strings(csv_factory):
    content = csv_factory([" 01.01.2025 ;\t101\t; Иванов Иван ; 5 "])
    rows = parse_csv(content)
    assert rows[0].full_name == "Иванов Иван" # Ожидаем чистую строку
    assert rows[0].group_number == "101"