import csv
from io import StringIO
from typing import List
from app.grades.schemas import GradeCSVRow

def parse_csv(content: str) -> List[GradeCSVRow]:
    f = StringIO(content.strip())
    
    reader = csv.DictReader(f, delimiter=';')
    if reader.fieldnames:
        reader.fieldnames = [name.strip().replace('\ufeff', '') for name in reader.fieldnames]

    rows = []
    for row in reader:
        try:
            cleaned_row = {k: (v.strip() if isinstance(v, str) else v) for k, v in row.items()}
            
            validated_row = GradeCSVRow(
                lesson_date=cleaned_row["Дата"],
                group_number=cleaned_row["Номер группы"],
                full_name=cleaned_row["ФИО"],
                grade=cleaned_row["Оценка"]
            )
            rows.append(validated_row)
        except KeyError as e:
            raise ValueError(f"В файле не найдена колонка: {e}")
        except Exception as e:
            raise ValueError(f"Ошибка в данных: {e}")

    return rows