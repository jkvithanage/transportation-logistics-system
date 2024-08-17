import re
import datetime

class Menu:
    def __init__(self, title, options= []):
        self.title = title
        self.options = options

    def add_menu_item(self, key, label):
        self.options.append([key, label])

    # display the menu and returns user's choice
    def display(self):
        if not len(self.options) > 0:
            print('Error: Menu has no options to display!')
            return None

        print()
        print('--|', self.title, '|--')
        print()
        print('Please select an option:')

        for option in self.options:
            print('\t' + str(option[0]) + '. ' + option[1])

        return self.__get_valid_choice()

    # private method to get a valid choice from the user
    def __get_valid_choice(self):
        print()

        option_keys = []
        for option in self.options:
            option_keys.append(option[0])

        while True:
            try:
                choice = int(input('Enter your choice: '))

                if choice in option_keys:
                    return choice
                else:
                    print('Invalid choice, please choose an option from the menu.')
            except ValueError:
                print('Invalid input, please valid number.')


class Table:
    def __init__(self, headers, items):
        self.headers = headers
        self.items = items

    def display(self):
        # determine the maximum width for each column
        column_widths = []
        # take header lenghts as initial column widths
        for header in self.headers:
            column_widths.append(len(header))

        # iterate through each row
        for item in self.items:
            i = 0
            while i < len(item):
                element_length = len(str(item[i]))
                # if cell length of a cell value is geater than the initial column width,
                # assign it as the column width
                if element_length > column_widths[i]:
                    column_widths[i] = element_length
                i += 1

        # build the header row
        header_row = "|"
        i = 0
        while i < len(self.headers):
            header_row += " " + self.headers[i].ljust(column_widths[i]) + " |"
            i += 1

        print("-" * (sum(column_widths) + len(self.headers) * 3 + 1)) # header top line
        print(header_row)
        print("-" * (sum(column_widths) + len(self.headers) * 3 + 1)) # header bottom line

        # print the rows
        for item in self.items:
            row = "|"
            i = 0
            while i < len(item):
                row += " " + str(item[i]).ljust(column_widths[i]) + " |"
                i += 1
            print(row)

        print("-" * (sum(column_widths) + len(self.headers) * 3 + 1)) # table bottom line

class Model:
    # https://pynative.com/python-class-variables/
    # subclasses should override the following class variables
    # to maintain their own state
    _instances = [] # protected list to store all instances (vehicles, customers, shipments, etc)
    _id_regex = '' # regex for id validation
    _id_pattern = '' # the pattern of a valid id

    def __init__(self, object_id=None):
        self._object_id = object_id

    def get_id(self):
        return self._object_id

    def set_id(self, value):
        if not self.__is_unique_id(value):
            raise ValueError("\nDuplicate ID. Please enter a unique ID.")

        if not self.__is_valid_id(value):
            raise ValueError("\nInvalid ID. Please follow the pattern: " + self._id_pattern)

        self._object_id = value
        self.last_id = self._object_id

    # other public methods

    # https://realpython.com/instance-class-and-static-methods-demystified/
    # https://www.geeksforgeeks.org/decorators-in-python/
    @classmethod
    def get_all(cls):
        return cls._instances

    @classmethod
    def count(cls):
        return len(cls._instances)

    # A single method running all validations.
    # This is to prevent saving invalid instances
    # that are initialized with invalid attribute values.
    def validate(self):
        if not self.__is_unique_id(self._object_id):
            raise ValueError("Duplicate ID. Please enter a unique ID.")

        if not self.__is_valid_id(self._object_id):
            raise ValueError("Invalid ID. Please follow the pattern: Vxxx.")

    # the only method to save an instance to the _instances list
    def save(self):
        self.validate() # run all validation before saving
        self._instances.append(self)

        return True

    # the only method to remove an instance from the _instance list
    def remove(self):
        self._instances.remove(self)

    @classmethod
    def find_by_id(cls, object_id):
        for instance in cls._instances:
            if instance.get_id() == object_id:
                return instance

        return None

    # private methods

    def __is_unique_id(self, object_id):
        for instance in self._instances:
            if instance.get_id() == object_id:
               return False
        return True

    def __is_valid_id(self, object_id):
        match = re.search(self._id_regex, object_id)

        if match:
            return True
        else:
            return False

