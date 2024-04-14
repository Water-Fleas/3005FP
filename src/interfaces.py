import database as db

def registrationInterface():
    print("Thank you for deciding to make account here.")
    name = input("What is your first name? ")
    lastname = input("What is your last name? ")
    weight = input("What is your weight (kilograms)? ")
    goalweight = input("What is your goal weight? ")
    emergencycontact = input("What is your emergency contact's phone number? ")
    fetch = db.query(f"INSERT INTO Members (first_name, last_name, emergency_contact, weight, goal_weight) VALUES ('{name}', '{lastname}', '{emergencycontact}', {weight}, {goalweight}) RETURNING member_id")
    print(f"Your member ID is {fetch[0][0]}. Remember it!")
    return fetch[0][0]

def profileUpdateInterface(member_id):
    print("Updating Profile.")
    name = input("What is your first name? ")
    lastname = input("What is your last name? ")
    weight = input("What is your weight (kilograms)? ")
    goalweight = input("What is your goal weight? ")
    emergencycontact = input("What is your emergency contact's phone number? ")
    db.query(f"UPDATE Members SET first_name = '{name}', last_name = '{lastname}', emergency_contact = '{emergencycontact}', weight = {weight}, goal_weight = {goalweight} WHERE member_id = {member_id}")

def trainingSessionInterface(member_id):
    trainers = db.query("SELECT first_name, last_name, booking_price, trainer_id FROM Trainers")
    for trainer in trainers:
        print(f'{trainer[3]}. {trainer[0]} {trainer[1]}, Price: {float(trainer[2])} per session')
    trainer_id = input("Which trainer would you like to select? ")
    open_slots = db.query(f"SELECT timeslot_id, date, start_time, length FROM Free_Timeslots WHERE trainer_id = {trainer_id}")
    for open_slot in open_slots:
        date_str = open_slot[1].strftime("%Y-%m-%d")
        time_str = open_slot[2].strftime("%H:%M:%S")
        print(f'{open_slot[0]}. {date_str} at {time_str} for {open_slot[3]} minutes.')
    slot_chosen = input("Which slot would you like to select?" )
    slot_info = db.query(f"SELECT start_time, length, date FROM Free_Timeslots WHERE timeslot_id = {slot_chosen}")
    start_time, length, date = slot_info[0][0], slot_info[0][1], slot_info[0][2]
    db.query(f"DELETE FROM Free_Timeslots WHERE timeslot_id = {slot_chosen}")
    db.query(f"INSERT INTO Training_Sessions (trainer_id, member_id, start_time, length, date) VALUES ({trainer_id}, {member_id}, '{start_time}', {length}, '{date}')")
    booking_price = db.query(f"SELECT booking_price FROM Trainers WHERE trainer_id = {trainer_id}")[0][0]
    db.query(f"INSERT INTO Fees (member_id, type, amount, status) VALUES ({member_id}, 'Training Session', {booking_price}, 'Pending')")
    print("Training session scheduled! Please check your fees.")

def joinClassInterface(member_id):
    classes = db.query("SELECT c.class_id, c.start_time, date, c.length, t.booking_price, c.trainer_id FROM Classes c JOIN Trainers t ON c.trainer_id = t.trainer_id")
    print("Available classes:")
    for class_info in classes:
        date_str = class_info[2].strftime("%Y-%m-%d")
        time_str = class_info[1].strftime("%H:%M:%S")
        print(f'{class_info[0]}. {date_str} at {time_str} for {class_info[3]} minutes for {class_info[4]} dollars.')

    class_id = int(input("Which class would you like to join? "))
    db.query(f"INSERT INTO Class_Members (class_id, member_id) VALUES ({class_id}, {member_id})")

    for class_info in classes:
        if class_info[0] == class_id:
            booking_price = class_info[4]
    db.query(f"INSERT INTO Fees (member_id, type, amount, status) VALUES ({member_id}, 'Class Fee', {booking_price}, 'Pending')")

