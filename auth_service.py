import json

# In-memory storage for simplicity
user_profiles = {}
workouts = {}
help_details = {
    '1': "Input/Update User Profile: Enter your unique user ID, height in centimeters,/"
         " and weight in kilograms to save or update your profile.",
    '2': "Create New Workout (With Date): This option is more detailed but potentially slower!/"
         "Log the details of your workout including the date (YYYY-MM-DD),/"
         " exercises, sets, reps, and weight used.",
    '3': "Create Simple Workout (Sequential Number): This option is faster but less detailed!/"
         "Add workout details without specifying a date./"
         " Each workout is given a sequential number automatically.",
    '4': "View Previous Workouts: See a list of all your recorded workouts./"
         " Select a workout to view its detailed information.",
    '5': "Edit a Workout: Modify the details of a previously logged workout by selecting it from your list of workouts.",
    '6': "Delete a Workout: Remove a previously logged workout from your records by/"
         " selecting it from your list of workouts.",
    '7': "Help - Features: Provides information on how to use each feature of the application.",
    '8': "Exit: Close the application."
}


import json


def load_data():
    try:
        with open('user_profiles.txt', 'r') as f:
            global user_profiles
            user_profiles = json.load(f)
    except FileNotFoundError:
        user_profiles = {}

    try:
        with open('workouts.txt', 'r') as f:
            global workouts
            workouts = json.load(f)
    except FileNotFoundError:
        workouts = {}


def save_data_to_file(data, file_name):
    with open(file_name, 'w') as f:
        json.dump(data, f, indent=4)


def confirm_action(prompt="Confirm action (yes/no): "):
    while True:
        confirm = input(prompt).lower()
        if confirm in ['yes', 'y']:
            return True
        elif confirm in ['no', 'n']:
            return False
        else:
            print("Invalid input. Please enter 'yes' or 'no'.")


def save_user_profile():
    while True:  # Outer loop for the entire profile saving process
        user_id = input("Enter your user ID: ")
        height = input("Enter your height (cm): ")
        weight = input("Enter your weight (kg): ")
        if confirm_action("Do you want to save this profile? (yes/no): "):
            user_profiles[user_id] = {'height': height, 'weight': weight}
            print("Profile saved.")
            save_data_to_file(user_profiles, 'user_profiles.txt')
            break  # Correctly breaks out of the outer while loop
        else:
            if not confirm_action("Do you want to retry? (yes/no): "):
                break  # Correctly breaks out of the outer while loop


def create_workout():
    user_id = input("Enter your user ID: ")
    if user_id not in workouts:
        workouts[user_id] = []  # Initialize with an empty list if user ID doesn't exist

    date = input("Enter the date of your workout (YYYY-MM-DD): ")
    print("Enter workout details (Exercise - Sets - Reps - Weight) or type 'done' to finish:")

    workout_details = []
    while True:
        detail = input()
        if detail.lower() == 'done':  # Check if the user is done entering workout details
            break
        workout_details.append(detail)

    # Combining all workout details into a single string for storage
    combined_details = '; '.join(workout_details)
    if confirm_action("Do you want to save this workout? (yes/no): "):
        # Properly adding the workout to the user's list of workouts
        workouts[user_id].append({'date': date, 'details': combined_details})
        print("Workout created.")
        save_data_to_file(workouts, 'workouts.txt')
    else:
        if not confirm_action("Do you want to retry? (yes/no): "):
            return  # Exit the function if the user does not want to retry


def list_workouts():
    user_id = input("Enter your user ID to see your workouts: ")
    # Check if the user_id exists in the workouts dictionary
    if user_id not in workouts or not workouts[user_id]:
        print("No workouts found.")
        return

    user_workouts = workouts[user_id]  # Access the list of workouts for the user

    print("\nYour workouts:")
    for i, workout in enumerate(user_workouts, start=1):
        # Check if it's a workout with a date or a sequential workout and display accordingly
        if 'date' in workout:
            print(f"{i}. Workout on {workout['date']}: {workout['details']}")
        else:
            print(f"{i}. Workout #{workout['workout_number']}: {workout['details']}")

    while True:
        detail_choice = input("\nEnter the number of the workout to see details or 'back' to return to the main menu: ")
        if detail_choice.lower() == 'back':
            break
        try:
            choice_index = int(detail_choice) - 1
            if 0 <= choice_index < len(user_workouts):
                selected_workout = user_workouts[choice_index]
                print("\nWorkout Details:")
                print(json.dumps(selected_workout, indent=2))
            else:
                print("Invalid selection. Please enter a number from the list.")
        except ValueError:
            print("Please enter a valid number or 'back'.")