class Vehicle(Model):
    # overriding the class variables in the super class
    _instances = []
    _id_regex = '^V[0-9]{3,}$'
    _id_pattern = 'Vxxx'

    def __init__(self, vehicle_id=None, vehicle_type=None, capacity=None):
        # call super class constructor
        super().__init__(vehicle_id)
        # call superclass id setter
        # self.set_id(vehicle_id)
        self._object_id = vehicle_id
        self._vehicle_type = vehicle_type
        self._capacity = capacity

    # getters and setters

    def get_vehicle_type(self):
        return self._vehicle_type

    def set_vehicle_type(self, value):
        if not self.__is_valid_vehicle_type(value):
            raise ValueError("\nInvalid vehicle type. It can be only Truck, Van or Car.")

        self._vehicle_type = value

    def get_capacity(self):
        return self._capacity

    def set_capacity(self, value):
        if not self.__is_valid_capacity(value):
            raise ValueError("\nInvalid capacity. Please enter a positive integer.")

        self._capacity = value

    # other public methods

    # overriding validate method from the super class
    def validate(self):
        super().validate()

        if not self.__is_valid_vehicle_type(self._vehicle_type):
            raise ValueError("\nInvalid vehicle type. It can be only Truck, Van or Car.")

        if not self.__is_valid_capacity(self._capacity):
            raise ValueError("\nInvalid capacity. Please enter a positive integer.")

    # private methods

    def __is_valid_vehicle_type(self, vehicle_type):
        match = re.search('^(Car|Van|Truck)$', vehicle_type)

        if match:
            return True
        else:
            return False

    def __is_valid_capacity(self, capacity):
        return capacity.isdigit() and int(capacity) > 0

class Controller:
    def menu(self):
        raise NotImplementedError()

    # protected methods

    # https://www.geeksforgeeks.org/higher-order-functions-in-python/
    def _get_valid_input(self, prompt, setter):
        print()
        while True:
            user_input = input(prompt)

            try:
                setter(user_input)
                break
            except ValueError as e:
                print(e)

