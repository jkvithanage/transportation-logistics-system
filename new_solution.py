import re
import datetime
import random

class Menu:
    def __init__(self, title, options= []):
        self.title = title
        self.options = options

    def add_menu_item(self, key, label):
        self.options.append([key, label])

    # display the menu and returns user's choice
    def display_menu(self):
        if not len(self.options) > 0:
            print('Error: Menu has no options to display!')
            return -1

        print('\n--|', self.title, '|--')
        print('Please select an option:')

        for option in self.options:
            print('\t' + str(option[0]) + '. ' + option[1])

        return input('Enter your choice: ')

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
    _instances = [] # protected list to store all instances (vehicles, customers, shipments)
    _id_regex = ''
    _id_pattern = ''

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
        if not value:
            raise ValueError("\nVehicle type cannot be empty.")

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

        if not self._vehicle_type:
            raise ValueError("\nVehicle type cannot be empty.")

        if not self.__is_valid_capacity(self._capacity):
            raise ValueError("\nVehicle type cannot be empty.")

    # private methods

    def __is_valid_capacity(self, capacity):
        return capacity.isdigit() and int(capacity) > 0

class VehiclesController:
    def fleets_menu(self):
        menu = Menu('Fleet Management',[[1, 'Add a vehicle'],
                                        [2, 'Update vehicle information'],
                                        [3, 'Remove a vehicle'],
                                        [4, 'View all vehicles'],
                                        [0, 'Quit fleet management']])
        choice = menu.display_menu()

        if choice == '1':
            # add a vehicle
            self.add_vehicle()
            self.fleets_menu()
        elif choice == '2':
            # update vehicle
           self.update_vehicle()
           self.fleets_menu()
        elif choice == '3':
            # remove a vehicle
            self.remove_vehicle()
            self.fleets_menu()
        elif choice == '4':
            # view all vehicles
            self.view_all_vehicles()
            self.fleets_menu()
        elif choice == '0':
            # quit fleet management
            print('\nQuitting fleet management...')
        else:
            print('\nInvalid choice, please try again.')
            self.fleets_menu()

    def add_vehicle(self):
        print('\n--| Add a Vehicle |--')

        vehicle = Vehicle()

        next_id = 'V00' + str(Vehicle.count() + 1)
        print('Suggested vehicle ID:', next_id)
        self.__get_valid_input('Enter vehicle ID: ', vehicle.set_id)
        self.__get_valid_input('Enter vehicle type: ', vehicle.set_vehicle_type)
        self.__get_valid_input('Enter vehicle capacity: ', vehicle.set_capacity)

        try:
            vehicle.save()
            print('\nVehicle', vehicle.get_id(), 'added successfully.')
        except ValueError as e:
            print(e)

    def update_vehicle(self):
        print('\n--| Update Vehicle Information |--')

        vehicle_id = input('Enter vehicle ID: ')
        vehicle = Vehicle.find_by_id(vehicle_id)

        if vehicle:
            # vehicle exists
            self.__get_valid_input('Enter vehicle type: ', vehicle.set_vehicle_type)
            self.__get_valid_input('Enter vehicle capacity: ', vehicle.set_capacity)
            print('\nVehicle', vehicle_id, 'updated successfully.')
        else:
            print('\nSorry, cannot find a vehicle with ID:', vehicle_id)

    def remove_vehicle(self):
        print('\n--| Remove a Vehicle |--')

        vehicle_id = input('\nEnter vehicle ID: ')
        vehicle = Vehicle.find_by_id(vehicle_id)

        if vehicle:
            # vehicle exists
            confirmation = input('\nAre you sure you want to remove vehicle ' + vehicle_id + '? (y/n): ')

            if confirmation.lower() in ['y', 'yes']:
                vehicle.remove()
                print('\nVehicle with ID', vehicle_id, 'removed successfully.')
            else:
                print('\nVehicle with ID', vehicle_id, 'was not removed.')
        else:
            print('\nSorry, cannot find a vehicle with ID:', vehicle_id)

    def view_all_vehicles(self):
        print('\n--| View all Vehicles |--')

        vehicles = Vehicle.get_all()

        vehicle_data = []
        for vehicle in vehicles:
            vehicle_data.append([vehicle.get_id(), vehicle.get_vehicle_type(), vehicle.get_capacity()])

        if len(vehicle_data) > 0:
            table = Table(['Vehicle ID', 'Type', 'Capacity'], vehicle_data)
            table.display()
        else:
            print('\nNo vehicles to display.')

        prompt = ''
        while not prompt == 'exit':
            prompt = input("\nEnter 'exit' to go back: ")

    # private methods

    # https://www.geeksforgeeks.org/higher-order-functions-in-python/
    def __get_valid_input(self, prompt, setter):
        valid_input = False
        while not valid_input:
            user_input = input(prompt)

            try:
                setter(user_input)
                valid_input = True
            except ValueError as e:
                print(e)

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

    def get_shipments(self):
        raise NotImplementedError()
        shipment_data = []
        for shipment in self._instances:
            if shipment.get_customer_id() == self.get_customer_id():
                shipment_data.append([])

        table = Table(['Shipment ID', 'Origin', 'Destination', 'Weight', 'Vehicle ID', 'Status', 'Delivery Date'], shipment_data)
        table.display()

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

