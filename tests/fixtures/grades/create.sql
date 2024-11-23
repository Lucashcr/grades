create table grades (
	id serial primary key,
	student_id varchar(255),
	exam varchar(255),
	value float
);

create index grades_test_grades_student_id on grades (student_id);