class VehiclesController(Controller):
    def menu(self):
        menu = Menu('Fleet Management', [[1, 'Add a vehicle'],
                                        [2, 'Update vehicle information'],
                                        [3, 'Remove a vehicle'],
                                        [4, 'View all vehicles'],
                                        [0, 'Quit fleet management']])

        while True:
            choice = menu.display()

            print()
            if choice == 1:
                # add a vehicle
                self.add_vehicle()
            elif choice == 2:
                # update vehicle
                self.update_vehicle()
            elif choice == 3:
                # remove a vehicle
                self.remove_vehicle()
            elif choice == 4:
                # view all vehicles
                self.view_all_vehicles()
            elif choice == 0:
                # quit fleet management
                print('Quitting fleet management...')
                break

    def add_vehicle(self):
        print('--| Add a Vehicle |--')
        print()

        vehicle = Vehicle()

        next_id = 'V00' + str(Vehicle.count() + 1)
        print('Suggested vehicle ID:', next_id)
        self._get_valid_input('Enter vehicle ID: ', vehicle.set_id)
        self._get_valid_input('Enter vehicle type: ', vehicle.set_vehicle_type)
        self._get_valid_input('Enter vehicle capacity: ', vehicle.set_capacity)

        print()
        try:
            vehicle.save()
            print('Vehicle', vehicle.get_id(), 'added successfully.')
        except ValueError as e:
            print(e)

    def update_vehicle(self):
        print('--| Update Vehicle Information |--')
        print()

        vehicle_id = input('Enter vehicle ID: ')
        vehicle = Vehicle.find_by_id(vehicle_id)

        if vehicle:
            # vehicle exists
            self._get_valid_input('Enter vehicle type: ', vehicle.set_vehicle_type)
            self._get_valid_input('Enter vehicle capacity: ', vehicle.set_capacity)

            print()
            print('Vehicle', vehicle_id, 'updated successfully.')
        else:
            print()
            print('Sorry, cannot find a vehicle with ID:', vehicle_id)

    def remove_vehicle(self):
        print('--| Remove a Vehicle |--')
        print()

        vehicle_id = input('Enter vehicle ID: ')
        vehicle = Vehicle.find_by_id(vehicle_id)

        if vehicle:
            # vehicle exists
            confirmation = input('Are you sure you want to remove vehicle ' + vehicle_id + '? (y/n): ')

            if confirmation.lower() in ['y', 'yes']:
                vehicle.remove()
                print('Vehicle with ID', vehicle_id, 'removed successfully.')
            else:
                print('Vehicle with ID', vehicle_id, 'was not removed.')
        else:
            print('Sorry, cannot find a vehicle with ID:', vehicle_id)

    def view_all_vehicles(self):
        print('--| View all Vehicles |--')
        print()

        vehicles = Vehicle.get_all()

        vehicle_data = []
        for vehicle in vehicles:
            vehicle_data.append([vehicle.get_id(), vehicle.get_vehicle_type(), vehicle.get_capacity()])

        if len(vehicle_data) > 0:
            table = Table(['Vehicle ID', 'Type', 'Capacity'], vehicle_data)
            table.display()
        else:
            print('No vehicles to display.')

        print()
        prompt = ''
        while not prompt == 'exit':
            prompt = input("Enter 'exit' to go back: ")