class CustomersController:
    def customers_menu(self):
        menu = Menu('Customer Management',[[1, 'Add a customer'],
                                           [2, 'Update customer information'],
                                           [3, 'Remove a customer'],
                                           [4, 'View all customers'],
                                           [5, "View a customer's shipments"],
                                           [0, 'Quit customer management']])
        choice = menu.display_menu()

        if choice == '1':
            self.add_customer()
            self.customers_menu()
        elif choice == '2':
            self.update_customer()
            self.customers_menu()
        elif choice == '3':
            self.remove_customer()
            self.customers_menu()
        elif choice == '4':
            self.view_all_customers()
            self.customers_menu()
        elif choice == '5':
            self.view_shipments()
            self.customers_menu()
        elif choice == '0':
            print('\nQuitting customer management...')
        else:
            print('\nInvalid choice, please try again.')
            self.customers_menu()

    def add_customer(self):
        print('\n--| Add a Customer |--')

        customer = Customer()

        next_id = 'C00' + str(Customer.count() + 1)
        print('Suggested customer ID:', next_id)
        self.__get_valid_input('Enter customer ID: ', customer.set_id)
        self.__get_valid_input('Enter customer name: ', customer.set_name)
        self.__get_valid_input('Enter date of birth (DD/MM/YYYY): ', customer.set_dob)
        self.__get_valid_input('Enter address: ', customer.set_address)
        self.__get_valid_input('Enter phone number', customer.set_phone)
        self.__get_valid_input('Enter emai address: ', customer.set_email)

        try:
            customer.save()
            print('\nCustomer', customer.get_id(), 'added successfully.')
        except ValueError as e:
            print(e)

    def update_customer(self):
        print('\n--| Update Customer Information |--')

        customer_id = input('Enter customer ID: ')
        customer = Customer.find_by_id(customer_id)

        if customer:
            # customer exists
            self.__get_valid_input('Enter customer name: ', customer.set_name)
            self.__get_valid_input('Enter date of birth (DD/MM/YYYY): ', customer.set_dob)
            self.__get_valid_input('Enter address: ', customer.set_address)
            self.__get_valid_input('Enter phone number', customer.set_phone)
            self.__get_valid_input('Enter emai address: ', customer.set_email)
            print('\nCustomer', customer_id, 'updated successfully.')
        else:
            print('\nSorry, cannot find a customer with ID:', customer_id)

    def remove_customer(self):
        print('\n--| Remove a Customer |--')

        customer_id = input('Enter customer ID: ')
        customer = Customer.find_by_id(customer_id)

        if customer:
            # customer exists
            confirmation = input('Are you sure you want to remove customer ' + customer_id + '? (y/n): ')

            if confirmation.lower() in ['y', 'yes']:
                customer.remove()
                print('\nCustomer with ID', customer_id, 'removed successfully.')
            else:
                print('\nCustomer with ID', customer_id, 'was not removed.')
        else:
            print('\nSorry, cannot find a customer with ID:', customer_id)

    def view_all_customers(self):
        print('\n--| View all Customers |--')

        customers = Customer.get_all()

        customer_data = []
        for customer in customers:
            customer_data.append([customer.get_id(), customer.get_name(), customer.get_dob(), customer.get_address(), customer.get_phone(), customer.get_email()])

        if len(customer_data) > 0:
            table = Table(['Customer ID', 'Name', 'DOB', 'Address', 'Phone', 'Email'], customer_data)
            table.display()
        else:
            print('No customers to display.')

        prompt = ''
        while not prompt == 'exit':
            prompt = input("Enter 'exit' to go back: ")

    def view_shipments(self):
        print('\n--| View Shipments |--')

        customer_id = input('Enter customer ID: ')
        customer = Customer.find_by_id(customer_id)

        if customer:
            # customer exists
            customer.get_shipments()
        else:
            print('\nSorry, cannot find a customer with ID:', customer_id)

    # private methods

    # https://www.geeksforgeeks.org/higher-order-functions-in-python/
    def __get_valid_input(self, prompt, setter):
        valid_input = False
        while not valid_input:
            user_input = input(prompt)

            try:
                setter(user_input)
                valid_input = True
            except ValueError as e:
                print(e)

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
        return isinstance(weight, (int, float)) or weight <= 0

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

