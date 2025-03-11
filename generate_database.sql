-- Recreate the users table
DROP TABLE IF EXISTS access_log;
DROP TABLE IF EXISTS badge_snapshot;
DROP TABLE IF EXISTS users;

CREATE TABLE users (
    Email VARCHAR(255) PRIMARY KEY,
    Name VARCHAR(255),
    FirstName VARCHAR(255),
    LastName VARCHAR(255),
    LastSignIn DECIMAL(20, 6)
);

-- Recreate the access_log table
CREATE TABLE access_log (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    Email VARCHAR(255),
    Name VARCHAR(255),
    FirstName VARCHAR(255),
    LastName VARCHAR(255),
    StudentID VARCHAR(255),
    SignInTimeExternal VARCHAR(255),
    SignInTime DECIMAL(20, 6),
    IsMember BOOLEAN,
    FOREIGN KEY (Email) REFERENCES users(Email)
);

-- Recreate the badge_snapshot table
CREATE TABLE badge_snapshot (
    Email VARCHAR(255) PRIMARY KEY,
    Badges VARCHAR(255),
    FOREIGN KEY (Email) REFERENCES users(Email)
);