class Customer(Model):
    # overriding the class variables in the super class
    _instances = []
    _id_regex = '^C[0-9]{3,}$'
    _id_pattern = 'Cxxx'

    def __init__(self, customer_id=None, name=None, dob=None, address=None, phone=None, email=None):
        # call super class constructor
        super().__init__(customer_id)
        self._object_id = customer_id
        self._name = name
        self._dob = dob
        self._address = address
        self._phone = phone
        self._email = email

    # getters and setters

    def get_name(self):
        return self._name

    def set_name(self, value):
        if not value:
            raise ValueError("Customer name cannot be empty.")

        self._name = value

    def get_dob(self):
        return self._dob

    def set_dob(self, value):
        if not self.__is_valid_dob(value):
            raise ValueError('\nInvalid date of birth. Please enter DD/MM/YYYY')

        if not self.__is_valid_age(value):
            raise ValueError('\nAge must be 18 or above.')

        self._dob = value

    def get_address(self):
        return self._address

    def set_address(self, value):
        if not self.__is_valid_address(value):
            raise ValueError('\nInvalid address. Please enter a valid Australian address.')

        self._address = value

    def get_phone(self):
        return self._phone

    def set_phone(self, value):
        if not self.__is_valid_phone(value):
            raise ValueError('\nInvalid phone number. Please enter a valid Australian phone number.')

        self._phone = value

    def get_email(self):
        return self._email

    def set_email(self, value):
        if not self.__is_valid_email(value):
            raise ValueError('\nInvalid email address. Please enter a valid email.')

        self._email = value

    # other public methods

    def validate(self):
        super().validate()

        if not self._name:
            raise ValueError("Customer name cannot be empty.")

        if not self.__is_valid_dob(self._dob):
            raise ValueError('\nInvalid date of birth. Please enter DD/MM/YYYY')

        if not self.__is_valid_age(self._dob):
            raise ValueError('\nAge must be 18 or above.')

        if not self.__is_valid_address(self._address):
            raise ValueError('\nInvalid address. Please enter a valid Australian address.')

        if not self.__is_valid_phone(self._phone):
            raise ValueError('\nInvalid phone number. Please enter a valid Australian phone number.')

        if not self.__is_valid_email(self._email):
            raise ValueError('\nInvalid email address. Please enter a valid email.')

    # returns a list of shipments belong to the customer
    def get_shipments(self):
        shipments = []
        for shipment in Shipment.get_all():
            if shipment.get_customer_id() == self.get_id():
                shipments.append(shipment)

        return shipments

    # private methods

    # =============================================================================
    # dd/mm/yyyy
    # 06/09/1995
    # 31/10/1995
    # 35/10/1995 - not matching day
    # 31/15/1995 - not matching month
    # 10/10/2500 - not matching year
    # 10/10/1800 - not matching year
    # =============================================================================
    def __is_valid_dob(self, dob):
        match = re.search('^(0[1-9]|[12][0-9]|3[01])/(0[1-9]|1[0-2])/(19|20)[0-9]{2}$', dob)

        if match:
            return True
        else:
            return False

    def __is_valid_age(self, dob):
        today = datetime.date.today()
        birth_year = int(dob[-4:])

        age = today.year - birth_year

        return age >= 18

    # =============================================================================
    # 123 Main St, Sydney, NSW 2000, Australia
    # 6/149 Princes Hwy, Dandenong, VIC 3175, Australia
    # 6/149A Princes Hwy, Dandenong, VIC 3175, Australia
    # Unit 6 149 Princes Hwy, Dandenong, VIC 3175, Australia
    # 8A Park Rd, Cheltenham VIC 3192, Australia
    # 4 Anfield Cres, Mulgrave VIC 3170, Australia
    # 4 Anfield Cres, Mulgrave, VIC 3170, Australia
    # =============================================================================
    def __is_valid_address(self, address):
        match = re.search('^([\d\/\w\s]+)\s([a-zA-Z\s]+)\,\s([a-zA-Z\s]+)\,?\s(ACT|NSW|VIC|SA|WA|NT|TAS)\s([0-9]{4})\,\s(Australia)$', address)

        if match:
            return True
        else:
            return False

    # =============================================================================
    # 04xxxxxxxx or 04xx xxx xxx
    # =============================================================================
    def __is_valid_phone(self, phone):
        match = re.search('^(04\d{2})\s?\d{3}\s?\d{3}$', phone)

        if match:
            return True
        else:
            return False

    # =============================================================================
    # john@example.com
    # john.doe@gmail.com
    # john_doe@gmail.com
    # john.doe@gmail.com.au
    # john1234@gmail.com.au
    # 123john@gmail.com
    # john@example - invalid
    # john@example_com - invalid
    # =============================================================================
    def __is_valid_email(self, email):
        match = re.search('^([\w\-_.]*[^.])(@\w+)(\.\w+(\.\w+)?)$', email)

        if match:
            return True
        else:
            return False