class ShipmentsController:
    def shipments_menu(self):
        menu = Menu('Shipment Management',[[1, 'Create a new shipment'],
                                           [2, 'Track a shipment'],
                                           [3, 'View all shipments'],
                                           [0, 'Quit shipment management',]])
        choice = menu.display_menu()

        if choice == '1':
            self.create_shipment()
            self.shipments_menu()
        elif choice == '2':
            self.track_shipment()
            self.shipments_menu()
        elif choice == '3':
            self.view_all_shipments()
            self.shipments_menu()
        elif choice == '0':
            print('\nQuitting customer management...')
        else:
            print('\nInvalid choice, please try again.')
            self.shipments_menu()

    def create_shipment(self):
        print('\n--| Create a Shipment |--')

        shipment = Shipment()

        next_id = 'S00' + str(Shipment.count() + 1)
        print('Suggested shipment ID:', next_id)
        self.__get_valid_input('Enter shipment ID: ', shipment.set_id)

        self.__get_valid_input('Enter origin location: ', shipment.set_origin)
        self.__get_valid_input('Enter destination location: ', shipment.set_destination)
        self.__get_valid_input('Enter weight: ', shipment.set_weight)

        Vehicle.get_all()
        self.__get_valid_input('Enter vehicle ID: ', shipment.set_vehicle_id)

        Customer.get_all()
        self.__get_valid_input('Enter customer ID: ', shipment.set_customer_id)

        try:
            shipment.save()
            print('\nShipment', shipment.get_id(), 'added successfully.')
        except ValueError as e:
            print(e)

    def track_shipment(self):
        print('\n--| Track a Shipment |--')

        shipment_id = input('Enter shipment ID: ')
        shipment = Shipment.find_by_id(shipment_id)

        if shipment:
            print('\nStatus of the shipment', shipment_id, 'is:', shipment.get_status())
        else:
            print('\nSorry, cannot find a shipment with ID:', shipment_id)

    def view_all_shipments(self):
        print('\n--| View all Shipments |--')

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

        prompt = ''
        while not prompt == 'exit':
            prompt = input("\nEnter 'exit' to go back: ")

