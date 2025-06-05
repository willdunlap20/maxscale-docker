CREATE DATABASE IF NOT EXISTS zipcodes_two;
USE zipcodes_two;

CREATE TABLE zipcodes (
  zipcode INT,
  state CHAR(2),
  TotalWages INT
);

INSERT INTO zipcodes (zipcode, state, TotalWages) VALUES
(41001, 'KY', 58000),
(41102, 'KY', 61000),
(19103, 'PA', 75000),
(99999, 'CA', 88000)
