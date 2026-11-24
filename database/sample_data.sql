INSERT INTO doctors (name, specialty, consultation_fee, room) VALUES
('Dr. Mona Khaled', 'Cardiology', 600.00, 'A-101'),
('Dr. Hany Fawzy', 'ENT', 350.00, 'A-102'),
('Dr. Salma Adel', 'Dermatology', 400.00, 'B-201'),
('Dr. Omar Nabil', 'Pediatrics', 300.00, 'B-202'),
('Dr. Laila Samir', 'Dentistry', 250.00, 'C-301');
-- 4 slots for every doctor (20 rows)
INSERT INTO slots (doctor_id, slot_date, start_time)
SELECT d.doctor_id, t.slot_date, t.start_time
FROM doctors d
CROSS JOIN (
SELECT '2026-12-27' AS slot_date, '10:00:00' AS start_time
UNION ALL SELECT '2026-12-27', '10:30:00'
UNION ALL SELECT '2026-12-28', '11:00:00'
UNION ALL SELECT '2026-12-28', '11:30:00'
) t;
INSERT INTO insurance_plans (plan_code, plan_name, coverage_percent, max_coverage) VALUES
('BASIC', 'Basic Health', 50.00, 200.00),
('GOLD', 'Gold Care', 80.00, 500.00),
('STAFF', 'University Staff', 100.00, 300.00);
