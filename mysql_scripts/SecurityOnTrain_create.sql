-- MySQL Script generated by MySQL Workbench
-- Sat May 13 20:29:58 2023
-- Model: New Model    Version: 1.0
-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema securityonatrain
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema securityonatrain
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `securityonatrain` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci ;
USE `securityonatrain` ;

-- -----------------------------------------------------
-- Table `securityonatrain`.`carriage`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `securityonatrain`.`carriage` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `capacity` INT NOT NULL,
  `type` ENUM('VIP', '1class', '2class', 'restaurant') NULL DEFAULT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB
AUTO_INCREMENT = 40
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `securityonatrain`.`station`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `securityonatrain`.`station` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NOT NULL,
  `location` VARCHAR(45) NOT NULL,
  `capacity` INT NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB
AUTO_INCREMENT = 32
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `securityonatrain`.`camera`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `securityonatrain`.`camera` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `locationId` INT NULL DEFAULT NULL,
  `locationType` ENUM('Carriage', 'Station') NOT NULL,
  `status` VARCHAR(45) NOT NULL,
  `datastorage` TEXT(50) NULL,
  PRIMARY KEY (`id`),
  INDEX `idCarriage_idx` (`locationId` ASC) VISIBLE,
  INDEX `idStation_idx` (`locationId` ASC) VISIBLE,
  CONSTRAINT `idCarriage`
    FOREIGN KEY (`locationId`)
    REFERENCES `securityonatrain`.`carriage` (`id`),
  CONSTRAINT `idStation`
    FOREIGN KEY (`locationId`)
    REFERENCES `securityonatrain`.`station` (`id`))
ENGINE = InnoDB
AUTO_INCREMENT = 32
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `securityonatrain`.`passenger`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `securityonatrain`.`passenger` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `firstname` VARCHAR(45) NOT NULL,
  `surname` VARCHAR(45) NOT NULL,
  `age` INT NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB
AUTO_INCREMENT = 32
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `securityonatrain`.`train`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `securityonatrain`.`train` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NULL DEFAULT NULL,
  `type` ENUM('Freight', 'Passenger') NOT NULL,
  `numOfCarriages` INT NOT NULL,
  `capacity` INT NULL DEFAULT NULL,
  `departureStationId` INT NULL,
  `destinationStationId` INT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `idTrain_UNIQUE` (`id` ASC) VISIBLE,
  INDEX `depId_idx` (`departureStationId` ASC) VISIBLE,
  INDEX `arrId_idx` (`destinationStationId` ASC) VISIBLE,
  CONSTRAINT `depId`
    FOREIGN KEY (`departureStationId`)
    REFERENCES `securityonatrain`.`station` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `arrId`
    FOREIGN KEY (`destinationStationId`)
    REFERENCES `securityonatrain`.`station` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
AUTO_INCREMENT = 14
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `securityonatrain`.`route`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `securityonatrain`.`route` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `idTrain` INT NOT NULL,
  `idStation` INT NOT NULL,
  `arrivalTime` DATETIME NOT NULL,
  `departureTime` DATETIME NOT NULL,
  PRIMARY KEY (`id`, `idTrain`, `idStation`),
  INDEX `station_idx` (`idStation` ASC) VISIBLE,
  UNIQUE INDEX `id_UNIQUE` (`id` ASC) VISIBLE,
  CONSTRAINT `station`
    FOREIGN KEY (`idStation`)
    REFERENCES `securityonatrain`.`station` (`id`)
    ON UPDATE CASCADE,
  CONSTRAINT `train`
    FOREIGN KEY (`idTrain`)
    REFERENCES `securityonatrain`.`train` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `securityonatrain`.`securitypersonnel`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `securityonatrain`.`securitypersonnel` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `firstname` VARCHAR(45) NOT NULL,
  `surname` VARCHAR(45) NOT NULL,
  `age` INT NOT NULL,
  `role` ENUM('onStation', 'onTrain', 'Dispatcher') NOT NULL,
  `locationId` INT NULL DEFAULT NULL,
  `locationType` ENUM('Carriage', 'Station') NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `locationId_idx` (`locationId` ASC) VISIBLE,
  CONSTRAINT `carriageId`
    FOREIGN KEY (`locationId`)
    REFERENCES `securityonatrain`.`carriage` (`id`)
    ON DELETE SET NULL
    ON UPDATE CASCADE,
  CONSTRAINT `stationId`
    FOREIGN KEY (`locationId`)
    REFERENCES `securityonatrain`.`station` (`id`)
    ON DELETE SET NULL
    ON UPDATE CASCADE)
