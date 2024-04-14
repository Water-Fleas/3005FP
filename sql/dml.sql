INSERT INTO Trainers (first_name, last_name, booking_price, emergency_contact)
VALUES 
('Grace', 'Hopper', 90.00, '123-456-7890'),
('John', 'Snow', 40.00, '123-456-7890');

INSERT INTO Members (first_name, last_name, emergency_contact, weight, goal_weight)
VALUES 
('He', 'Zheng', '111-111-1111', 150.5, 140.0),
('William', 'Shakespeare', '222-222-2222', 180.0, 170.0);

INSERT INTO Staff (first_name, last_name)
VALUES 
('Sunsin', 'Yi'),
('Ngola', 'Nzinga');

INSERT INTO Training_Sessions (trainer_id, member_id, start_time, length, date)
VALUES 
(1, 1, '2024-04-13 11:00:00', 90, '2024-04-13'),
(1, 2, '2024-04-14 14:00:00', 90, '2024-04-13'),
(2, 2, '2024-04-14 09:00:00', 60, '2024-04-13');

INSERT INTO Classes (trainer_id, start_time, length, date)
VALUES 
(2, '18:00:00', 60, '2024-04-15'),
(2, '12:00:00', 60, '2024-04-13'),
(1, '17:30:00', 90, '2024-04-16');

INSERT INTO Fees (member_id, type, amount, status)
VALUES 
(1, 'Membership Fee', 100.00, 'Paid'),
(1, 'Personal Training', 90.00, 'Pending'),
(2, 'Personal Training', 90.00, 'Paid'),
(2, 'Personal Training', 80.00, 'Paid');

INSERT INTO Equipment (name, status, last_maintained)
VALUES 
('Treadmill', 'Operational', '2024-03-01'),
('Elliptical', 'Under Maintenance', '2024-04-13');

INSERT INTO Equipment_Maintenance (staff_id, equipment_id, maintenance_date, status)
VALUES 
(1, 2, '2024-04-13', 'Incomplete'),
(2, 1, '2024-03-15', 'Complete');

INSERT INTO Free_Timeslots (trainer_id, date, start_time, length)
VALUES
(1, '2024-04-13', '08:00:00', 90),
(1, '2024-04-13', '09:30:00', 90),
(1, '2024-04-13', '12:30:00', 90),
(1, '2024-04-13', '15:30:00', 90),
(2, '2024-04-13', '08:00:00', 30),
(2, '2024-04-13', '08:30:00', 30),
(2, '2024-04-13', '09:00:00', 30),
(2, '2024-04-13', '09:30:00', 30),
(2, '2024-04-13', '10:00:00', 30),
(2, '2024-04-13', '10:30:00', 30),
(2, '2024-04-13', '11:00:00', 30),
(2, '2024-04-13', '11:30:00', 30),
(2, '2024-04-13', '13:00:00', 30),
(2, '2024-04-13', '13:30:00', 30),
(2, '2024-04-13', '14:00:00', 30),
(2, '2024-04-13', '14:30:00', 30),
(2, '2024-04-13', '15:00:00', 30),
(2, '2024-04-13', '15:30:00', 30),
(2, '2024-04-13', '16:00:00', 30),
(2, '2024-04-13', '16:30:00', 30);

INSERT INTO Class_Members (class_id, member_id)
VALUES 
(1, 1);