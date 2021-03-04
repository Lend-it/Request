CREATE DATABASE requestLendItDB_dev
    WITH
        ENCODING = UTF8
        LC_COLLATE = 'pt_BR.UTF-8'
        LC_CTYPE = 'pt_BR.UTF-8'
        TEMPLATE = template0;

\c requestlenditdb_dev

CREATE TABLE PRODUCT_CATEGORY (
    productCategoryId SMALLSERIAL NOT NULL,
    name TEXT NOT NULL,

    CONSTRAINT PRODUCT_CATEGORY_PK PRIMARY KEY (productCategoryId)
);

CREATE TABLE REQUEST (
    requestId UUID NOT NULL,
    productName TEXT NOT NULL,
    startDate DATE NOT NULL,
    endDate DATE NOT NULL,
    description TEXT NOT NULL,
    requester TEXT NOT NULL,
    lender TEXT NULL,
    productCategoryId SMALLSERIAL NOT NULL,

    CONSTRAINT REQUEST_PK PRIMARY KEY (requestId),

    CONSTRAINT REQUEST_PRODUCT_CATEGORY_FK FOREIGN KEY (productCategoryId)
        REFERENCES PRODUCT_CATEGORY (productCategoryId)
        ON DELETE RESTRICT
        ON UPDATE RESTRICT,

    CONSTRAINT VALID_REQUESTER_EMAIL CHECK (requester ~* '^[\w\-\.]+@([\w-]+\.)+[\w-]{2,4}$'),
    CONSTRAINT VALID_LENDER_EMAIL CHECK (lender ~* '^[\w\-\.]+@([\w-]+\.)+[\w-]{2,4}$'),
    CONSTRAINT VALID_LENDER_USER CHECK (requester <> lender)
);