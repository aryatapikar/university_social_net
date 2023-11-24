create database if not exists social;
use social;

create table `student`(
`s_id` varchar(20) not null,
`stu_name` varchar(50) not null,
`stu_number` varchar(10) not null,
`section` varchar(1) not null,
`semester` int not null,
`username` varchar(50) not null,
`stu_password` varchar(50) not null,
primary key (`username`)
);

create table teacher(
`t_id` varchar(20) not null,
`t_name` varchar(50) not null,
`t_number` varchar(10) not null,
`section` varchar(1) not null,
`semester` int not null,
`username` varchar(50) not null,
`t_password` varchar(50) not null,
primary key (`username`),
);

create table posts(
`post_id` int auto_increment not null,
`username` varchar(50) not null,
`caption` varchar(200),
`comments` varchar(200),
`likes` int default 0,
`subject` int,
`photo` blob,
primary key (`post_id`),
foreign key(`username`) references who(`username`),
foreign key(`subject`) references subject(`sub_id`)
);

create table subject(
`sub_id` int not null,
`sub_name` varchar(10) not null,
primary key (`sub_id`)
);


create table who(
`username` varchar(50) primary key,
`stu_teach` varchar(10) not NULL
);

create table student_studies(
`username` varchar(50) not null,
`subject` int not null,
foreign key(`username`) references student(`username`),
foreign key(`subject`) references subject(`sub_id`)
);

create table teacher_teaches(
`username` varchar(50) not null,
`subject` int not null,
foreign key(`username`) references teacher(`username`),
foreign key(`subject`) references subject(`sub_id`)
);


create table comments(postid int not null,
username varchar(50) not null,
comment varchar(200) not null,
foreign key (postid) references posts(post_id),
foreign key (username) references who(username));

DELIMITER //
CREATE TRIGGER after_student_insert 
AFTER INSERT ON student
FOR EACH ROW 
BEGIN
  INSERT INTO who(username, stu_teach) VALUES (NEW.username, 'student');
END;
//
DELIMITER ;

DELIMITER //
CREATE TRIGGER after_teacher_insert 
AFTER INSERT ON teacher
FOR EACH ROW 
BEGIN
  INSERT INTO who(username, stu_teach) VALUES (NEW.username, 'teacher');
END;
//

DELIMITER ;

DELIMITER //
CREATE PROCEDURE CountUserPosts(IN user_name VARCHAR(50), OUT post_count INT)
BEGIN
    SELECT COUNT(*) INTO post_count FROM posts WHERE username = user_name;
END;
//
DELIMITER ;