class CustomersController(Controller):
    def menu(self):
        menu = Menu('Customer Management',[[1, 'Add a customer'],
                                           [2, 'Update customer information'],
                                           [3, 'Remove a customer'],
                                           [4, 'View all customers'],
                                           [5, "View a customer's shipments"],
                                           [0, 'Quit customer management']])

        while True:
            choice = menu.display()

            print()
            if choice == 1:
                self.add_customer()
            elif choice == 2:
                self.update_customer()
            elif choice == 3:
                self.remove_customer()
            elif choice == 4:
                self.view_all_customers()
            elif choice == 5:
                self.view_shipments()
            elif choice == 0:
                print('Quitting customer management...')
                break

    def add_customer(self):
        print('--| Add a Customer |--')
        print()

        customer = Customer()

        next_id = 'C00' + str(Customer.count() + 1)
        print('Suggested customer ID:', next_id)
        self._get_valid_input('Enter customer ID: ', customer.set_id)

        self._get_valid_input('Enter customer name: ', customer.set_name)
        self._get_valid_input('Enter date of birth (DD/MM/YYYY): ', customer.set_dob)
        self._get_valid_input('Enter address (e.g: 123 Main St, Sydney, NSW 2000, Australia): ', customer.set_address)
        self._get_valid_input('Enter phone number: (e.g: 04xxxxxxxx)', customer.set_phone)
        self._get_valid_input('Enter email address (e.g: user@example.com): ', customer.set_email)

        try:
            customer.save()

            print()
            print('Customer', customer.get_id(), 'added successfully.')
        except ValueError as e:
            print(e)

    def update_customer(self):
        print('--| Update Customer Information |--')
        print()

        customer_id = input('Enter customer ID: ')
        customer = Customer.find_by_id(customer_id)

        if customer:
            # customer exists
            self._get_valid_input('Enter customer name: ', customer.set_name)
            self._get_valid_input('Enter date of birth (DD/MM/YYYY): ', customer.set_dob)
            self._get_valid_input('Enter address (e.g: 123 Main St, Sydney, NSW 2000, Australia): ', customer.set_address)
            self._get_valid_input('Enter phone number: (e.g: 04xxxxxxxx)', customer.set_phone)
            self._get_valid_input('Enter email address (e.g: user@example.com): ', customer.set_email)

            print()
            print('Customer', customer_id, 'updated successfully.')
        else:
            print()
            print('Sorry, cannot find a customer with ID:', customer_id)

    def remove_customer(self):
        print('--| Remove a Customer |--')
        print()

        customer_id = input('Enter customer ID: ')
        customer = Customer.find_by_id(customer_id)

        print()
        if customer:
            # customer exists
            confirmation = input('Are you sure you want to remove customer ' + customer_id + '? (y/n): ')

            print()
            if confirmation.lower() in ['y', 'yes']:
                customer.remove()
                print('Customer with ID', customer_id, 'removed successfully.')
            else:
                print('Customer with ID', customer_id, 'was not removed.')
        else:
            print('Sorry, cannot find a customer with ID:', customer_id)

    def view_all_customers(self):
        print('--| View all Customers |--')
        print()

        customers = Customer.get_all()

        customer_data = []
        for customer in customers:
            customer_data.append([customer.get_id(), customer.get_name(), customer.get_dob(), customer.get_address(), customer.get_phone(), customer.get_email()])

        if len(customer_data) > 0:
            table = Table(['Customer ID', 'Name', 'DOB', 'Address', 'Phone', 'Email'], customer_data)
            table.display()
        else:
            print('No customers to display.')

        print()
        prompt = ''
        while not prompt == 'exit':
            prompt = input("Enter 'exit' to go back: ")

    def view_shipments(self):
        print('--| View Shipments |--')
        print()

        customer_id = input('Enter customer ID: ')
        customer = Customer.find_by_id(customer_id)

        print()
        if customer:
            # customer exists
            shipments = customer.get_shipments()

            shipment_data = []
            for shipment in shipments:
                shipment_data.append([shipment.get_id(),
                                        shipment.get_origin(),
                                        shipment.get_destination(),
                                        shipment.get_weight(),
                                        shipment.get_vehicle_id(),
                                        shipment.get_status(),
                                        shipment.get_delivery_date()])

            table = Table(['Shipment ID', 'Origin', 'Destination', 'Weight', 'Vehicle ID', 'Status', 'Delivery Date'], shipment_data)
            table.display()

            print()
            prompt = ''
            while not prompt == 'exit':
                prompt = input("Enter 'exit' to go back: ")
        else:
            print('Sorry, cannot find a customer with ID:', customer_id)

