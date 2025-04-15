-- Drop tables if they exist
IF OBJECT_ID('badge_snapshot', 'U') IS NOT NULL DROP TABLE badge_snapshot;
IF OBJECT_ID('access_log', 'U') IS NOT NULL DROP TABLE access_log;
IF OBJECT_ID('users', 'U') IS NOT NULL DROP TABLE users;
IF OBJECT_ID('email_exceptions', 'U') IS NOT NULL DROP TABLE email_exceptions;

-- Recreate the users table
CREATE TABLE users (
    Email NVARCHAR(255) PRIMARY KEY,
    StudentID NVARCHAR(255),
    FirstName NVARCHAR(255),
    LastName NVARCHAR(255),
    School NVARCHAR(255) NULL,    -- New column
    ClassLevel NVARCHAR(255) NULL  -- New column
);

-- Recreate the access_log table
CREATE TABLE access_log (
    ID INT IDENTITY(1,1) PRIMARY KEY,
    Email NVARCHAR(255),
    SignInTimeExternal NVARCHAR(255),
    SignInTime DECIMAL(20,6),
    membershipYears NVARCHAR(MAX) NOT NULL DEFAULT ('[]'),
    IsMember BIT,
    FOREIGN KEY (Email) REFERENCES users(Email)
);

-- Recreate the badge_snapshot table
CREATE TABLE badge_snapshot (
    ID INT IDENTITY(1,1) PRIMARY KEY,
    Narrative_Detail NVARCHAR(255),
    Narrative_Title NVARCHAR(255),
    IssuedOn NVARCHAR(255),
    CreatedAt NVARCHAR(255),
    Revoked BIT,
    Revocation_Reason NVARCHAR(255),
    BadgeClass NVARCHAR(255),
    ImageURL NVARCHAR(255),
    AccessLogID INT,
    FOREIGN KEY (AccessLogID) REFERENCES access_log(ID)
);

-- Create simple email exceptions table
CREATE TABLE email_exceptions (
    exception_email NVARCHAR(255) PRIMARY KEY,
    badgr_email NVARCHAR(255) NOT NULL,
    created_at DATETIME DEFAULT GETDATE()
);
