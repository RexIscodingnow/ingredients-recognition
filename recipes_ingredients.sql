show databases;

use `recipes_ingredients`;
show tables;

create table `Users` (
	`user_id` 	integer			auto_increment,
    `username` 	varchar(10) 	not null,
    `email` 	varchar(50) 	not null unique,
    `password` 	varchar(255) 	not null,

    primary key (`user_id`)
);

create table `Ingredients` (
	`ingredient_id` 	integer 	auto_increment,
    `ingredient_name` 	varchar(20) not null,

    primary key (`ingredient_id`)
);
alter table `Ingredients`
modify `ingredient_name` varchar(20) not null unique;

create table `Recipes` (
	`recipe_id` 		integer 	auto_increment,
    `recipe_name` 		varchar(20) not null,
    `recipe_info_url` 	text 		null,
    `cooking_step`		text 		null,

    primary key (`recipe_id`)
);
alter table `Recipes`
modify `recipe_name` varchar(20) not null unique;

/* The intermediary table for Ingredients and Recipes */
create table `RecipeIngredients` (
    `recipe_id` 	integer not null,
    `ingredient_id` integer not null,

    primary key (`recipe_id`, `ingredient_id`),
	foreign key (`recipe_id`) references `Recipes`(`recipe_id`)
		ON DELETE CASCADE 		/* 當食譜被刪除時，相關連結也刪除 */
        ON UPDATE CASCADE, 		/* 當食譜ID更新時，相關連結也更新 */
    foreign key (`ingredient_id`) references `Ingredients`(`ingredient_id`)
		ON DELETE RESTRICT 		/* 當食材仍被使用時，禁止刪除食材 */
        ON UPDATE CASCADE
);

/*
The intermediary table for Users and Recipes.
In order for the recommendation system to retrieve the rating score of a recipe
based on users' relative preferences.
*/
create table `Recipe_ratings` (
    `user_id` 	integer not null,
    `recipe_id` integer not null,
    `rating` 	integer not null,

    primary key (`user_id`, `recipe_id`),
    foreign key (`user_id`) references `Users`(`user_id`)
		on delete cascade	/* 當使用者刪除時，評分也一併刪除 */
        on update cascade,
    foreign key (`recipe_id`) references `Recipes`(`recipe_id`)
		on delete cascade	/* 當食譜刪除時，評分也一併刪除 */
        on update cascade
);

/*
Set the foreign keys based on relational of `Ingredients` <--> `Recipes` and `Users.id` --> `Recipe_ratings.user_id`
*/
/*
-- alter table `Ingredients`
-- add `recipe_id` integer null;
-- alter table `Ingredients`
-- add foreign key (`recipe_id`) references `RecipeIngredients`(`recipe_id`);

-- alter table `Recipes`
-- add `ingredient_id` integer null;
-- alter table `Recipes`
-- add foreign key (`ingredient_id`) references `Ingredients`(`ingredient_id`);
-- alter table `Recipes`
-- add foreign key (`ingredient_id`) references `RecipeIngredients`(`ingredient_id`);

-- alter table `Users`
-- add foreign key (`user_id`) references `Recipe_ratings`(`user_id`);
*/
/* ======================================================================================== */

desc `Users`;
desc `Ingredients`;
desc `Recipes`;
desc `RecipeIngredients`;
desc `Recipe_ratings`;
show create table `Users`;
show create table `Ingredients`;
show create table `Recipes`;
show create table `RecipeIngredients`;
show create table `Recipe_ratings`;


/* 查詢欄位約束條件 (屬性) */
SELECT * 
FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE
WHERE TABLE_NAME = 'Ingredients' AND CONSTRAINT_NAME != 'PRIMARY';
SELECT * 
FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE
WHERE TABLE_NAME = 'Recipes' AND CONSTRAINT_NAME != 'PRIMARY';
SELECT * 
FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE
WHERE TABLE_NAME = 'RecipeIngredients' AND CONSTRAINT_NAME != 'PRIMARY';


