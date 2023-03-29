-- phpMyAdmin SQL Dump
-- version 2.11.6
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Mar 17, 2023 at 03:54 PM
-- Server version: 5.0.51
-- PHP Version: 5.2.6

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `multi_disease`
--

-- --------------------------------------------------------

--
-- Table structure for table `admin`
--

CREATE TABLE `admin` (
  `username` varchar(20) NOT NULL,
  `password` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `admin`
--

INSERT INTO `admin` (`username`, `password`) VALUES
('admin', 'admin');

-- --------------------------------------------------------

--
-- Table structure for table `doctor`
--

CREATE TABLE `doctor` (
  `id` int(11) NOT NULL,
  `name` varchar(20) NOT NULL,
  `mobile` bigint(20) NOT NULL,
  `email` varchar(30) NOT NULL,
  `uname` varchar(20) NOT NULL,
  `pass` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `doctor`
--

INSERT INTO `doctor` (`id`, `name`, `mobile`, `email`, `uname`, `pass`) VALUES
(1, 'Siva', 9567834223, 'siva@gmail.com', 'siva', '1234'),
(2, 'Ram', 9360967387, 'ram@gmail.com', 'ram', '1234');

-- --------------------------------------------------------

--
-- Table structure for table `patient`
--

CREATE TABLE `patient` (
  `id` int(11) NOT NULL,
  `name` varchar(20) NOT NULL,
  `gender` varchar(19) NOT NULL,
  `dob` varchar(15) NOT NULL,
  `mobile` bigint(20) NOT NULL,
  `email` varchar(30) NOT NULL,
  `uname` varchar(20) NOT NULL,
  `pass` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `patient`
--

INSERT INTO `patient` (`id`, `name`, `gender`, `dob`, `mobile`, `email`, `uname`, `pass`) VALUES
(1, 'Raj', 'Male', '24-10-1998', 9360967387, 'raj@gmail.com', 'raj', '1234'),
(2, 'Ramesh', 'Male', '1998-06-05', 7894562555, 'ramesh@gmail.com', 'ramesh', '123456');

-- --------------------------------------------------------

--
-- Table structure for table `suggest`
--

CREATE TABLE `suggest` (
  `id` int(11) NOT NULL,
  `pid` varchar(20) NOT NULL,
  `suggestion` varchar(100) NOT NULL,
  `prescription` varchar(100) NOT NULL,
  `rdate` varchar(15) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `suggest`
--

INSERT INTO `suggest` (`id`, `pid`, `suggestion`, `prescription`, `rdate`) VALUES
(1, 'raj', 'assasa', 'fgdfgdf', '05-04-2021');

-- --------------------------------------------------------

--
-- Table structure for table `test_data`
--

CREATE TABLE `test_data` (
  `id` int(11) NOT NULL,
  `name` varchar(20) NOT NULL,
  `gender` varchar(10) NOT NULL,
  `age` int(11) NOT NULL,
  `height` double NOT NULL,
  `weight` double NOT NULL,
  `glucose_level` double NOT NULL,
  `blood_pressure` double NOT NULL,
  `result` double NOT NULL,
  `date_time` timestamp NOT NULL default CURRENT_TIMESTAMP on update CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `test_data`
--