def memberInterface(member_id, name):
    print(f"Welcome, {name}!")
    while True:
        print("0. View your profile.")
        print("1. Update your profile.")
        print("2. Delete your account.")
        print("3. Schedule a training session.")
        print("4. Join a class.")
        print("5. View your fees.")
        print("6. Pay a fee.")
        print("7. View your schedule.")
        print("8. Go back.")
        selection = int(input("Please input what you would like to do today: "))
        if selection == 0:
            fetch = db.query(f"SELECT * FROM Members WHERE member_id = {member_id}")
            print("Member ID:", fetch[0][0])
            print("First Name:", fetch[0][1])
            print("Last Name:", fetch[0][2])
            print("Emergency Contact:", fetch[0][3])
            print("Weight:", fetch[0][4])
            print("Goal Weight:", fetch[0][5])
            print()
        if selection == 1:
            profileUpdateInterface(member_id)
        if selection == 2:
            db.query(f"DELETE FROM Members WHERE member_id = {member_id}")
            print("Account deleted.")
            break
        if selection == 3:
            trainingSessionInterface(member_id)
        if selection == 4:
            joinClassInterface(member_id)
        if selection == 5:
            fees = db.query(f"SELECT * FROM Fees WHERE member_id = {member_id}")
            for fee in fees:
                print(f"{fee[2]}: {float(fee[3])}, {fee[4]}")
            print()
        if selection == 6:
            fees = db.query(f"SELECT * FROM Fees WHERE member_id = {member_id} AND status = 'Pending'")
            for fee in fees:
                print(f"{fee[0]}. {fee[2]}: {float(fee[3])}, {fee[4]}")
            print()
            fee_to_pay = input("Which Fee would you like to pay? ")
            db.query(f"UPDATE Fees SET status = 'Paid' WHERE fee_id = {fee_to_pay}")
        if selection == 7:
            events = db.query(
                f'''
                SELECT 'Training' AS event_type,
                    trainer_id,
                    start_time,
                    length,
                    date
                FROM Training_Sessions
                WHERE member_id = {member_id}
                AND date >= CURRENT_DATE
                UNION
                SELECT 'Class' AS event_type,
                    trainer_id,
                    start_time,
                    length,
                    date
                FROM Classes
                WHERE date >= CURRENT_DATE
                AND class_id IN (
                    SELECT class_id
                    FROM Class_Members
                    WHERE member_id = {member_id}
                )
                ORDER BY date, start_time;
                '''
            )
            for event in events:
                date_str = event[4].strftime("%Y-%m-%d")
                time_str = event[2].strftime("%H:%M:%S")
                print(f'{event[0]} on {date_str} at {time_str} for {event[3]} minutes.')
        if selection == 8:
            print("Exiting interface.")
            break
        
def trainerInterface(trainer_id, name):
    print(f"Welcome, {name}!")
    while True:
        print("0. View a member's profile.")
        print("1. Delete an open timeslot.")
        print("2. Create an open timeslot.")
        print("3. View your schedule.")
        print("4. Go back.")
        selection = int(input("Please input what you would like to do today: "))
        if selection == 0:
            member_id = input("Which member's profile would you like to look at?")
            fetch = db.query(f"SELECT * FROM Members WHERE member_id = {member_id}")
            print("Member ID:", fetch[0][0])
            print("First Name:", fetch[0][1])
            print("Last Name:", fetch[0][2])
            print("Emergency Contact:", fetch[0][3])
            print("Weight:", fetch[0][4])
            print("Goal Weight:", fetch[0][5])
            print()
        if selection == 1:
            open_slots = db.query(f"SELECT timeslot_id, date, start_time, length FROM Free_Timeslots WHERE trainer_id = {trainer_id}")
            for open_slot in open_slots:
                date_str = open_slot[1].strftime("%Y-%m-%d")
                time_str = open_slot[2].strftime("%H:%M:%S")
                print(f'{open_slot[0]}. {date_str} at {time_str} for {open_slot[3]} minutes.')
            slot_chosen = input("Which slot would you like to select?" )
            db.query(f"DELETE FROM Free_Timeslots WHERE timeslot_id = {slot_chosen}")
        if selection == 2:
            date = input("Enter date (YYYY-MM-DD): ")
            start_time = input("Enter start time (HH:MM:SS): ")
            length = int(input("Enter length in minutes: "))
            db.query(f"INSERT INTO Free_Timeslots (trainer_id, date, start_time, length) VALUES ({trainer_id}, '{date}', '{start_time}', {length})")
        if selection == 3:
            events = db.query(
                f'''
                SELECT 'Training' AS event_type,
                    trainer_id,
                    start_time,
                    length,
                    date
                FROM Training_Sessions
                WHERE trainer_id = {trainer_id}
                AND date >= CURRENT_DATE
                UNION
                SELECT 'Class' AS event_type,
                    trainer_id,
                    start_time,
                    length,
                    date
                FROM Classes
                WHERE date >= CURRENT_DATE
                AND class_id IN (
                    SELECT class_id
                    FROM Class_Members
                    WHERE trainer_id = {trainer_id}
                )
                ORDER BY date, start_time;
                '''
            )
            for event in events:
                date_str = event[4].strftime("%Y-%m-%d")
                time_str = event[2].strftime("%H:%M:%S")
                print(f'{event[0]} on {date_str} at {time_str} for {event[3]} minutes.')
        if selection == 4:
            print("Exiting interface.")
            break

