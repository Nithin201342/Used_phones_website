/*
SQLyog Community v13.1.6 (64 bit)
MySQL - 10.4.24-MariaDB : Database - mainproject
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
CREATE DATABASE /*!32312 IF NOT EXISTS*/`mainproject` /*!40100 DEFAULT CHARACTER SET utf8mb4 */;

USE `mainproject`;

/*Table structure for table `tbl_brand` */

DROP TABLE IF EXISTS `tbl_brand`;

CREATE TABLE `tbl_brand` (
  `brand_id` int(5) NOT NULL AUTO_INCREMENT,
  `brand_name` varchar(30) NOT NULL,
  `brand_desc` varchar(50) NOT NULL,
  `status` int(1) NOT NULL,
  PRIMARY KEY (`brand_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4;

/*Data for the table `tbl_brand` */

insert  into `tbl_brand`(`brand_id`,`brand_name`,`brand_desc`,`status`) values 
(1,'OnePlus','Never Settle',1),
(2,'Apple','Think Different',1),
(3,'Apple','Think Different',1);

/*Table structure for table `tbl_card` */

DROP TABLE IF EXISTS `tbl_card`;

CREATE TABLE `tbl_card` (
  `Card_id` int(5) NOT NULL AUTO_INCREMENT,
  `Cust_id` int(5) NOT NULL,
  `Card_num` varchar(30) NOT NULL,
  `Card_holder` varchar(30) NOT NULL,
  `Exp_date` date NOT NULL,
  PRIMARY KEY (`Card_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

/*Data for the table `tbl_card` */

/*Table structure for table `tbl_cart_child` */

DROP TABLE IF EXISTS `tbl_cart_child`;

CREATE TABLE `tbl_cart_child` (
  `Cart_child_id` int(5) NOT NULL AUTO_INCREMENT,
  `Cart_master_id` int(5) NOT NULL,
  `Item_id` int(5) NOT NULL,
  PRIMARY KEY (`Cart_child_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

/*Data for the table `tbl_cart_child` */

/*Table structure for table `tbl_cart_master` */

DROP TABLE IF EXISTS `tbl_cart_master`;

CREATE TABLE `tbl_cart_master` (
  `Cart_master_id` int(5) NOT NULL AUTO_INCREMENT,
  `Cust_id` int(5) NOT NULL,
  `Cart_status` varchar(8) NOT NULL,
  PRIMARY KEY (`Cart_master_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

/*Data for the table `tbl_cart_master` */

/*Table structure for table `tbl_category` */

DROP TABLE IF EXISTS `tbl_category`;

CREATE TABLE `tbl_category` (
  `cat_id` int(5) NOT NULL AUTO_INCREMENT,
  `cat_name` varchar(30) NOT NULL,
  `cat_desc` varchar(50) NOT NULL,
  `status` int(1) NOT NULL,
  PRIMARY KEY (`cat_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4;

/*Data for the table `tbl_category` */

insert  into `tbl_category`(`cat_id`,`cat_name`,`cat_desc`,`status`) values 
(1,'Budget-Friendly','Cheapest mobiles with maximum specifiactions',1);

/*Table structure for table `tbl_cour` */

DROP TABLE IF EXISTS `tbl_cour`;

CREATE TABLE `tbl_cour` (
  `cour_id` int(5) NOT NULL AUTO_INCREMENT,
  `cour_name` varchar(30) NOT NULL,
  `cour_gno` varchar(30) NOT NULL,
  `cour_city` varchar(30) NOT NULL,
  `cour_pin` varchar(6) NOT NULL,
  `cour_phone` varchar(10) NOT NULL,
  `status` int(1) NOT NULL,
  PRIMARY KEY (`cour_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

/*Data for the table `tbl_cour` */

/*Table structure for table `tbl_customer` */

DROP TABLE IF EXISTS `tbl_customer`;

CREATE TABLE `tbl_customer` (
  `cust_id` int(5) NOT NULL AUTO_INCREMENT,
  `email` varchar(30) NOT NULL,
  `cust_fname` varchar(30) NOT NULL,
  `cust_lname` varchar(30) NOT NULL,
  `cust_city` varchar(30) NOT NULL,
  `cust_pin` varchar(30) NOT NULL,
  `cust_phone` varchar(30) NOT NULL,
  `status` int(1) NOT NULL,
  PRIMARY KEY (`cust_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4;

/*Data for the table `tbl_customer` */

insert  into `tbl_customer`(`cust_id`,`email`,`cust_fname`,`cust_lname`,`cust_city`,`cust_pin`,`cust_phone`,`status`) values 
(1,'stf1@gmail.com','Roy','Krishna','Ernakulam','682309','9400737266',1),
(2,'marko@gmail.com','Markose','Sanil','Ernakulam','682331','9499622989',1);

/*Table structure for table `tbl_item` */

DROP TABLE IF EXISTS `tbl_item`;

CREATE TABLE `tbl_item` (
  `item_id` int(5) NOT NULL AUTO_INCREMENT,
  `cat_id` int(5) NOT NULL,
  `brand_id` int(5) NOT NULL,
  `item_name` varchar(30) NOT NULL,
  `item_profit` varchar(30) NOT NULL,
  `item_price` varchar(30) NOT NULL,
  `image` varchar(1000) NOT NULL,
  `status` int(1) NOT NULL,
  PRIMARY KEY (`item_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

/*Data for the table `tbl_item` */

/*Table structure for table `tbl_login` */

DROP TABLE IF EXISTS `tbl_login`;

CREATE TABLE `tbl_login` (
  `email` varchar(30) NOT NULL,
  `password` varchar(15) NOT NULL,
  `usertype` varchar(10) NOT NULL,
  `status` int(1) NOT NULL,
  PRIMARY KEY (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

/*Data for the table `tbl_login` */

insert  into `tbl_login`(`email`,`password`,`usertype`,`status`) values 
('admin@gmail.com','admin','admin',1),
('marko@gmail.com','neenu','customer',1),
('muzz@gmail.com','habibi','staff',1),
('staff@gmail.com','staff','staff',1),
('stf1@gmail.com','asdf','customer',1),
('zoi@gmial','123','staff',1);

/*Table structure for table `tbl_payment` */

DROP TABLE IF EXISTS `tbl_payment`;

CREATE TABLE `tbl_payment` (
  `Payment_id` int(5) NOT NULL AUTO_INCREMENT,
  `Card_id` int(5) NOT NULL,
  `Payment_date` date NOT NULL,
  PRIMARY KEY (`Payment_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

/*Data for the table `tbl_payment` */

/*Table structure for table `tbl_purchase_child` */

DROP TABLE IF EXISTS `tbl_purchase_child`;

CREATE TABLE `tbl_purchase_child` (
  `Pur_child_id` int(5) NOT NULL AUTO_INCREMENT,
  `Pur_master_id` int(5) NOT NULL,
  `Item_id` int(5) DEFAULT NULL,
  `Date` date DEFAULT NULL,
  `Cost_price` varchar(10) DEFAULT NULL,
  `Sell_price` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`Pur_child_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

/*Data for the table `tbl_purchase_child` */

/*Table structure for table `tbl_purchase_master` */

DROP TABLE IF EXISTS `tbl_purchase_master`;

CREATE TABLE `tbl_purchase_master` (
  `Pur_master_id` int(5) NOT NULL AUTO_INCREMENT,
  `Staff_id` int(5) NOT NULL,
  `Cust_id` int(5) NOT NULL,
  `Tot_amt` int(10) NOT NULL,
  `Date` date NOT NULL,
  `Staus` int(1) NOT NULL,
  PRIMARY KEY (`Pur_master_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

/*Data for the table `tbl_purchase_master` */

/*Table structure for table `tbl_staff` */

DROP TABLE IF EXISTS `tbl_staff`;

CREATE TABLE `tbl_staff` (
  `staff_id` int(5) NOT NULL AUTO_INCREMENT,
  `email` varchar(30) NOT NULL,
  `staff_fname` varchar(15) NOT NULL,
  `staff_lname` varchar(15) NOT NULL,
  `staff_city` varchar(15) NOT NULL,
  `staff_phone` varchar(10) NOT NULL,
  `staff_gender` varchar(10) NOT NULL,
  `status` int(1) NOT NULL,
  PRIMARY KEY (`staff_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4;

/*Data for the table `tbl_staff` */

insert  into `tbl_staff`(`staff_id`,`email`,`staff_fname`,`staff_lname`,`staff_city`,`staff_phone`,`staff_gender`,`status`) values 
(1,'staff@gmail.com','Rohan','Kishore','Kochi','9496229898','Male',1),
(2,'muzz@gmail.com','Dhashamoolum','Dhamu','Dubai','0561397098','Male',1),
(3,'zoi@gmial','Zoi','Sanil','Ernakulam','9465456543','Male',1);

/*Table structure for table `tbl_subcategory` */

DROP TABLE IF EXISTS `tbl_subcategory`;

CREATE TABLE `tbl_subcategory` (
  `Subcat_id` int(5) NOT NULL AUTO_INCREMENT,
  `Subcat_name` varchar(30) NOT NULL,
  `Status` int(1) NOT NULL,
  PRIMARY KEY (`Subcat_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

/*Data for the table `tbl_subcategory` */

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