insert into `Users` (`username`, `email`, `password`) values
('真．爆炸王', 'Feevell@mail.com', 123),
('軟綿綿黃金少女', 'Zirgruzath@mail.com', 123);

insert into `Ingredients` (`ingredient_name`) values
('雞扒/雞排'), ('麻油'), ('醬油'), ('米酒'), ('糖'), ('蒜頭'), ('薑'), ('九層塔'),
('川耳(泡發)'), ('小黃瓜'), ('蒜末'), ('大辣椒'), ('白芝麻'), ('醬油膏'), ('香油'), ('白醋'), ('砂糖'), ('味精'),
('蕃茄'), ('雞蛋'), ('蕃茄醬'), ('蔥花'), ('鹽巴'),
('豬五花'), ('蔥'), ('大蒜'), ('胡椒'),
('青椒'), ('豬肉絲');

insert into `Recipes` (`recipe_name`, `cooking_step`) values
('台式三杯雞', '步驟:
1. 蒜頭切片
2. 中火熱鍋煎雞扒/雞排，先煎皮的一邊出油，煎至金黃色，反轉煎約1分鐘後夾起，不用全熟
3. 把雞扒/雞排切成小塊
4. 中火熱鍋加入麻油，把薑和蒜頭炒香
5. 加入雞件，然後加入醬油、米酒及糖，再炒一炒雞件轉小火燉8-10分鐘蓋上蓋子
6. 開蓋轉大火收汁
7. 加入九層塔，炒1-2分鐘即可上碟'),
('酸甜涼拌川耳(五辛素)', '步驟:
1. 川耳加熱水浸泡20分鐘
2. 川耳洗淨，下鍋焯水2~3分鐘，控乾備用
3. 盆中加入蒜末、辣椒圈、醬油膏、香油、白糖、白醋、味精，攪拌均勻
4. 小黃瓜切波浪片，所有材料翻拌均勻
5. 裝盤，撒上芝麻粒點綴'),
('番茄炒蛋', '步驟:
1. 蔥洗淨切成蔥花
2. 洗淨然後在蕃茄底部輕輕界十字
3. 中火把水煮至沸騰， 加入蕃茄煮約30-45秒即可
4. 把蕃茄加入冷水一會再取出
5. 煮過的蕃茄很容易就能去皮把蕃茄去皮後切塊
6. 把雞蛋打散，加鹽攪拌均勻
7. 中火熱鍋加油和蕃茄，加入蕃茄醬及糖炒至軟身及收汁後備用
8. 中火熱鍋後加油及雞蛋，蛋液邊缘漸漸凝固後把蛋液往中間推
9. 雞蛋5成熟時加入蕃茄關火繼續炒，利用餘溫將蛋液炒熟，加入少許鹽調味，攪拌均勻即可'),
('蔥爆豬五花', '步驟:
1. 豬五花切長條狀， 蔥白蔥綠切小段分開、大蒜切片。 醬油2大匙、糖一小匙、米酒一小匙、香油一小匙
2. 豬五花直接入炒鍋、開中火逼出油。
3. 在逼出的油中煎至金黃色。
4. 瀝乾油的豬五花盛出備用,鍋中放一小匙豬油爆香蔥白、蒜片。
5. 把豬五花倒回鍋中拌炒。
6. 將調料，鹽、胡椒、醬油、糖放入翻炒，米酒沿著鍋邊淋下、香油接著下翻炒拌勻。
7. 最後把蔥綠加入快速翻炒即可裝盤。
8. 焦香的蔥爆豬五花下酒好菜上桌'),
('青椒炒肉絲', '步驟:
1. 青椒切絲備用、蒜頭切蒜末，肉絲先用少許醬油醃15 -20分鐘
2. 起油鍋爆香蒜頭
3. 先稍微炒一下青椒後起鍋備用
4. 炒肉絲至8分熟時
5. 再加入炒好的青椒
6. 起鍋前一點點鹽巴調味
7. 青椒肉絲完成囉～');



select * from `Users`;
select * from `Ingredients`;
select * from `Recipes`;


