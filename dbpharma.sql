-- phpMyAdmin SQL Dump
-- version 4.5.1
-- http://www.phpmyadmin.net
--
-- Host: 127.0.0.1
-- Generation Time: Apr 03, 2018 at 09:09 PM
-- Server version: 10.1.16-MariaDB
-- PHP Version: 5.6.24

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `pharmacy`
--

-- --------------------------------------------------------

--
-- Table structure for table `company`
--
CREATE DATABASE dbpharma;
USE dbpharma;
CREATE TABLE `company` (
  `NAME` varchar(50) NOT NULL,
  `ADDRESS` varchar(50) NOT NULL,
  `PHONE` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `company`
--

INSERT INTO `company` (`NAME`, `ADDRESS`, `PHONE`) VALUES
('Cipla', 'Mumbai', '12903'),
('Sun Pharma', 'Mysore', '01289078443'),
('Med_City', 'Nellore', '010114367832');

-- --------------------------------------------------------

--
-- Table structure for table `drugs`
--

CREATE TABLE IF NOT EXISTS drugs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    type VARCHAR(50) NOT NULL,
    dose VARCHAR(50) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    quantity INT NOT NULL,
    expiration_date DATE NOT NULL,
    company_name VARCHAR(255) NOT NULL
);

-- Insert sample data into `drugs` table
INSERT INTO drugs (name, type, dose, price, quantity, expiration_date, company_name)
VALUES
('Paracetamol', 'Tablet', '500mg', 1.00, 100, '2024-12-31', 'PharmaCorp'),
('Amoxicillin', 'Capsule', '250mg', 0.50, 200, '2025-01-15', 'MedLife'),
('Ibuprofen', 'Tablet', '400mg', 1.20, 150, '2024-11-30', 'HealthCare Inc.');
-- --------------------------------------------------------


--
-- Table structure for table `login`
--

CREATE TABLE `login` (
  `NAME` varchar(50) NOT NULL,
  `TYPE` varchar(20) NOT NULL,
  `DATE` varchar(20) NOT NULL,
  `TIME` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `login`
--

INSERT INTO `login` (`NAME`, `TYPE`, `DATE`, `TIME`) VALUES
('admin', 'Admin', '17-02-2017', '10:30:24'),

------------------------------------------------------
--
-- Table structure for table `purchase`
--

CREATE TABLE `purchase` (
  `NAME` varchar(50) NOT NULL,
  `TYPE` varchar(20) NOT NULL,
  `COMPANY_NAME` varchar(20) NOT NULL,
  `QUANTITY` int(11) NOT NULL,
  `PRICE` double NOT NULL,
  `AMOUNT` double NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `purchase`
--

INSERT INTO `purchase` ( `NAME`, `TYPE`, `COMPANY_NAME`, `QUANTITY`, `PRICE`, `AMOUNT`) VALUES
('fsdgjfihjorodsf', 'Novalo', 'Bills', 'Med_City', 40, 2, 80);

-- --------------------------------------------------------

--
-- Table structure for table `sales`
--

CREATE TABLE `sales` (
  `NAME` varchar(50) NOT NULL,
  `QUANTITY` int(11) NOT NULL,
  `PRICE` double NOT NULL,
  `AMOUNT` double NOT NULL,
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `ID` int(11) NOT NULL,
  `NAME` varchar(50) NOT NULL,
  `DOB` varchar(20) NOT NULL,
  `ADDRESS` varchar(100) NOT NULL,
  `PHONE` varchar(20) NOT NULL,
  `SALARY` double NOT NULL,
  `PASSWORD` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`ID`, `NAME`, `DOB`, `ADDRESS`, `PHONE`, `SALARY`, `PASSWORD`) VALUES
(1, 'admin', '23-12-1995', 'Someplace India', '9800000000', 50000, 'admin'),

--
-- Indexes for dumped tables
--

--
-- Indexes for table `company`
--
ALTER TABLE `company`
  ADD PRIMARY KEY (`NAME`);

--
-- Indexes for table `drugs`
--
ALTER TABLE `drugs`
  ADD PRIMARY KEY (`BARCODE`);

--
-- Indexes for table `purchase`
--
ALTER TABLE `purchase`
  ADD PRIMARY KEY (`BARCODE`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`ID`);
--
-- Indexes for table `purchase`
--  
  ALTER TABLE purchase 
  add constraint fkr3
  foreign key(company_name)
  references company(name) 
  on update cascade on delete cascade;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
CREATE TABLE deals (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255),
    quantity INT,
    price FLOAT,
    amount FLOAT
);
INSERT INTO deals (name, quantity, price, amount) VALUES
('Deal 1', 10, 50.0, 500.0),

