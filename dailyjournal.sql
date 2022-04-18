CREATE TABLE `Mood` (
    `id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    `label` TEXT
);

CREATE TABLE `Entry` (
    `id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    `concept` TEXT,
    `entry` TEXT NOT NULL,
    `date` TEXT NOT NULL,
    `mood_id` INTEGER,
    FOREIGN KEY(`mood_id`) REFERENCES `Mood`(`id`)
);

INSERT INTO `Mood` VALUES (null, "Happy");
INSERT INTO `Mood` VALUES (null, "Sad");

INSERT INTO `Entry` values(null, "SQL", "Enjoying learning SQL!", "April 18th 2022", 1);
INSERT INTO `Entry` values(null, "Python", "Enjoying learning Python", "April 18th 2022", 1);
INSERT INTO `Entry` values(null, "SQL", "SQL is also ruining my life someone please send help", "April 18th 2022", 2);