-- Recreate the users table
DROP TABLE IF EXISTS badge_snapshot;
DROP TABLE IF EXISTS access_log;
DROP TABLE IF EXISTS users;

CREATE TABLE users (
    Email VARCHAR(255) PRIMARY KEY,
    StudentID VARCHAR(255),
    FirstName VARCHAR(255),
    LastName VARCHAR(255)
);

-- Recreate the access_log table
CREATE TABLE access_log (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    Email VARCHAR(255),
    SignInTimeExternal VARCHAR(255),
    SignInTime DECIMAL(20, 6),
    IsMember BOOLEAN,
    FOREIGN KEY (Email) REFERENCES users(Email)
);

-- Recreate the badge_snapshot table
CREATE TABLE badge_snapshot (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    Narrative_Detail VARCHAR(255),
    Narrative_Title VARCHAR(255),
    IssuedOn VARCHAR(255),
    Revoked BOOLEAN,
    Revocation_Reason VARCHAR(255),
    BadgeClass VARCHAR(255),
    ImagePath VARCHAR(255),
    AccessLogID INT,
    FOREIGN KEY (AccessLogID) REFERENCES access_log(ID)
);

