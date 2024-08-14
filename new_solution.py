import re

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

    # other public methods

    def get_all(cls):
        return cls._instances

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

    @classmethod
    def find_by_id(cls, object_id):
        for instance in cls._instances:
            if instance.get_id() == object_id:
                return instance

        return None

    # private methods

    def __is_unique_id(self, object_id):
        for instance in self._instances:
            if instance._vehicle_id == object_id:
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
        self.set_id(vehicle_id)
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

    @classmethod
    def get_all(cls):
        vehicle_data = []
        for vehicle in cls._instances:
            vehicle_data.append([vehicle.get_id(), vehicle.get_vehicle_type(), vehicle.get_capacity()])

        if len(vehicle_data) > 0:
            table = Table(['Vehicle ID', 'Type', 'Capacity'], vehicle_data)
            table.display()
        else:
            print('\nNo vehicles to display.')

    # private methods

    def __is_valid_capacity(self, capacity):
        return capacity.isdigit() and int(capacity) > 0


try:
    v = Vehicle(vehicle_id='V001', capacity=500)
    v.save()
except ValueError as e:
    print(e)

Vehicle.get_all()
