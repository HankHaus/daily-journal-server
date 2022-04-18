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