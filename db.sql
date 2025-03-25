SHOW databases;

-- create database `recipes_ingredients`;

use `recipes_ingredients`;
show tables;

create table `recipe` (
	`recipe_id` int auto_increment,
    `recipe_name` varchar(50) unique,
    `cook_step` varchar(200),
	
    primary key (`recipe_id`)
);

create table `ingredient` (
	`ingredient_id` int auto_increment,
    `ingredient` varchar(50) unique,
    `recipe_id` int,
    
    primary key (`ingredient_id`),
    foreign key (`recipe_id`) references `recipe`(`recipe_id`)
);

/* Add foreign key */
/*
alter table `recipe`
add `ingredient_id` int;
alter table `recipe`
add foreign key (`ingredient_id`) references `ingredient`(`ingredient_id`);
*/

describe `recipe`;
describe `ingredient`;