class Shipment(Model):
    # overriding the class variables in the super class
    _instances = []
    _id_regex = '^S[0-9]{3,}$'
    _id_pattern = 'Sxxx'

    def __init__(self, shipment_id=None, origin=None, destination=None, weight=None, vehicle_id=None, customer_id=None):
        # call super class constructor
        super().__init__(shipment_id)
        self._object_id = shipment_id
        self._origin = origin
        self._destination = destination
        self._weight = weight
        self._vehicle_id = vehicle_id
        self._customer_id = customer_id
        self._status = 'In Transit'
        self._delivery_date = None

    # getters and setters

    def get_origin(self):
        return self._origin

    def set_origin(self, value):
        if not value:
            raise ValueError("Origin cannot be empty.")

        self._origin = value

    def get_destination(self):
        return self._destination

    def set_destination(self, value):
        if not value:
            raise ValueError("Destination cannot be empty.")

        self._destination = value

    def get_weight(self):
        return self._weight

    def set_weight(self, value):
        if not self.__is_valid_weight(value):
            raise ValueError("Weight must be a positive number.")

        self._weight = value

    def get_vehicle_id(self):
        return self._vehicle_id

    def set_vehicle_id(self, value):
        if not self.__is_valid_vehicle_id(value):
            raise ValueError("Invalid vehicle ID. Please select one from the vehicles list.")

        self._vehicle_id = value

    def get_customer_id(self):
        return self._customer_id

    def set_customer_id(self, value):
        if not self.__is_valid_customer_id(value):
            raise ValueError("Invalid customer ID. Please select one from the customers list.")

        self._customer_id = value

    def get_status(self):
        return self._status

    def get_delivery_date(self):
        if self._delivery_date:
            return self._delivery_date.strftime('%c')
        else:
            return 'N/A'

    # other public methods

    def mark_delivered(self):
        if self._status == 'Delivered':
            return False
        else:
            self._status = 'Delivered'
            self._delivery_date = datetime.datetime.now()
            return True

    def validate(self):
        super().validate()

        if not self._origin:
            raise ValueError("Origin cannot be empty.")

        if not self._destination:
            raise ValueError("Destination cannot be empty.")

        if not self.__is_valid_weight(self._weight):
            raise ValueError("Weight must be a positive number.")

        if not self.__is_valid_vehicle_id(self._vehicle_id):
            raise ValueError("Invalid vehicle ID. Please select one from the vehicles list.")

        if not self.__is_valid_customer_id(self._customer_id):
            raise ValueError("Invalid customer ID. Please select one from the customers list.")

    # private methods

    def __is_valid_weight(self, weight):
        return isinstance(weight, (int, float)) or weight > 0

    def __is_valid_vehicle_id(self, vehicle_id):
        vehicle = Vehicle.find_by_id(vehicle_id)

        if vehicle:
            return True
        else:
            return False

    def __is_valid_customer_id(self, customer_id):
        customer = Customer.find_by_id(customer_id)

        if customer:
            return True
        else:
            return False

class ShipmentsController(Controller):
    def menu(self):
        menu = Menu('Shipment Management',[[1, 'Create a new shipment'],
                                           [2, 'Track a shipment'],
                                           [3, 'View all shipments'],
                                           [0, 'Quit shipment management',]])

        while True:
            choice = menu.display()

            print()
            if choice == 1:
                self.create_shipment()
            elif choice == 2:
                self.track_shipment()
            elif choice == 3:
                self.view_all_shipments()
            elif choice == 0:
                print('Quitting customer management...')
                break

    def create_shipment(self):
        print('--| Create a Shipment |--')
        print()

        shipment = Shipment()

        next_id = 'S00' + str(Shipment.count() + 1)
        print('Suggested shipment ID:', next_id)
        self._get_valid_input('Enter shipment ID: ', shipment.set_id)

        self._get_valid_input('Enter origin location: ', shipment.set_origin)
        self._get_valid_input('Enter destination location: ', shipment.set_destination)
        self._get_valid_input('Enter weight: ', shipment.set_weight)

        vehicles = Vehicle.get_all()

        vehicle_data = []
        for vehicle in vehicles:
            vehicle_data.append([vehicle.get_id(), vehicle.get_vehicle_type(), vehicle.get_capacity()])

        if len(vehicle_data) > 0:
            table = Table(['Vehicle ID', 'Type', 'Capacity'], vehicle_data)
            table.display()
        else:
            print('No vehicles to display.')
        self._get_valid_input('Enter vehicle ID: ', shipment.set_vehicle_id)

        self._get_valid_input('Enter customer ID: ', shipment.set_customer_id)

        try:
            shipment.save()

            print()
            print('Shipment', shipment.get_id(), 'added successfully.')
        except ValueError as e:
            print(e)

    def track_shipment(self):
        print('--| Track a Shipment |--')
        print()

        shipment_id = input('Enter shipment ID: ')
        shipment = Shipment.find_by_id(shipment_id)

        print()
        if shipment:
            print('Status of the shipment', shipment_id, 'is:', shipment.get_status())
        else:
            print('Sorry, cannot find a shipment with ID:', shipment_id)

    def view_all_shipments(self):
        print('--| View all Shipments |--')
        print()

        shipments = Shipment.get_all()

        shipment_data = []
        for shipment in shipments:
            shipment_data.append([shipment.get_id(),
                                  shipment.get_origin(),
                                  shipment.get_destination(),
                                  shipment.get_weight(),
                                  shipment.get_vehicle_id(),
                                  shipment.get_customer_id(),
                                  shipment.get_status(),
                                  shipment.get_delivery_date()])

        table = Table(['Shipment ID', 'Origin', 'Destination', 'Weight', 'Vehicle', 'Customer', 'Status', 'Delivery Date'], shipment_data)
        table.display()

        print()
        prompt = ''
        while not prompt == 'exit':
            prompt = input("Enter 'exit' to go back: ")

