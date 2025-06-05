CREATE DATABASE IF NOT EXISTS zipcodes_one;
USE zipcodes_one;

CREATE TABLE zipcodes (
  zipcode INT,
  state CHAR(2),
  TotalWages INT
);

INSERT INTO zipcodes (zipcode, state, TotalWages) VALUES
(40202, 'KY', 55000),
(40301, 'KY', 62000),
(19019, 'PA', 72000),
(40502, 'KY', 50000);
