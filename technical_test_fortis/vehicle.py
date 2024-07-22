from abc import ABC, abstractmethod


class Vehicle(ABC):
    """

    The Vehicle class is an abstract base class that represents a generic vehicle.

    Attributes:
        - year (int): The year of manufacture of the vehicle.
        - tank_size (int): The size of the vehicle's fuel tank.
        - consumption (int): The fuel consumption rate of the vehicle in liters per kilometer.

    Methods:
        - __init__(year: int, tank_size: int, consumption: int) -> None:
            Initializes a new instance of the Vehicle class.
            Raises a ValueError if any of the input arguments are invalid.

        - compute_maximal_distance() -> int:
            Computes and returns the maximal distance that the vehicle can travel with its current fuel.

    """
    def __init__(self, year: int, tank_size: int, consumption: int) -> None:

        def validate_input(input_value, minimum, error_message):
            if not isinstance(input_value, int):
                raise TypeError("Input value must be of type int.")
            elif input_value < minimum:
                raise ValueError(error_message)

        validate_input(year, 1, "The year of manufacture must be a positive integer.")
        validate_input(tank_size, 0, "The tank size must be a non-negative integer.")
        validate_input(consumption, 1, "The consumption must be a positive integer.")
        self.year = year
        self.tank_size = tank_size
        self.consumption = consumption  # 5L per km -> consumption = 5

    @abstractmethod
    def compute_maximal_distance(self) -> int:
        ...


def find_best_vehicle(vehicle1: Vehicle, vehicle2: Vehicle) -> Vehicle:
    """
    This function takes two vehicles as arguments and return the one with the highest autonomy.
    :param vehicle1: the first vehicle
    :param vehicle2: the second vehicle
    :return: the vehicle with the highest autonomy
    """

    if vehicle1.compute_maximal_distance() > vehicle2.compute_maximal_distance():
        return vehicle1
    else:
        return vehicle2