def classCreationInterface():
    trainers = db.query("SELECT first_name, last_name, booking_price, trainer_id FROM Trainers")
    for trainer in trainers:
        print(f'{trainer[3]}. {trainer[0]} {trainer[1]}, Price: {float(trainer[2])} per session')
    trainer_id = input("Which trainer would you like to select to teach the class? ")
    open_slots = db.query(f"SELECT timeslot_id, date, start_time, length FROM Free_Timeslots WHERE trainer_id = {trainer_id}")
    for open_slot in open_slots:
        date_str = open_slot[1].strftime("%Y-%m-%d")
        time_str = open_slot[2].strftime("%H:%M:%S")
        print(f'{open_slot[0]}. {date_str} at {time_str} for {open_slot[3]} minutes.')
    slot_chosen = input("Which slot would you like to select?" )
    slot_info = db.query(f"SELECT start_time, length, date FROM Free_Timeslots WHERE timeslot_id = {slot_chosen}")
    start_time, length, date = slot_info[0][0], slot_info[0][1], slot_info[0][2]
    db.query(f"DELETE FROM Free_Timeslots WHERE timeslot_id = {slot_chosen}")
    db.query(f"INSERT INTO Classes (trainer_id, start_time, length, date) VALUES ({trainer_id}, '{start_time}', {length}, '{date}');")

def staffInterface(staff_id, name):
    print(f"Welcome, {name}!")
    while True:
        print("0. View equipment.")
        print("1. View equipment maintenance history.")
        print("2. Create a class.")
        print("3. View fees.")
        print("4. View unpaid fees")
        print("5. Have maintenance done")
        print("6. View Attendance")
        print("7. Go Back.")
        selection = int(input("Please input what you would like to do today: "))
        if selection == 0:
            fetch = db.query(f"SELECT * FROM Equipment")
            for machine in fetch:
                date_str = machine[3].strftime("%Y-%m-%d")
                print(f'Machine {machine[0]}. Name: {machine[1]}. Status: {machine[2]}. Last maintained: {date_str}')
        if selection == 1:
            fetch = db.query(f"SELECT * FROM Equipment_Maintenance")
            for log in fetch:
                date_str = log[3].strftime("%Y-%m-%d")
                print(f'Machine ID: {log[2]}. Maintenance Supervisor: {log[1]}. Maintenance Date: {date_str}. Status: {log[4]}')
        if selection == 2:
            classCreationInterface()
        if selection == 3:
            fees = db.query(f"SELECT * FROM Fees")
            for fee in fees:
                print(f"Member {fee[1]}. {fee[2]}: {float(fee[3])}, {fee[4]}")
            print()
        if selection == 4:
            fees = db.query(f"SELECT * FROM Fees WHERE status = 'Pending'")
            for fee in fees:
                print(f"Member {fee[1]}. {fee[2]}: {float(fee[3])}, {fee[4]}")
            print()
        if selection == 5:
            machine_id = input("Which machine would you like maintained?")
            db.query(f"UPDATE Equipment SET status = 'Under Maintenance' WHERE equipment_id = {machine_id}")
            db.query(f"INSERT INTO Equipment_Maintenance (staff_id, equipment_id, maintenance_date, status) VALUES ({staff_id}, {machine_id}, CURRENT_DATE, 'Under Maintenance')")
        if selection == 6:
            classes = db.query("SELECT c.class_id, c.start_time, date, c.length, t.booking_price, c.trainer_id FROM Classes c JOIN Trainers t ON c.trainer_id = t.trainer_id")
            print("Classes:")
            for class_info in classes:
                date_str = class_info[2].strftime("%Y-%m-%d")
                time_str = class_info[1].strftime("%H:%M:%S")
                print(f'{class_info[0]}. {date_str} at {time_str} for {class_info[3]} minutes for {class_info[4]} dollars.')
            class_id = input("Which class would you like to check enrollment for?")
            enrollment = db.query(f"SELECT M.first_name, M.last_name FROM Class_Members CM JOIN Members M ON CM.member_id = M.member_id WHERE CM.class_id = {class_id};")
            for student in enrollment:
                print(f"{student[0]} {student[1]}")
            if enrollment == []:
                print("No students :c")
        if selection == 7:
            print("Exiting interface.")
            break
