CREATE TABLE Trainers (
    trainer_id SERIAL PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    booking_price DECIMAL(10, 2),
    emergency_contact VARCHAR(20)
);

CREATE TABLE Members (
    member_id SERIAL PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    emergency_contact VARCHAR(20),
    weight DECIMAL(5, 2),
    goal_weight DECIMAL(5, 2)
);

CREATE TABLE Staff (
    staff_id SERIAL PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50)
);

CREATE TABLE Training_Sessions (
    session_id SERIAL PRIMARY KEY,
    trainer_id INT,
    member_id INT,
    start_time TIME,
    length INT,
    date DATE,
    FOREIGN KEY (trainer_id) REFERENCES Trainers(trainer_id),
    FOREIGN KEY (member_id) REFERENCES Members(member_id)
);

CREATE TABLE Classes (
    class_id SERIAL PRIMARY KEY,
    trainer_id INT,
    start_time TIME,
    length INT,
    date DATE,
    FOREIGN KEY (trainer_id) REFERENCES Trainers(trainer_id)
);

CREATE TABLE Fees (
    fee_id SERIAL PRIMARY KEY,
    member_id INT,
    type VARCHAR(50),
    amount DECIMAL(10, 2),
    status VARCHAR(20),
    FOREIGN KEY (member_id) REFERENCES Members(member_id)
);

CREATE TABLE Equipment (
    equipment_id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    status VARCHAR(20),
    last_maintained DATE
);

CREATE TABLE Equipment_Maintenance (
    maintenance_id SERIAL PRIMARY KEY,
    staff_id INT,
    equipment_id INT,
    maintenance_date DATE,
    status VARCHAR(20),
    FOREIGN KEY (staff_id) REFERENCES Staff(staff_id),
    FOREIGN KEY (equipment_id) REFERENCES Equipment(equipment_id)
);

CREATE TABLE Free_Timeslots (
    timeslot_id SERIAL PRIMARY KEY,
    trainer_id INT,
    date DATE,
    start_time TIME,
    length INT,
    FOREIGN KEY (trainer_id) REFERENCES Trainers(trainer_id)
);

CREATE TABLE Class_Members (
    class_member_id SERIAL PRIMARY KEY,
    class_id INT,
    member_id INT,
    FOREIGN KEY (class_id) REFERENCES Classes(class_id),
    FOREIGN KEY (member_id) REFERENCES Members(member_id)
);