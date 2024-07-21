from technical_test_fortis.vehicle import Vehicle


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
        if not isinstance(technical_inspection, bool):
            raise ValueError("The technical_inspection must be a boolean value.")
        self.technical_inspection = technical_inspection

    def __str__(self) -> str:
        return f'Car(year={self.year}, tank_size={self.tank_size}, consumption={self.consumption}, technical_inspection={self.technical_inspection})'

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

