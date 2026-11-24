CREATE DATABASE clinic_system;

USE clinic_system;
-- Doctor & Schedule Service
CREATE TABLE doctors (
doctor_id INT PRIMARY KEY AUTO_INCREMENT,
name VARCHAR(100) NOT NULL,
specialty VARCHAR(50) NOT NULL,
consultation_fee DECIMAL(10,2) NOT NULL,
room VARCHAR(20)
);
CREATE TABLE slots (
slot_id INT PRIMARY KEY AUTO_INCREMENT,
doctor_id INT NOT NULL,
slot_date DATE NOT NULL,
start_time TIME NOT NULL,
status ENUM('AVAILABLE','BOOKED') NOT NULL DEFAULT 'AVAILABLE',
FOREIGN KEY (doctor_id) REFERENCES doctors(doctor_id),
UNIQUE (doctor_id, slot_date, start_time)
);
-- Patient Service
CREATE TABLE patients (
patient_id INT PRIMARY KEY AUTO_INCREMENT,
name VARCHAR(100) NOT NULL,
email VARCHAR(100) NOT NULL UNIQUE,
phone VARCHAR(20) NOT NULL,
password_hash VARCHAR(255) NOT NULL,
insurance_plan_code VARCHAR(20) NULL, -- NULL = no insurance
completed_visits INT NOT NULL DEFAULT 0,
created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
-- Appointment Service
CREATE TABLE appointments (
appointment_id INT PRIMARY KEY AUTO_INCREMENT,
patient_id INT NOT NULL,
doctor_id INT NOT NULL,
slot_id INT NOT NULL,
reason VARCHAR(255),
SOA Project: Clinic Appointment System
Page 6 of 20
status ENUM('CONFIRMED','CANCELLED','COMPLETED') NOT NULL DEFAULT
'CONFIRMED',
created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE
CURRENT_TIMESTAMP
);
-- Billing Service
CREATE TABLE insurance_plans (
plan_code VARCHAR(20) PRIMARY KEY,
plan_name VARCHAR(100) NOT NULL,
coverage_percent DECIMAL(5,2) NOT NULL, -- e.g. 80.00 = 80%
max_coverage DECIMAL(10,2) NOT NULL -- EGP cap per visit
);
CREATE TABLE invoices (
invoice_id INT PRIMARY KEY AUTO_INCREMENT,
appointment_id INT NOT NULL UNIQUE,
patient_id INT NOT NULL,
consultation_fee DECIMAL(10,2) NOT NULL,
loyalty_discount DECIMAL(10,2) NOT NULL,
insurance_covered DECIMAL(10,2) NOT NULL,
booking_fee DECIMAL(10,2) NOT NULL,
total DECIMAL(10,2) NOT NULL,
status ENUM('ISSUED','CANCELLED') NOT NULL DEFAULT 'ISSUED',
created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
-- Notification Service
CREATE TABLE notification_log (
notification_id INT PRIMARY KEY AUTO_INCREMENT,
appointment_id INT NOT NULL,
patient_id INT NOT NULL,
channel ENUM('EMAIL','SMS') NOT NULL,
type VARCHAR(30) NOT NULL, -- CONFIRMED, CANCELLED,
COMPLETED, ...
message TEXT NOT NULL,
sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


