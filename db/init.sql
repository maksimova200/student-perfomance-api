CREATE TABLE IF NOT EXISTS students (
    id SERIAL PRIMARY KEY,
    full_name VARCHAR(255) NOT NULL,
    group_number VARCHAR(10) NOT NULL,
    CONSTRAINT unique_student_group UNIQUE (full_name, group_number)
);

CREATE TABLE IF NOT EXISTS grades (
    id SERIAL PRIMARY KEY,
    student_id INTEGER REFERENCES students(id) ON DELETE CASCADE,
    grade SMALLINT NOT NULL CHECK (grade >= 1 AND grade <= 5),
    lesson_date DATE NOT NULL
);

CREATE INDEX idx_grades_student_id ON grades(student_id);
CREATE INDEX idx_grades_grade_student ON grades(grade, student_id);