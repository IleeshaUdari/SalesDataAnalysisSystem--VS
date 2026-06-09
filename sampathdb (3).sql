-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jul 11, 2024 at 07:11 PM
-- Server version: 10.4.27-MariaDB
-- PHP Version: 8.1.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `sampathdb`
--
CREATE DATABASE IF NOT EXISTS `sampathdb` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE `sampathdb`;

-- --------------------------------------------------------

--
-- Table structure for table `branch`
--

DROP TABLE IF EXISTS `branch`;
CREATE TABLE IF NOT EXISTS `branch` (
  `brid` int(11) NOT NULL,
  `branchName` varchar(100) NOT NULL,
  `address` varchar(255) NOT NULL,
  `branchManager` varchar(255) NOT NULL,
  `totalEmployees` int(11) NOT NULL,
  PRIMARY KEY (`brid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `branch`
--

INSERT INTO `branch` (`brid`, `branchName`, `address`, `branchManager`, `totalEmployees`) VALUES
(1, 'Colombo', 'Colombo', 'Mr. Amal Perera', 50),
(2, 'Gampaha', 'Gampaha', 'Mr. Tharaka', 36),
(3, 'Kandy', 'Kandy', 'Ms. Jane Eyre', 56);

-- --------------------------------------------------------

--
-- Table structure for table `branchproduct`
--

DROP TABLE IF EXISTS `branchproduct`;
CREATE TABLE IF NOT EXISTS `branchproduct` (
  `bpid` int(11) NOT NULL AUTO_INCREMENT,
  `branchId` int(11) NOT NULL,
  `productId` int(11) NOT NULL,
  `branchqty` int(11) NOT NULL,
  PRIMARY KEY (`bpid`),
  KEY `abc` (`branchId`),
  KEY `xyz` (`productId`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `branchproduct`
--

INSERT INTO `branchproduct` (`bpid`, `branchId`, `productId`, `branchqty`) VALUES
(2, 2, 10, 400),
(4, 1, 11, 148),
(5, 1, 12, 123),
(6, 2, 11, 50),
(7, 2, 12, 60),
(8, 1, 10, 89),
(9, 1, 14, 0),
(10, 2, 14, 0),
(11, 3, 14, 0);

-- --------------------------------------------------------

--
-- Table structure for table `grn`
--

DROP TABLE IF EXISTS `grn`;
CREATE TABLE IF NOT EXISTS `grn` (
  `grnid` int(11) NOT NULL AUTO_INCREMENT,
  `grnBillNo` varchar(50) NOT NULL,
  `total` double NOT NULL,
  `date` date DEFAULT NULL,
  `discount` double NOT NULL,
  `totalAfterDiscount` double NOT NULL,
  `paidAmount` double NOT NULL,
  `status` varchar(50) NOT NULL,
  `supplierId` int(11) NOT NULL,
  PRIMARY KEY (`grnid`),
  KEY `ccc` (`supplierId`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `grn`
--

INSERT INTO `grn` (`grnid`, `grnBillNo`, `total`, `date`, `discount`, `totalAfterDiscount`, `paidAmount`, `status`, `supplierId`) VALUES
(1, '777', 181010, '2024-07-10', 0, 181010, 5000, 'Payment Not Complete', 1),
(2, '4596', 66820, '2024-07-10', 0.05, 63479, 14000, 'Payment Not Complete', 1),
(3, '4563', 28400, '2024-07-10', 0.02, 27832, 27832, 'Payment Complete', 1);

-- --------------------------------------------------------

--
-- Table structure for table `price`
--

DROP TABLE IF EXISTS `price`;
CREATE TABLE IF NOT EXISTS `price` (
  `priceid` int(11) NOT NULL AUTO_INCREMENT,
  `productId` int(11) NOT NULL,
  `startDate` date NOT NULL,
  `price` double NOT NULL,
  PRIMARY KEY (`priceid`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `price`
--

INSERT INTO `price` (`priceid`, `productId`, `startDate`, `price`) VALUES
(2, 222, '2024-07-11', 255),
(3, 7585, '2024-07-11', 260),
(4, 222, '2024-07-11', 300);

-- --------------------------------------------------------

--
-- Table structure for table `product`
--

DROP TABLE IF EXISTS `product`;
CREATE TABLE IF NOT EXISTS `product` (
  `pid` int(11) NOT NULL AUTO_INCREMENT,
  `pname` varchar(255) NOT NULL,
  `unit` varchar(255) NOT NULL,
  `price` decimal(10,2) NOT NULL,
  `discount` decimal(10,2) NOT NULL,
  `priceAfterDiscount` decimal(10,2) NOT NULL,
  `pcode` varchar(20) NOT NULL,
  PRIMARY KEY (`pid`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `product`
--

INSERT INTO `product` (`pid`, `pname`, `unit`, `price`, `discount`, `priceAfterDiscount`, `pcode`) VALUES
(10, 'Anchor', '500g', '1020.00', '0.01', '1009.80', '444'),
(11, 'Maree', '100g', '300.00', '0.00', '250.00', '222'),
(12, 'Nice', '50g', '500.00', '0.00', '500.00', '555'),
(13, 'Apple', '5g', '100.00', '0.00', '100.00', '333'),
(14, 'Kottu Me', '15g', '260.00', '0.00', '260.00', '7585');

-- --------------------------------------------------------

--
-- Table structure for table `salesbill`
--

DROP TABLE IF EXISTS `salesbill`;
CREATE TABLE IF NOT EXISTS `salesbill` (
  `billcode` varchar(50) NOT NULL,
  `billdate` date NOT NULL,
  `billTotal` double NOT NULL,
  `discount` double NOT NULL,
  `totalAfterDiscount` double NOT NULL,
  `paymentType` varchar(50) NOT NULL,
  `userId` int(11) NOT NULL,
  `branchid` int(11) NOT NULL,
  PRIMARY KEY (`billcode`),
  KEY `yyy` (`userId`),
  KEY `rty` (`branchid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `salesbill`
--

INSERT INTO `salesbill` (`billcode`, `billdate`, `billTotal`, `discount`, `totalAfterDiscount`, `paymentType`, `userId`, `branchid`) VALUES
('7586', '2024-07-10', 2500, 0, 2500, 'Credit Card', 1, 1),
('77789', '2024-07-10', 5060, 0, 5060, 'Cash', 1, 1);

-- --------------------------------------------------------

--
-- Table structure for table `salesitem`
--

DROP TABLE IF EXISTS `salesitem`;
CREATE TABLE IF NOT EXISTS `salesitem` (
  `siid` int(11) NOT NULL AUTO_INCREMENT,
  `billId` varchar(50) NOT NULL,
  `qty` int(11) NOT NULL,
  `price` double NOT NULL,
  `total` double NOT NULL,
  `branchproductid` int(11) NOT NULL,
  PRIMARY KEY (`siid`),
  KEY `swd` (`branchproductid`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `salesitem`
--

INSERT INTO `salesitem` (`siid`, `billId`, `qty`, `price`, `total`, `branchproductid`) VALUES
(3, '77789', 3, 1020, 3060, 8),
(4, '77789', 4, 500, 2000, 5),
(5, '4542', 1, 1020, 1020, 8),
(6, '4542', 3, 500, 1500, 5),
(7, '7586', 2, 250, 500, 4),
(8, '7586', 4, 500, 2000, 5);

-- --------------------------------------------------------

--
-- Table structure for table `stockitem`
--

DROP TABLE IF EXISTS `stockitem`;
CREATE TABLE IF NOT EXISTS `stockitem` (
  `stid` int(11) NOT NULL AUTO_INCREMENT,
  `qty` int(11) NOT NULL,
  `stockPrice` double NOT NULL,
  `expDate` date NOT NULL,
  `mfDate` date NOT NULL,
  `grnBillNo` varchar(50) NOT NULL,
  `branchproductid` int(11) NOT NULL,
  PRIMARY KEY (`stid`),
  KEY `dfg` (`branchproductid`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `stockitem`
--

INSERT INTO `stockitem` (`stid`, `qty`, `stockPrice`, `expDate`, `mfDate`, `grnBillNo`, `branchproductid`) VALUES
(1, 5, 202, '2025-05-05', '2024-07-01', '777', 8),
(2, 400, 450, '2026-06-06', '2024-07-01', '777', 5),
(3, 120, 200, '2026-08-01', '2024-07-10', '4596', 8),
(4, 200, 140, '2028-08-08', '2024-02-02', '4596', 5),
(5, 95, 156, '2026-05-05', '2024-06-06', '4596', 4),
(6, 50, 200, '2028-01-01', '2024-01-01', '4563', 4),
(7, 80, 230, '2028-01-01', '2024-01-01', '4563', 5);

-- --------------------------------------------------------

--
-- Table structure for table `supplier`
--

DROP TABLE IF EXISTS `supplier`;
CREATE TABLE IF NOT EXISTS `supplier` (
  `supid` int(11) NOT NULL AUTO_INCREMENT,
  `supName` varchar(255) NOT NULL,
  `supAddress` varchar(255) NOT NULL,
  `supNic` varchar(20) NOT NULL,
  `supTel` varchar(20) NOT NULL,
  `supEmail` varchar(100) NOT NULL,
  PRIMARY KEY (`supid`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `supplier`
--

INSERT INTO `supplier` (`supid`, `supName`, `supAddress`, `supNic`, `supTel`, `supEmail`) VALUES
(1, 'Amal Silva', 'Colombo', '4545', '075455', 'amal@gmail.com');

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
CREATE TABLE IF NOT EXISTS `user` (
  `userid` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL,
  `password` varchar(100) NOT NULL,
  `nic` varchar(20) NOT NULL,
  `address` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  PRIMARY KEY (`userid`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`userid`, `username`, `password`, `nic`, `address`, `email`) VALUES
(1, 'Admin', '111', '20000000', 'Gampaha', 'amal@gmail.com'),
(2, 'abc', '123', '20000000', 'Yakkala', 'nimal@gmail.com');

--
-- Constraints for dumped tables
--

--
-- Constraints for table `branchproduct`
--
ALTER TABLE `branchproduct`
  ADD CONSTRAINT `abc` FOREIGN KEY (`branchId`) REFERENCES `branch` (`brid`) ON UPDATE CASCADE,
  ADD CONSTRAINT `xyz` FOREIGN KEY (`productId`) REFERENCES `product` (`pid`) ON UPDATE CASCADE;

--
-- Constraints for table `grn`
--
ALTER TABLE `grn`
  ADD CONSTRAINT `ccc` FOREIGN KEY (`supplierId`) REFERENCES `supplier` (`supid`) ON UPDATE CASCADE;

--
-- Constraints for table `salesbill`
--
ALTER TABLE `salesbill`
  ADD CONSTRAINT `rty` FOREIGN KEY (`branchid`) REFERENCES `branch` (`brid`) ON UPDATE CASCADE,
  ADD CONSTRAINT `yyy` FOREIGN KEY (`userId`) REFERENCES `user` (`userid`) ON UPDATE CASCADE;

--
-- Constraints for table `salesitem`
--
ALTER TABLE `salesitem`
  ADD CONSTRAINT `swd` FOREIGN KEY (`branchproductid`) REFERENCES `branchproduct` (`bpid`) ON UPDATE CASCADE;

--
-- Constraints for table `stockitem`
--
ALTER TABLE `stockitem`
  ADD CONSTRAINT `dfg` FOREIGN KEY (`branchproductid`) REFERENCES `branchproduct` (`bpid`) ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
