USE QuizSystemDB;

-- Devices 테이블 생성
CREATE TABLE IF NOT EXISTS Devices (
    DeviceID VARCHAR(255) PRIMARY KEY,
    Status BOOLEAN NOT NULL
);

-- QuizQuestions 테이블 생성
CREATE TABLE IF NOT EXISTS QuizQuestions (
    QuestionID INT AUTO_INCREMENT PRIMARY KEY,
    QuestionText TEXT NOT NULL,
    CorrectAnswer CHAR(1) NOT NULL
);

-- QuizResponses 테이블 생성
CREATE TABLE IF NOT EXISTS QuizResponses (
    ResponseID INT AUTO_INCREMENT PRIMARY KEY,
    DeviceID VARCHAR(255),
    QuestionID INT,
    SelectedAnswer CHAR(1) NOT NULL,
    Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (DeviceID) REFERENCES Devices(DeviceID),
    FOREIGN KEY (QuestionID) REFERENCES QuizQuestions(QuestionID)
);

-- QuizResults 테이블 생성
CREATE TABLE IF NOT EXISTS QuizResults (
    QuestionID INT,
    CorrectResponses INT DEFAULT 0,
    TotalResponses INT DEFAULT 0,
    PRIMARY KEY (QuestionID),
    FOREIGN KEY (QuestionID) REFERENCES QuizQuestions(QuestionID)
);
