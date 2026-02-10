import csv
from io import StringIO
from typing import List
from app.grades.schemas import GradeCSVRow

def parse_csv(content: str) -> List[GradeCSVRow]:
    f = StringIO(content.strip())
    
    reader = csv.DictReader(f, delimiter=';')

    rows = []
    for row in reader:
        try:
            # Маппим 
            validated_row = GradeCSVRow(
                lesson_date=row["Дата"].strip(),
                group_number=row["Номер группы"].strip(),
                full_name=row["ФИО"].strip(),
                grade=int(row["Оценка"].strip())
            )
            rows.append(validated_row)
        except KeyError as e:
            raise ValueError(f"В файле не найдена колонка: {e}")
        except Exception as e:
            raise ValueError(f"Ошибка в данных строки {row}: {e}")

    return rows