class DeliveriesController:
    def deliveries_menu(self):
        menu = Menu('Delivery Management',[[1, 'Mark shipment delivery'],
                                           [2, 'View delivery status for a shipment'],
                                           [0, 'Quit shipment management',]])
        choice = menu.display_menu()

        if choice == '1':
            self.mark_shipment_delivered()
            self.deliveries_menu()
        elif choice == '2':
            self.view_delivery_status()
            self.deliveries_menu()
        elif choice == '0':
            print('\nQuitting delivery management...')
        else:
            print('\nInvalid choice, please try again.')
            self.deliveries_menu()

    def mark_shipment_delivered(self):
        print('\n--| Mark Shipment Delivery |--')

        shipment_id = input('Enter shipment ID: ')
        shipment = Shipment.find_by_id(shipment_id)

        if shipment:
            is_marked = shipment.mark_delivered()
            if is_marked:
                print('\nShipment', shipment_id, 'has been marked as delivered.')
            else:
                print('\nShipment with ID:', shipment_id, 'is already delivered.')
        else:
            print('\nSorry, cannot find a shipment with ID:', shipment_id)

    def view_delivery_status(self):
        print('\n--| View Delivery Status |--')

        shipment_id = input('Enter shipment ID: ')
        shipment = Shipment.find_by_id(shipment_id)

        if shipment:
            if shipment.get_delivery_status() == 'Delivered':
                # referred https://strftime.org/ to find the mask
                print('\nShipment', shipment_id, 'was delivered on', shipment.get_delivery_date())
            else:
                print('\nShipment', shipment_id, 'is not delivered yet.')
        else:
            print('\nSorry, cannot find a shipment with ID:', shipment_id)

    # private methods

    # https://www.geeksforgeeks.org/higher-order-functions-in-python/
    def __get_valid_input(self, prompt, setter):
        valid_input = False
        while not valid_input:
            user_input = input(prompt)

            try:
                setter(user_input)
                valid_input = True
            except ValueError as e:
                print(e)

class Main:
    def __init__(self):
        self.vehicles_controller = VehiclesController()
        self.customers_controller = CustomersController()
        self.shipments_controller = ShipmentsController()
        self.deliveries_controller = DeliveriesController()

    def main_menu(self):
        menu = Menu('Transportation Logistics System', [[1, 'Fleet Management'],
                                                        [2, 'Customer Management'],
                                                        [3, 'Shipment Management'],
                                                        [4, 'Delivery Management'],
                                                        [0, 'Quit']])

        choice = menu.display_menu()

        if choice == '1':
            self.vehicles_controller.fleets_menu()
            self.main_menu()
        elif choice == '2':
            self.customers_controller.customers_menu()
            self.main_menu()
        elif choice == '3':
            self.shipments_controller.shipments_menu()
            self.main_menu()
        elif choice == '4':
            self.deliveries_controller.deliveries_menu()
            self.main_menu()
        elif choice == '0':
            print('\nExiting the system. Goodbye!')
        else:
            print('\nInvalid choice, please try again.')
            # call run() method recursively
            self.main_menu()

try:
    for i in range(10):
        v = Vehicle('V00' + str(i + 1), random.choice(['Truck', 'Van', 'Car']), str(random.choice([100, 200, 300, 400, 500])))
        v.save()

    for i in range(10):
        c = Customer('C00' + str(i + 1), 'test name', '10/10/1990', '123 Main St, Sydney, NSW 2000, Australia', '0451506271', 'user@example.com')
        c.save()

    for i in range(20):
        s = Shipment('S00' + str(i + 1), 'Melbourne', 'Sydney', random.randint(10, 100), 'V001', 'C001')
        s.save()
except ValueError as e:
    print(e)

# Vehicle.get_all()
# Customer.get_all()
# Shipment.get_all()

main = Main()
main.main_menu()
