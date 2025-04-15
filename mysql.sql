-- Drop tables if they exist
DROP TABLE IF EXISTS badge_snapshot;
DROP TABLE IF EXISTS access_log;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS email_exceptions;

-- Recreate the users table
CREATE TABLE users (
    Email VARCHAR(255) PRIMARY KEY,
    StudentID VARCHAR(255),
    FirstName VARCHAR(255),
    LastName VARCHAR(255),
    School VARCHAR(255) NULL,    -- New column
    ClassLevel VARCHAR(255) NULL  -- New column
);

-- Recreate the access_log table
CREATE TABLE access_log (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    Email VARCHAR(255),
    SignInTimeExternal VARCHAR(255),
    SignInTime DECIMAL(20,6),
    membershipYears JSON NOT NULL DEFAULT ('[]'),
    IsMember BOOLEAN,
    FOREIGN KEY (Email) REFERENCES users(Email)
);

-- Recreate the badge_snapshot table
CREATE TABLE badge_snapshot (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    Narrative_Detail VARCHAR(255),
    Narrative_Title VARCHAR(255),
    IssuedOn VARCHAR(255),
    CreatedAt VARCHAR(255),
    Revoked BOOLEAN,
    Revocation_Reason VARCHAR(255),
    BadgeClass VARCHAR(255),
    ImageURL VARCHAR(255),
    AccessLogID INT,
    FOREIGN KEY (AccessLogID) REFERENCES access_log(ID)
);

-- Create simple email exceptions table
CREATE TABLE email_exceptions (
    exception_email VARCHAR(255) PRIMARY KEY,
    badgr_email VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_badgr_email (badgr_email)
);