class DeliveriesController(Controller):
    def menu(self):
        menu = Menu('Delivery Management',[[1, 'Mark shipment delivery'],
                                           [2, 'View delivery status for a shipment'],
                                           [0, 'Quit shipment management',]])

        while True:
            choice = menu.display()

            print()
            if choice == 1:
                self.mark_shipment_delivered()
            elif choice == 2:
                self.view_delivery_status()
            elif choice == 0:
                print('\nQuitting delivery management...')
                break

    def mark_shipment_delivered(self):
        print('--| Mark Shipment Delivery |--')
        print()

        shipment_id = input('Enter shipment ID: ')
        shipment = Shipment.find_by_id(shipment_id)

        print()
        if shipment:
            is_marked = shipment.mark_delivered()
            if is_marked:
                print('Shipment', shipment_id, 'has been marked as delivered.')
            else:
                print('Shipment with ID:', shipment_id, 'is already delivered.')
        else:
            print('Sorry, cannot find a shipment with ID:', shipment_id)

    def view_delivery_status(self):
        print('--| View Delivery Status |--')
        print()

        shipment_id = input('Enter shipment ID: ')
        shipment = Shipment.find_by_id(shipment_id)

        print()
        if shipment:
            if shipment.get_status() == 'Delivered':
                # referred https://strftime.org/ to find the mask
                print('Shipment', shipment_id, 'was delivered on', shipment.get_delivery_date())
            else:
                print('Shipment', shipment_id, 'is not delivered yet.')
        else:
            print('Sorry, cannot find a shipment with ID:', shipment_id)

class Main:
    def __init__(self):
        self.vehicles_controller = VehiclesController()
        self.customers_controller = CustomersController()
        self.shipments_controller = ShipmentsController()
        self.deliveries_controller = DeliveriesController()

    def menu(self):
        menu = Menu('Transportation Logistics System', [[1, 'Fleet Management'],
                                                        [2, 'Customer Management'],
                                                        [3, 'Shipment Management'],
                                                        [4, 'Delivery Management'],
                                                        [0, 'Quit']])

        while True:
            choice = menu.display()

            # else statement is not required
            # since the display() method only returns a valid choice
            if choice == 1:
                self.vehicles_controller.menu()
            elif choice == 2:
                self.customers_controller.menu()
            elif choice == 3:
                self.shipments_controller.menu()
            elif choice == 4:
                self.deliveries_controller.menu()
            elif choice == 0:
                print('Exiting the system. Goodbye!')
                break

main = Main()
main.menu()
