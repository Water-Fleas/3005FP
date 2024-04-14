import interfaces
import database as db

selection = ""

print("Welcome to the Fitness Database Interface. Enter exit to exit.")
while selection == "" or selection.lower()[0] != "e":
    selection = input("Please enter Member, Staff, or Trainer based on the interface you'd like to access or Exit: ")[0]
    if selection.lower()[0] == 'm':
        member_id = input("Please enter your member id, or input Register to create an account. ")
        if member_id.lower()[0] == 'r':
            member_id = interfaces.registrationInterface()
        fetch = db.query(f"SELECT * FROM Members WHERE member_id = {member_id}")
        if fetch == []:
            print("No member with that ID.")
        else:
            interfaces.memberInterface(member_id, fetch[0][1])
    if selection.lower()[0] == 't':
        trainer_id = input("Please enter your trainer id: ")
        fetch = db.query(f"SELECT * FROM Trainers WHERE trainer_id = {trainer_id}")
        if fetch == []:
            print("No trainer with that ID.")
        else:
            interfaces.trainerInterface(trainer_id, fetch[0][1])
    if selection.lower()[0] == 's':
        staff_id = input("Please enter your staff id: ")
        fetch = db.query(f"SELECT * FROM Staff WHERE staff_id = {staff_id}")
        if fetch == []:
            print("No staff with that ID.")
        else:
            interfaces.staffInterface(staff_id, fetch[0][1])
        