def edit_workout():
    user_id = input("Enter your user ID: ")
    # Check if the user ID exists in the workouts dictionary and has workouts
    if user_id in workouts and workouts[user_id]:
        user_workouts = workouts[user_id]  # Directly access the list of workouts for the user

        print("\nYour workouts:")
        for i, workout in enumerate(user_workouts, start=1):
            # Display workout details, handling both date-based and sequential workouts
            workout_identifier = workout.get('date', f"#{workout.get('workout_number', 'N/A')}")
            print(f"{i}. Workout {workout_identifier}: {workout['details']}")

        while True:
            edit_choice = input("\nEnter the number of the workout to edit or 'back' to return to the main menu: ")
            if edit_choice.lower() == 'back':
                break
            try:
                choice_index = int(edit_choice) - 1
                if 0 <= choice_index < len(user_workouts):
                    print("Enter new workout details (Exercise - Sets - Reps - Weight) or type 'done' to finish:")
                    workout_details = []
                    while True:
                        detail = input()
                        if detail.lower() == 'done':
                            break
                        workout_details.append(detail)

                    combined_details = '; '.join(workout_details)
                    if confirm_action("Do you want to save these changes? (yes/no): "):
                        user_workouts[choice_index]['details'] = combined_details
                        print("Workout updated.")
                        save_data_to_file(workouts, 'workouts.txt')
                        break
                    else:
                        if not confirm_action("Do you want to retry editing? (yes/no): "):
                            break
                else:
                    print("Invalid selection. Please enter a number from the list.")
            except ValueError:
                print("Please enter a valid number or 'back'.")
    else:
        print("No workouts found or user ID not found.")


def create_simple_workout():
    user_id = input("Enter your user ID: ")
    if user_id not in workouts:
        workouts[user_id] = []  # Initialize with an empty list if user ID doesn't exist

    print("Enter workout details (Exercise - Sets - Reps - Weight) or type 'done' to finish:")
    workout_details = []
    while True:
        detail = input()
        if detail.lower() == 'done':
            break
        workout_details.append(detail)

    combined_details = '; '.join(workout_details)
    workout_number = len(workouts[user_id]) + 1  # Sequential number for the workout

    if confirm_action("Do you want to save this workout? (yes/no): "):
        workouts[user_id].append({'workout_number': workout_number, 'details': combined_details})
        print(f"Workout #{workout_number} created.")
        save_data_to_file(workouts, 'workouts.txt')


def delete_workout():
    user_id = input("Enter your user ID: ")
    # Check if the user ID exists in the workouts dictionary and has workouts
    if user_id in workouts and workouts[user_id]:
        user_workouts = workouts[user_id]  # Directly access the list of workouts for the user

        print("\nYour workouts:")
        for i, workout in enumerate(user_workouts, start=1):
            # Display workout details, handling both date-based and sequential workouts
            workout_identifier = workout.get('date', f"Workout #{workout.get('workout_number', 'N/A')}")
            print(f"{i}. {workout_identifier}: {workout['details']}")

        while True:
            delete_choice = input("\nEnter the number of the workout to delete or 'back' to return to the main menu: ")
            if delete_choice.lower() == 'back':
                break
            try:
                choice_index = int(delete_choice) - 1
                if 0 <= choice_index < len(user_workouts):
                    if confirm_action("Are you sure you want to delete this workout? (yes/no): "):
                        # Remove the selected workout from the list
                        deleted_workout = user_workouts.pop(choice_index)
                        print(f"Workout deleted: {deleted_workout.get('date', deleted_workout.get('workout_number', 'N/A'))}")
                        save_data_to_file(workouts, 'workouts.txt')
                        break
                    else:
                        print("Workout not deleted.")
                        break
                else:
                    print("Invalid selection. Please enter a number from the list.")
            except ValueError:
                print("Please enter a valid number or 'back'.")
    else:
        print("No workouts found or user ID not found.")


def help_menu():
    print("\nHelp - Features Overview")
    print("1. Input/Update User Profile")
    print("2. Create New Workout (With Date)")
    print("3. Create Simple Workout (Sequential Number)")
    print("4. View Previous Workouts")
    print("5. Edit a Workout")
    print("6. Delete a Workout")
    print("7. Help - Features")
    print("8. Exit")
    print("9. View all information")
    print("\nEnter the number for more details, '9' to view all, or 'back' to return to the main menu.")

    while True:
        choice = input("Your choice: ").lower()
        if choice == 'back':
            break
        elif choice in help_details:
            print(f"\n{help_details[choice]}")
        elif choice == '9':
            for key, value in help_details.items():
                print(f"\n{value}")
        else:
            print("Invalid choice. Please enter a valid number, '9' to view all, or 'back' to return.")


def main_menu():
    load_data()
    while True:
        print("\nWorkout Logger Main Menu")
        print("1. Input/Update User Profile")
        print("2. Create New Workout (With Date) *Recommended for detailed entries")
        print("3. Create Simple Workout (Sequential Number) *Recommended for beginners for fast entry")
        print("4. View Previous Workouts")
        print("5. Edit a Workout")
        print("6. Delete a Workout *New feature for fast deletion")  # New option for deleting workouts
        print("7. Help - Features")
        print("8. Exit")
        choice = input("Enter your choice on keyboard: ")

        if choice == '1':
            save_user_profile()
        elif choice == '2':
            create_workout()
        elif choice == '3':
            create_simple_workout()
        elif choice == '4':
            list_workouts()
        elif choice == '5':
            edit_workout()
        elif choice == '6':  # Handle the choice for deleting a workout
            delete_workout()
        elif choice == '7':
            help_menu()
        elif choice == '8':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please choose again.")


if __name__ == "__main__":
    main_menu()