from technical_test_fortis.vehicle import Vehicle


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


        if not isinstance(year, int):
            raise TypeError("The 'year' attribute must be of type 'int'")

        if not isinstance(consumption, int):
            raise TypeError("The 'consumption' attribute must be of type 'int'")

        if not isinstance(saddle_comfort, bool):
            raise TypeError("The 'saddle_comfort' attribute must be of type 'bool'")


        self.saddle_comfort = saddle_comfort

    def __str__(self) -> str:
        return f'Bike(year={self.year}, consumption={self.consumption}, saddle_comfort={self.saddle_comfort})'

    def compute_maximal_distance(self) -> int:
        """
        This method overrides the abstract method in the parent class.
        It returns twice the distance if the saddle is comfortable, in contrast to the Car class where the mileage
        is affected by the technical inspection and the year of manufacture.
        """
        base_distance = 100 // self.consumption  # TODO change to something more realistic, maybe introduce a tanksize as well.

        if self.saddle_comfort:
            # If saddle is comfortable, the base distance is doubled.
            return int(2.0 * base_distance)
        else:
            return int(base_distance)
