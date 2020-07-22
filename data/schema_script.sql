
CREATE TABLE if not exists `worker` ( `id` INTEGER PRIMARY KEY AUTOINCREMENT , `password` varchar (255) NOT NULL, `user_name` varchar (200) NOT NULL UNIQUE, `email` varchar(200) NOT NULL,`phone_number` varchar(11) NOT NULL, `name` varchar(200) NOT NULL, `created_at` datetime NOT NULL, `updated_at` datetime NOT NULL, `is_deleted` bool NOT NULL, `designation` varchar(200) NOT NULL );

CREATE TABLE if not exists `role` ( `id`  INTEGER PRIMARY KEY AUTOINCREMENT , `role` varchar ( 200 ) NOT NULL);

CREATE TABLE if not exists `user_role` ( `user_id` varchar ( 200 ) NOT NULL, `role` int  NOT NULL, primary key(`role`, `user_id`), FOREIGN KEY(`role`) REFERENCES `role`(`id`), FOREIGN KEY(`user_id`) REFERENCES `worker`(`id`) );

CREATE TABLE if not exists `accident_type` ( `id`  INTEGER PRIMARY KEY AUTOINCREMENT , `accident` varchar ( 200 ) NOT NULL Unique);

CREATE TABLE if not exists  `accident` ( `id`  INTEGER PRIMARY KEY AUTOINCREMENT , `type` int NOT NULL , `timestamp` datetime NOT NULL, `created_by` int NOT NULL, `location` varchar(200) NOT NULL, `status` varchar(200) NOT NULL, FOREIGN KEY(`type`) REFERENCES `accident_type`(`id`), FOREIGN KEY(`created_by`) REFERENCES `worker`(`id`));

CREATE TABLE if not exists `accidents_supervisor` (`id`  INTEGER PRIMARY KEY AUTOINCREMENT , `accident_id` int NOT NULL, `supervisor_id` int NOT NULL, FOREIGN KEY(`supervisor_id`) REFERENCES `worker`(`id`), FOREIGN KEY(`accident_id`) REFERENCES `accident`(`id`), UNIQUE (`accident_id`,`supervisor_id`) );

CREATE TABLE if not exists `accident_reports` ( `id`  INTEGER PRIMARY KEY AUTOINCREMENT , `accident_id` int NOT NULL, `submitted_by` int NOT NULL, `eye_witness` int , `reason` varchar(200) not null, `timing` datetime NOT NULL, `submission_time` datetime NOT NULL, `location` varchar(200) not null, `casualties` varchar ( 200 ), `culprit` varchar ( 200 ), `action_to_resolve` varchar ( 200 ) ,FOREIGN KEY(`accident_id`) REFERENCES `accident`(`id`), FOREIGN KEY(`submitted_by`) REFERENCES `worker`(`id`), FOREIGN KEY(`eye_witness`) REFERENCES `worker`(`id`) );

CREATE TABLE if not exists `final_accident_report` ( `id`  INTEGER PRIMARY KEY AUTOINCREMENT , `accident_id` int NOT NULL, `accident_location` varchar(200) NOT NULL, `victims` varchar(200), `time_of_accident` datetime NOT NULL, `submission_time` datetime, `culprit` varchar ( 200 ), `action_to_resolve` varchar ( 200 ),`reason` varchar ( 200 ) not null, FOREIGN KEY(`accident_id`) REFERENCES `accident`(`id`));
