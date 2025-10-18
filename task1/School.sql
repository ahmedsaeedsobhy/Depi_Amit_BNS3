Create SCHEMA school;

CREATE TABLE school.teachers (
	teacher_id SERIAL PRIMARY KEY,
	first_name VARCHAR(255) NOT NULL,
	last_name VARCHAR(255) NOT NULL
);

CREATE TABLE school.subjects (
	subject_id SERIAL PRIMARY KEY,
	title VARCHAR(255) NOT NULL
);

CREATE TABLE school.groups_ (
	group_id SERIAL PRIMARY KEY,
	name VARCHAR(255) NOT NULL
);

CREATE TABLE school.students (
	student_id SERIAL PRIMARY KEY,
	first_name VARCHAR(255) NOT NULL,
	last_name VARCHAR(255) NOT NULL,
	group_id INTEGER NOT NULL,
	FOREIGN KEY (group_id) REFERENCES school.groups_ (group_id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE school.subject_teacher (
	subject_id INTEGER NOT NULL,
	teacher_id INTEGER NOT NULL,
	group_id INTEGER NOT NULL,
	FOREIGN KEY (subject_id) REFERENCES school.subjects (subject_id) ON DELETE CASCADE ON UPDATE CASCADE,
	FOREIGN KEY (teacher_id) REFERENCES school.teachers (teacher_id) ON DELETE CASCADE ON UPDATE CASCADE,
	FOREIGN KEY (group_id) REFERENCES school.groups_ (group_id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE school.marks (
	mark_id SERIAL PRIMARY KEY,
	student_id INTEGER NOT NULL,
	subject_id INTEGER NOT NULL,
	date date NOT NULL,
	mark INTEGER NOT NULL,
	FOREIGN KEY (student_id) REFERENCES school.students (student_id) ON DELETE CASCADE ON UPDATE CASCADE,
	FOREIGN KEY (subject_id) REFERENCES school.subjects (subject_id) ON DELETE CASCADE ON UPDATE CASCADE
);