ENGINE = InnoDB
AUTO_INCREMENT = 32
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `securityonatrain`.`shift`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `securityonatrain`.`shift` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `startTime` DATETIME NOT NULL,
  `endTime` DATETIME NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB
AUTO_INCREMENT = 17
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `securityonatrain`.`shiftpersonnel`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `securityonatrain`.`shiftpersonnel` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `idShift` INT NOT NULL,
  `idPersonnel` INT NOT NULL,
  PRIMARY KEY (`id`, `idShift`, `idPersonnel`),
  INDEX `personnelId_idx` (`idPersonnel` ASC) VISIBLE,
  UNIQUE INDEX `id_UNIQUE` (`id` ASC) VISIBLE,
  CONSTRAINT `personnelId`
    FOREIGN KEY (`idPersonnel`)
    REFERENCES `securityonatrain`.`securitypersonnel` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `shiftId`
    FOREIGN KEY (`idShift`)
    REFERENCES `securityonatrain`.`shift` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `securityonatrain`.`traincarriage`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `securityonatrain`.`traincarriage` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `idTrain` INT NOT NULL,
  `idCarriage` INT NOT NULL,
  PRIMARY KEY (`id`, `idTrain`, `idCarriage`),
  INDEX `fk_train_has_carriage_carriage1_idx` (`idCarriage` ASC) VISIBLE,
  INDEX `fk_train_has_carriage_train1_idx` (`idTrain` ASC) VISIBLE,
  UNIQUE INDEX `id_UNIQUE` (`id` ASC) VISIBLE,
  CONSTRAINT `fk_train_has_carriage_train1`
    FOREIGN KEY (`idTrain`)
    REFERENCES `securityonatrain`.`train` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_train_has_carriage_carriage1`
    FOREIGN KEY (`idCarriage`)
    REFERENCES `securityonatrain`.`carriage` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `securityonatrain`.`ticket`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `securityonatrain`.`ticket` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `idTrain` INT NOT NULL,
  `idCarriage` INT NOT NULL,
  `seatNum` INT NOT NULL,
  `departureStationId` INT NOT NULL,
  `destinationStationId` INT NOT NULL,
  PRIMARY KEY (`id`, `idCarriage`),
  INDEX `idCarr_idx` (`idCarriage` ASC) INVISIBLE,
  INDEX `idTrain_in_idx` (`idTrain` ASC) VISIBLE,
  CONSTRAINT `idCarr`
    FOREIGN KEY (`idCarriage`)
    REFERENCES `securityonatrain`.`carriage` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `idTrain_in`
    FOREIGN KEY (`idTrain`)
    REFERENCES `securityonatrain`.`traincarriage` (`idTrain`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `securityonatrain`.`passengerticket`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `securityonatrain`.`passengerticket` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `idPassenger` INT NOT NULL,
  `idTicket` INT NOT NULL,
  PRIMARY KEY (`id`, `idPassenger`, `idTicket`),
  INDEX `fk_ticket_has_passenger_passenger1_idx` (`idPassenger` ASC) VISIBLE,
  INDEX `fk_ticket_has_passenger_ticket1_idx` (`idTicket` ASC) VISIBLE,
  UNIQUE INDEX `id_UNIQUE` (`id` ASC) VISIBLE,
  CONSTRAINT `fk_ticket_has_passenger_ticket1`
    FOREIGN KEY (`idTicket`)
    REFERENCES `securityonatrain`.`ticket` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_ticket_has_passenger_passenger1`
    FOREIGN KEY (`idPassenger`)
    REFERENCES `securityonatrain`.`passenger` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
