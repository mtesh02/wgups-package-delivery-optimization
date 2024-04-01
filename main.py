
#Copyright(c))2023, Munywoki D. Kiteme < munywoki1735 at gmail dot com >
#All rights reserved.

import datetime
from csv_reader import get_hash_map
from packages import total_distance

class WGUPSGUI:
    def __init__(self):
        self.user_options = [
            "Get info for all packages at a particular time",
            "Get info for a single package at a particular time",
            "View total mileage traveled by all trucks"
        ]

        self.option_index = None

        while True:
            # Display available options and get user choice
            self.print_options()
            self.option_index = self.get_option_index()

            # Perform actions based on user's selected option
            if self.option_index == 0:
                self.show_time_input()
            elif self.option_index == 1:
                self.show_package_id_input()
            elif self.option_index == 2:
                self.show_entire_hash_table()
            else:
                print("Invalid option. Please choose a valid option.")

    def print_options(self):
        print("Welcome to WGUPS Routing Program!\n")
        # Display the available user options with indexed numbers
        for index, option in enumerate(self.user_options):
            print(f"{index + 1}. {option}")

    def get_option_index(self):
        try:
            # Get the user's option choice and convert it to an index
            return int(input("\nPlease select an option: ")) - 1
        except ValueError:
            return -1

    def show_time_input(self):
        input_time = input("Enter a time (HH:MM:SS): ")
        self.show_all_packages(input_time)

    def show_package_id_input(self):
        # Get user input for a package ID and show information for that package
        package_id = input("Enter a valid package ID: ")
        self.show_single_package(package_id)

    def show_entire_hash_table(self):
            hash_map = get_hash_map()
            print("Contents of the Hash Table:")
            for index, bucket in enumerate(hash_map.map):
                if bucket:
                    print(f"Bucket {index}:")
                    for key, value in bucket:
                        print(f"  Key: {key}")
                        print(f"  Value: {value}")
                    print("-" * 20)

    def show_total_mileage(self):
        # Call the total_distance function to get mileage for each truck
        total_mileage_1, total_mileage_2, total_mileage_3 = total_distance()

        # Display mileage for each truck
        print(f"Total distance traveled by Truck 1: {total_mileage_1:.2f} miles")
        print(f"Total distance traveled by Truck 2: {total_mileage_2:.2f} miles")
        print(f"Total distance traveled by Truck 3: {total_mileage_3:.2f} miles")


    def show_all_packages(self, input_time):
        try:
            convert_user_time = datetime.datetime.strptime(input_time, "%H:%M:%S").time()

            packages_info = "Package Information at {}: \n".format(input_time)
            for count in range(1, 41):
                package = get_hash_map().get_value(str(count))
                if package:
                    self.update_package_status(package, convert_user_time)
                    package_info = {
                        'Package ID': package[0],
                        'Street Address': package[2],
                        'Delivery Deadline': package[6],
                        'State': package[4],
                        'City': package[3],
                        'Zip Code': package[5],
                        'Weight': package[7],
                        'Delivery Status': package[10]
                    }

                    if package[10].startswith('Delivered') and len(package[10].split(' ')) > 2:
                        package_info['Delivery Time'] = package[10].split(' ')[2]
                    elif package[6] != 'EOD':
                        delivery_deadline = datetime.datetime.strptime(package[6], "%I:%M %p").time()
                        if convert_user_time > delivery_deadline:
                            package_info['Delivery Status'] = 'Delivered'
                        else:
                            package_info['Delivery Status'] = 'En-route'

                    package_info_text = "\n".join([f"{key}: {value}" for key, value in package_info.items()])
                    packages_info += package_info_text + "\n\n"

            print(packages_info)
        except ValueError:
            print("Invalid time format. Please use HH:MM:SS.")

    def show_single_package(self, package_id):
        # Show information for a single package based on the provided package ID
        package = get_hash_map().get_value(package_id)
        if package:
            self.update_package_status(package)
            package_info = {
                'Package ID': package[0],
                'Street Address': package[2],
                'Delivery Deadline': package[6],
                'State': package[4],
                'City': package[3],
                'Zip Code': package[5],
                'Weight': package[7],
                'Delivery Status': package[10]
            }

            if package[10].startswith('Delivered'):
                if len(package[10].split(' ')) > 2:
                    package_info['Delivery Time'] = package[10].split(' ')[2]

            # Format package information into a readable text
            package_info_text = "\n".join([f"{key}: {value}" for key, value in package_info.items()])
            print(package_info_text)
        else:
            print(f"Package ID {package_id} not found.")

    def update_package_status(self, package, input_time=None):
        current_time = datetime.datetime.now().time() if input_time is None else input_time

        if package[6] != 'EOD':
            try:
                delivery_deadline = datetime.datetime.strptime(package[6], "%I:%M %p").time()

                if current_time >= delivery_deadline:
                    package[10] = "Delivered"
                else:
                    if package[1] == "1" and current_time < datetime.time(8, 0, 0):
                        package[10] = "At Hub"
                    elif package[1] == "2" and current_time < datetime.time(9, 10, 0):
                        package[10] = "At Hub"
                    elif package[1] == "3" and current_time < datetime.time(11, 0, 0):
                        package[10] = "At Hub"
                    else:
                        package[10] = "En-route"
            except ValueError:
                # Handle the case when delivery deadline is 'EOD' or has an invalid format
                package[10] = "En-route"
        else:
            package[10] = "Delivered"

if __name__ == "__main__":
    # Instantiate the WGUPSGUI class to start the program
    gui = WGUPSGUI()
