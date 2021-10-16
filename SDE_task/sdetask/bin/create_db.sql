DROP TABLE IF EXISTS accounts;
DROP TABLE IF EXISTS accounts_customer_link;
DROP TABLE IF EXISTS customers;
DROP TABLE IF EXISTS properties;

CREATE TABLE properties (
    pt_property_number NUMERIC PRIMARY KEY,
    pt_in_possession CHAR,
    pt_property_type CHAR,
    pt_detachment_type CHAR,
    pt_year_built NUMERIC,
    pt_region CHAR
);

CREATE TABLE products (
    pd_product_number NUMERIC PRIMARY KEY,
    pd_product_code CHAR,
    pd_product_type CHAR,
    pd_product_fixed_ind CHAR,
    pd_product_flexible_ind CHAR,
    pd_product_tracker_ind CHAR,
    pd_product_variable_ind CHAR,
    pd_product_capped_ind CHAR,
    pd_product_discount_ind CHAR
);

CREATE TABLE accounts (
    a_account_number NUMERIC PRIMARY KEY,
    a_property_number NUMERIC,
    a_product_number NUMERIC,
    a_account_balance NUMERIC,
    a_arrears_balance NUMERIC,
    a_regular_payment_amount NUMERIC,
    a_term_date DATE,
    FOREIGN KEY (a_property_number)
        REFERENCES properties (pt_property_number),
    FOREIGN KEY (a_product_number)
        REFERENCES products (pd_product_number)
);

CREATE TABLE customers (
    c_customer_number NUMERIC PRIMARY KEY,
    c_deceased_date DATE,
    c_bankruptcy_ind CHAR
);

CREATE TABLE accounts_customer_link (
    acl_account_number NUMERIC,
    acl_customer_number NUMERIC,
    acl_customer_pos NUMERIC
);


.mode csv
.import raw/prop.csv properties
.import raw/prod.csv products
.import raw/acc.csv accounts
.import raw/cust.csv customers
.import raw/acc_cust_link.csv accounts_customer_link