CREATE TABLE stickers (
    sid BIGINT(7) NOT NULL AUTO_INCREMENT, 
    url VARCHAR(255),
    filename VARCHAR(100),
    category VARCHAR(100),
    created TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
    PRIMARY KEY (sid));

CREATE TABLE categories (
    cid BIGINT(7) NOT NULL AUTO_INCREMENT,
    category VARCHAR(100),
    folder VARCHAR(100),
    folder2 VARCHAR(100),
    created TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
    PRIMARY KEY (cid));

CREATE TABLE belong (
    bid BIGINT(7) NOT NULL AUTO_INCREMENT,
    sid BIGINT(7),
    cid BIGINT(7),
    created TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
    PRIMARY KEY (bid));

CREATE TABLE users (
    uid BIGINT(7) NOT NULL AUTO_INCREMENT,
    uname VARCHAR(100),
    openid VARCHAR(100),
    created TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
    PRIMARY KEY (uid));


CREATE TABLE collect
 (
    collect_id BIGINT(7) NOT NULL AUTO_INCREMENT comment '收藏ID', 
    collect_name VARCHAR(255) comment '收藏名', 
    sid BIGINT(7) comment '表情id', 
    uid BIGINT(7) comment '用户id', 
    created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (collect_id)
 );