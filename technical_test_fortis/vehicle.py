from abc import ABC, abstractmethod


class Vehicle(ABC):
    def __init__(self, year: int, tank_size: int, consumption: int) -> None:
        self.year = year
        self.tank_size = tank_size
        self.consumption = consumption  # 5L per km -> consumption = 5

    @abstractmethod
    def compute_maximal_distance(self) -> int:
        ...


class Car(Vehicle):
    """

    This class represents a car. It is a subclass of Vehicle.

    Attributes:
    - year (int): The year of the car's manufacture.
    - tank_size (int): The size of the car's fuel tank in liters.
    - consumption (int): The car's fuel consumption in liters per 100 kilometers.
    - technical_inspection (bool): Whether the car has passed its technical inspection.

    Methods:
    - __init__(year: int, tank_size: int, consumption: int, technical_inspection: bool) -> None:
        Initializes the Car object with the given year, tank size, consumption, and technical inspection status.

    - compute_maximal_distance() -> int:
        Computes and returns the theoretical maximum distance the car can travel on a full tank of fuel,
        taking into account its year of manufacture and technical inspection status.

    """

    def __init__(self, year: int, tank_size: int, consumption: int, technical_inspection: bool) -> None:
        super().__init__(year, tank_size, consumption)
        self.technical_inspection = technical_inspection

    def compute_maximal_distance(self) -> int:
        if not self.technical_inspection:
            # if the technical inspection is not done, the car cannot move
            return 0

        theoretical_max_distance = self.tank_size / self.consumption

        if self.year < 2000:
            # if the car is from before 2000, the theoretical maximal distance is reduced by 10%
            theoretical_max_distance *= 0.9
        elif self.year > 2010:
            # if the car is from after 2010, the theoretical maximal distance is increased by 10%
            theoretical_max_distance *= 1.1

        return int(theoretical_max_distance)


class Bike(Vehicle):
    """
    This class represents a bike. It is a subclass of Vehicle.

    Attributes:
    - year (int): The year of the bike's manufacture.
    - tank_size (int): This attribute does not apply to bikes. Set to 0 as default.
    - consumption (int): This attribute represents the consumption of energy of the rider per km,
      typically it has a very low value.
    - saddle_comfort (bool): Whether the bike has a very comfortable saddle or not.

    Methods:
    - __init__(year: int, consumption: int, saddle_comfort: bool) -> None:
       Initializes the Bike object with the given year, consumption, and saddle_comfort status.

    - compute_maximal_distance() -> int:
        Computation of how far a person can travel on this Bike under ideal circumstances.
        The impact of saddle_comfort is to double the distance if it is comfortable.
    """

    def __init__(self, year: int, consumption: int, saddle_comfort: bool) -> None:
        super().__init__(year, 0, consumption)
        self.saddle_comfort = saddle_comfort

    def compute_maximal_distance(self) -> int:
        """
        This method overrides the abstract method in the parent class.
        It returns twice the distance if the saddle is comfortable, in contrast to the Car class where the mileage
        is affected by the technical inspection and the year of manufacture.
        """
        base_distance = 100 / self.consumption

        if self.saddle_comfort:
            # If saddle is comfortable, the base distance is doubled.
            return int(2 * base_distance)
        else:
            return int(base_distance)


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


""" 
Task 3: 
Add a unit test on find_best_vehicle
"""
