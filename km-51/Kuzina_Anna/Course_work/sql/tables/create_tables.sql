DROP TABLE gift_category;

DROP TABLE gift_feature;

DROP TABLE user_feature;

DROP TABLE category_;

DROP TABLE feature;

DROP TABLE user_info;

DROP TABLE gift;

CREATE TABLE category_ (
    category_name      VARCHAR2(30),
    category_deleted   DATE DEFAULT NULL
);

ALTER TABLE category_ ADD CONSTRAINT category__pk PRIMARY KEY ( category_name );

CREATE TABLE feature (
    feature_name      VARCHAR2(30),
    feature_deleted   DATE DEFAULT NULL
);

ALTER TABLE feature ADD CONSTRAINT feature_pk PRIMARY KEY ( feature_name );

CREATE TABLE gift (
    gift_name      VARCHAR2(30),
    gift_price     FLOAT,
    gift_desc      CLOB,
    gift_deleted   DATE DEFAULT NULL
);

ALTER TABLE gift ADD CONSTRAINT gift_pk PRIMARY KEY ( gift_name );

CREATE TABLE gift_category (
    category_category_name   VARCHAR2(30) NOT NULL,
    gift_gift_name           VARCHAR2(30) NOT NULL
);

ALTER TABLE gift_category ADD CONSTRAINT gift_category_pk PRIMARY KEY ( category_category_name,
                                                                        gift_gift_name );

CREATE TABLE gift_feature (
    feature_feature_name   VARCHAR2(30) NOT NULL,
    gift_gift_name         VARCHAR2(30) NOT NULL
);

ALTER TABLE gift_feature ADD CONSTRAINT gift_feature_pk PRIMARY KEY ( feature_feature_name,
                                                                      gift_gift_name );

CREATE TABLE user_feature (
    user_info_user_login   VARCHAR2(30) NOT NULL,
    feature_feature_name   VARCHAR2(30) NOT NULL
);

ALTER TABLE user_feature ADD CONSTRAINT user_have_feature_pk PRIMARY KEY ( user_info_user_login,
                                                                           feature_feature_name );

CREATE TABLE user_info (
    user_login      VARCHAR2(30),
    user_name       VARCHAR2(30),
    user_password   VARCHAR2(30)
);

ALTER TABLE user_info ADD CONSTRAINT user_info_pk PRIMARY KEY ( user_login );

ALTER TABLE gift_category
    ADD CONSTRAINT gift_category_category_fk FOREIGN KEY ( category_category_name )
        REFERENCES category_ ( category_name )
            ON DELETE CASCADE;

ALTER TABLE gift_category
    ADD CONSTRAINT gift_category_gift_fk FOREIGN KEY ( gift_gift_name )
        REFERENCES gift ( gift_name )
            ON DELETE CASCADE;

ALTER TABLE gift_feature
    ADD CONSTRAINT gift_feature_feature_fk FOREIGN KEY ( feature_feature_name )
        REFERENCES feature ( feature_name )
            ON DELETE CASCADE;

ALTER TABLE gift_feature
    ADD CONSTRAINT gift_feature_gift_fk FOREIGN KEY ( gift_gift_name )
        REFERENCES gift ( gift_name )
            ON DELETE CASCADE;

ALTER TABLE user_feature
    ADD CONSTRAINT user_have_feature_feature_fk FOREIGN KEY ( feature_feature_name )
        REFERENCES feature ( feature_name )
            ON DELETE CASCADE;

ALTER TABLE user_feature
    ADD CONSTRAINT user_have_feature_user_info_fk FOREIGN KEY ( user_info_user_login )
        REFERENCES user_info ( user_login )
            ON DELETE CASCADE;