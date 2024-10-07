-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Oct 06, 2024 at 05:25 AM
-- Server version: 8.0.39
-- PHP Version: 8.3.11

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `techvaganza_test`
--

-- --------------------------------------------------------

--
-- Table structure for table `attendees`
--

CREATE TABLE `attendees` (
  `UID` int NOT NULL,
  `FirstName` varchar(50) DEFAULT NULL,
  `LastName` varchar(50) DEFAULT NULL,
  `Email` varchar(100) DEFAULT NULL,
  `ContactNumber` varchar(15) DEFAULT NULL,
  `BandID` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `attendees`
--

INSERT INTO `attendees` (`UID`, `FirstName`, `LastName`, `Email`, `ContactNumber`, `BandID`) VALUES
(1, 'John', 'Doe', 'john.doe@email.com', '123-456-7890', 50001),
(2, 'Jane', 'Smith', 'jane.smith@email.com', '234-567-8901', NULL),
(3, 'Bob', 'Johnson', 'bob.j@email.com', '345-678-9012', 50002),
(4, 'Alice', 'Williams', 'alice.w@email.com', '456-789-0123', NULL),
(5, 'Charlie', 'Brown', 'charlie.b@email.com', '567-890-1234', 50003),
(6, 'Diana', 'Miller', 'diana.m@email.com', '678-901-2345', 50004),
(7, 'Edward', 'Davis', 'edward.d@email.com', '789-012-3456', NULL),
(8, 'Fiona', 'Garcia', 'fiona.g@email.com', '890-123-4567', 50005),
(9, 'George', 'Wilson', 'george.w@email.com', '901-234-5678', 50006),
(10, 'Hannah', 'Martinez', 'hannah.m@email.com', '012-345-6789', NULL),
(11, 'Ian', 'Anderson', 'ian.a@email.com', '123-456-7891', 50007),
(12, 'Julia', 'Taylor', 'julia.t@email.com', '234-567-8902', 50008),
(13, 'Kevin', 'Thomas', 'kevin.t@email.com', '345-678-9013', NULL),
(14, 'Laura', 'Moore', 'laura.m@email.com', '456-789-0124', 50009),
(15, 'Michael', 'Jackson', 'michael.j@email.com', '567-890-1235', 50010);

-- --------------------------------------------------------

--
-- Table structure for table `events`
--

CREATE TABLE `events` (
  `EventID` int NOT NULL,
  `EventName` varchar(100) DEFAULT NULL,
  `EventType` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `events`
--

INSERT INTO `events` (`EventID`, `EventName`, `EventType`) VALUES
(1, 'Tech Conference 2024', 'Conference'),
(2, 'Music Festival', 'Concert'),
(3, 'Business Workshop', 'Workshop'),
(4, 'Art Exhibition', 'Exhibition'),
(5, 'Food & Wine Tasting', 'Culinary'),
(6, 'Sports Tournament', 'Sports');

-- --------------------------------------------------------

--
-- Table structure for table `participating`
--

CREATE TABLE `participating` (
  `EventID` int NOT NULL,
  `UserID` int NOT NULL,
  `attended` tinyint(1) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `participating`
--

INSERT INTO `participating` (`EventID`, `UserID`, `attended`) VALUES
(1, 1, 1),
(1, 2, 0),
(1, 3, 1),
(1, 9, 1),
(1, 11, 0),
(2, 4, 1),
(2, 5, 1),
(2, 6, 0),
(2, 10, 1),
(2, 12, 1),
(2, 15, 0),
(3, 1, 1),
(3, 7, 1),
(3, 8, 0),
(3, 13, 1),
(4, 2, 1),
(4, 5, 0),
(4, 9, 1),
(4, 14, 1),
(5, 3, 1),
(5, 6, 1),
(5, 10, 0),
(5, 15, 1),
(6, 7, 1),
(6, 11, 1),
(6, 13, 0),
(6, 14, 1);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `attendees`
--
ALTER TABLE `attendees`
  ADD PRIMARY KEY (`UID`);

--
-- Indexes for table `events`
--
ALTER TABLE `events`
  ADD PRIMARY KEY (`EventID`);

--
-- Indexes for table `participating`
--
ALTER TABLE `participating`
  ADD PRIMARY KEY (`EventID`,`UserID`),
  ADD KEY `UserID` (`UserID`);

--
-- Constraints for dumped tables
--

--
-- Constraints for table `participating`
--
ALTER TABLE `participating`
  ADD CONSTRAINT `participating_ibfk_1` FOREIGN KEY (`EventID`) REFERENCES `events` (`EventID`),
  ADD CONSTRAINT `participating_ibfk_2` FOREIGN KEY (`UserID`) REFERENCES `attendees` (`UID`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
