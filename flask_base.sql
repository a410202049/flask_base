/*
Navicat MySQL Data Transfer

Source Server         : 本地
Source Server Version : 50636
Source Host           : localhost:3306
Source Database       : flask_base

Target Server Type    : MYSQL
Target Server Version : 50636
File Encoding         : 65001

Date: 2017-12-12 17:36:35
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for `t_menu_auth`
-- ----------------------------
DROP TABLE IF EXISTS `t_menu_auth`;
CREATE TABLE `t_menu_auth` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `parent_id` int(11) DEFAULT NULL,
  `name` varchar(20) DEFAULT NULL,
  `method` varchar(50) DEFAULT NULL,
  `type` int(11) DEFAULT NULL,
  `sort` int(11) DEFAULT NULL,
  `icon` varchar(30) DEFAULT NULL,
  `create_time` datetime NOT NULL,
  `update_time` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=81 DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC;

-- ----------------------------
-- Records of t_menu_auth
-- ----------------------------
INSERT INTO `t_menu_auth` VALUES ('1', '0', '系统首页', 'admin/index', '0', '1', 'ti-home', '2017-11-06 14:19:02', '2017-11-09 14:38:10');
INSERT INTO `t_menu_auth` VALUES ('2', '0', '权限菜单', 'admin/menu-auth', '0', '1', 'md md-menu', '2017-11-06 14:20:37', '2017-11-07 10:59:26');
INSERT INTO `t_menu_auth` VALUES ('3', '2', '添加菜单', 'admin/menu-add', '1', '1', '', '2017-11-06 14:22:13', '2017-11-07 10:59:26');
INSERT INTO `t_menu_auth` VALUES ('4', '2', '编辑菜单', 'admin/menu-edit', '1', '1', '', '2017-11-06 14:23:17', '2017-11-07 10:59:26');
INSERT INTO `t_menu_auth` VALUES ('5', '0', '角色管理', 'admin/role-manage', '0', '1', 'fa fa-users', '2017-11-06 14:24:33', '2017-11-08 09:35:05');
INSERT INTO `t_menu_auth` VALUES ('6', '5', '用户管理', 'admin/user-manage', '0', '1', '', '2017-11-06 14:25:17', '2017-11-06 14:25:20');
INSERT INTO `t_menu_auth` VALUES ('7', '5', '用户分组', 'admin/user-group-manage', '0', '2', '', '2017-11-06 14:25:51', '2017-11-06 14:25:53');
INSERT INTO `t_menu_auth` VALUES ('74', '2', '删除菜单', 'admin/menu-del', '1', '1', '', '2017-11-09 11:12:26', '2017-11-09 11:12:26');
INSERT INTO `t_menu_auth` VALUES ('75', '6', '添加用户', 'admin/user-add', '1', '1', '', '2017-11-09 11:14:26', '2017-11-09 11:14:26');
INSERT INTO `t_menu_auth` VALUES ('76', '6', '编辑用户', 'admin/user-edit', '1', '1', '', '2017-11-09 11:15:48', '2017-11-09 11:15:48');
INSERT INTO `t_menu_auth` VALUES ('77', '6', '删除用户', 'admin/user-del', '1', '1', '', '2017-11-09 11:16:31', '2017-11-09 11:16:31');
INSERT INTO `t_menu_auth` VALUES ('78', '7', '添加分组', 'admin/group-add', '1', '1', '', '2017-11-09 11:17:36', '2017-11-09 11:17:36');
INSERT INTO `t_menu_auth` VALUES ('79', '7', '编辑分组', 'admin/group-edit', '1', '1', '', '2017-11-09 11:18:04', '2017-11-09 11:18:04');
INSERT INTO `t_menu_auth` VALUES ('80', '7', '删除分组', 'admin/group-del', '1', '1', '', '2017-11-09 11:19:00', '2017-11-09 11:19:00');

-- ----------------------------
-- Table structure for `t_message`
-- ----------------------------
DROP TABLE IF EXISTS `t_message`;
CREATE TABLE `t_message` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(32) NOT NULL,
  `content` varchar(32) NOT NULL,
  `status` int(11) DEFAULT NULL,
  `push_times` int(11) DEFAULT NULL,
  `cashier_no` varchar(32) DEFAULT NULL,
  `order_no` varchar(32) DEFAULT NULL,
  `imei` varchar(64) DEFAULT NULL,
  `create_time` datetime NOT NULL,
  `update_time` datetime NOT NULL,
  `remark` varchar(128) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `ix_t_message_cashier_no` (`cashier_no`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC;

-- ----------------------------
-- Records of t_message
-- ----------------------------

-- ----------------------------
-- Table structure for `t_operation_log`
-- ----------------------------
DROP TABLE IF EXISTS `t_operation_log`;
CREATE TABLE `t_operation_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(32) DEFAULT NULL,
  `operation` varchar(32) DEFAULT NULL,
  `operate_desc` varchar(1024) DEFAULT NULL,
  `login_ip` varchar(32) DEFAULT NULL,
  `request` varchar(500) DEFAULT NULL,
  `response` varchar(500) DEFAULT NULL,
  `create_time` datetime NOT NULL,
  `update_time` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC;

-- ----------------------------
-- Records of t_operation_log
-- ----------------------------

-- ----------------------------
-- Table structure for `t_user`
-- ----------------------------
DROP TABLE IF EXISTS `t_user`;
CREATE TABLE `t_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(64) DEFAULT NULL,
  `email` varchar(64) DEFAULT NULL,
  `password_hash` varchar(128) DEFAULT NULL,
  `register_time` datetime DEFAULT NULL,
  `last_time` datetime DEFAULT NULL,
  `status` tinyint(1) DEFAULT NULL,
  `confirmed` tinyint(1) DEFAULT NULL,
  `nickname` varchar(64) DEFAULT NULL,
  `is_manage` enum('1','0') DEFAULT NULL,
  `group_id` int(11) DEFAULT NULL,
  `create_time` datetime NOT NULL,
  `update_time` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_t_user_email` (`email`),
  UNIQUE KEY `ix_t_user_username` (`username`),
  KEY `group_id` (`group_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC;

-- ----------------------------
-- Records of t_user
-- ----------------------------
INSERT INTO `t_user` VALUES ('1', 'admin', '1', 'pbkdf2:sha256:50000$BktW7bxC$5eb77497fbbcc6406cc5cfe6d8e1ce18d221c13fecef84e54bce7946b7060f7c', '2017-11-09 14:30:07', '2017-11-09 14:30:09', '1', null, '1', '1', '1', '2017-11-09 14:30:16', '2017-11-09 14:30:19');
INSERT INTO `t_user` VALUES ('2', 'gaoyuan', '1509699669@qq.com', 'pbkdf2:sha256:50000$UDO2HZlD$1e9226c5865ec7e01f46afb31ff5ebd3ae717a7ca004dfce8d5a4e3b9e3c4ef1', '2017-11-09 06:37:37', '2017-11-09 06:37:37', '1', '0', null, '1', '2', '2017-11-09 14:37:37', '2017-11-14 11:40:51');

-- ----------------------------
-- Table structure for `t_user_group`
-- ----------------------------
DROP TABLE IF EXISTS `t_user_group`;
CREATE TABLE `t_user_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(64) DEFAULT NULL,
  `status` int(11) DEFAULT NULL,
  `rules` text,
  `description` text,
  `create_time` datetime NOT NULL,
  `update_time` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC;

-- ----------------------------
-- Records of t_user_group
-- ----------------------------
INSERT INTO `t_user_group` VALUES ('1', '超级管理员', '1', '[1,2,3,4,74,5,6,75,76,77,7,78,79,80]', 'super role', '2017-11-06 15:18:39', '2017-11-09 14:36:57');
INSERT INTO `t_user_group` VALUES ('2', '编辑管理员', '1', '[1,2,3,4,74,5,6,75,76,77,7,78,79,80,82,83]', 'edit role', '2017-11-06 15:19:15', '2017-11-20 10:47:11');
