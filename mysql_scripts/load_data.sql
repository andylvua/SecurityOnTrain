ALTER TABLE shift AUTO_INCREMENT = 1;
ALTER TABLE train AUTO_INCREMENT = 1;
ALTER TABLE camera AUTO_INCREMENT = 1;
ALTER TABLE passenger AUTO_INCREMENT = 1;
ALTER TABLE ticket AUTO_INCREMENT = 1;
ALTER TABLE passengerticket AUTO_INCREMENT = 1;
ALTER TABLE carriage AUTO_INCREMENT = 1;
ALTER TABLE traincarriage AUTO_INCREMENT = 1;
ALTER TABLE securitypersonnel AUTO_INCREMENT = 1;
ALTER TABLE shiftpersonnel AUTO_INCREMENT = 1;
ALTER TABLE route AUTO_INCREMENT = 1;
ALTER TABLE station AUTO_INCREMENT = 1;

load data infile 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/Station.csv' into table station
 FIELDS TERMINATED BY ',' LINES TERMINATED BY '\r\n';
SELECT * FROM station;

load data infile 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/Train.csv' into table train
 FIELDS TERMINATED BY ',' LINES TERMINATED BY '\r\n';
SELECT * FROM train;

load data infile 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/Carriage.csv' into table carriage
 FIELDS TERMINATED BY ',' LINES TERMINATED BY '\r\n';
SELECT * FROM carriage;

load data infile 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/TrainCarriage.csv' into table traincarriage
 FIELDS TERMINATED BY ',' LINES TERMINATED BY '\r\n';
SELECT * FROM traincarriage;

load data infile 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/Route.csv' into table route
 FIELDS TERMINATED BY ',' LINES TERMINATED BY '\r\n';
SELECT * FROM route;

load data infile 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/Shift.csv' into table shift
 FIELDS TERMINATED BY ',' LINES TERMINATED BY '\r\n';
SELECT * FROM shift;

load data infile 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/Camera.csv' into table camera
 FIELDS TERMINATED BY ',' LINES TERMINATED BY '\r\n';
SELECT * FROM camera;

load data infile 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/Passenger.csv' into table passenger
 FIELDS TERMINATED BY ',' LINES TERMINATED BY '\r\n';
SELECT * FROM passenger;

load data infile 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/Ticket.csv' into table ticket
 FIELDS TERMINATED BY ',' LINES TERMINATED BY '\r\n';
SELECT * FROM ticket;

load data infile 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/PassengerTicket.csv' into table passengerticket
 FIELDS TERMINATED BY ',' LINES TERMINATED BY '\r\n';
SELECT * FROM passengerticket;

load data infile 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/SecurityPersonnel.csv' into table securitypersonnel
 FIELDS TERMINATED BY ',' LINES TERMINATED BY '\r\n';
SELECT * FROM securitypersonnel;

load data infile 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/ShiftPersonnel.csv' into table shiftpersonnel
 FIELDS TERMINATED BY ',' LINES TERMINATED BY '\r\n';
SELECT * FROM shiftpersonnel;


