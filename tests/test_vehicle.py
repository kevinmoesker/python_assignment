import pytest
from technical_test_fortis.car import  Car
from technical_test_fortis.bike import Bike
from technical_test_fortis.vehicle import Vehicle, find_best_vehicle


@pytest.fixture
def create_car():
    def _create_car(year, tank_size, consumption, technical_inspection):
        return Car(year, tank_size, consumption, technical_inspection)

    return _create_car


@pytest.fixture
def create_bike():
    def _create_bike(year, consumption, saddle_comfort):
        return Bike(year, consumption, saddle_comfort)

    return _create_bike


# Adding test to validate inputs on bike creation
@pytest.mark.parametrize("year, consumption, saddle_comfort", [
    (-2000, 1, True),  # Negative year
    (2000, -1, True),  # Negative consumption
    (2000, 1, "Comfy"),  # Saddle comfort not a boolean
    (2000, '1', True),  # Consumption not a number
    ('2000', 1, True),  # Year not a number
])
def test_bike_creation_invalid_inputs(create_bike, year, consumption, saddle_comfort):
    with pytest.raises(ValueError):
        create_bike(year, consumption, saddle_comfort)


def test_car_creation_invalid_inputs(create_car):
    invalid_inputs = [
        (-2000, 50, 5, True),  # invalid year (negative)
        (2000, -50, 5, True),  # invalid tank size (negative)
        (2000, 50, -5, True),  # invalid consumption (negative)
        (2000, 50, 5, "Yes"),  # invalid technical_inspection (not a boolean)
        (2000, 50, 0, True),
        (0, 50, 0, True)
    ]

    for inputs in invalid_inputs:
        with pytest.raises(ValueError):
            create_car(*inputs)


class TestVehicle:
    def test_vehicle_abstract_class(self):
        with pytest.raises(TypeError):
            Vehicle(2000, 50, 5)


class TestCar:
    @pytest.mark.parametrize("year, tank_size, consumption, technical_inspection, expected_distance", [
        (2005, 50, 5, True, 10),  # Normal case
        (1995, 50, 5, True, 9),  # Old car (10% reduction)
        (2015, 50, 5, True, 11),  # New car (10% increase)
        (2005, 50, 5, False, 0),  # Failed technical inspection
        (2000, 40, 4, True, 10),  # Different tank size and consumption
        (2010, 60, 6, True, 10),  # Larger tank, higher consumption
        (1900, 50, 5, True, 9),  # Very old car
        (2100, 50, 5, True, 11),  # Future car
        (2005, 0, 5, True, 0),  # Zero tank size
        # (2005, 50, 0, True, float('inf')),  # Zero consumption
    ])
    def test_car_compute_maximal_distance(self, create_car, year, tank_size, consumption, technical_inspection,
                                          expected_distance):
        car = create_car(year, tank_size, consumption, technical_inspection)
        assert car.compute_maximal_distance() == expected_distance

    def test_car_attributes(self, create_car):
        car = create_car(2005, 50, 5, True)
        assert car.year == 2005
        assert car.tank_size == 50
        assert car.consumption == 5
        assert car.technical_inspection is True

    def test_car_str_representation(self, create_car):
        car = create_car(2005, 50, 5, True)
        expected_str = "Car(year=2005, tank_size=50, consumption=5, technical_inspection=True)"
        assert str(car) == expected_str

    @pytest.mark.parametrize("year, tank_size, consumption, technical_inspection", [
        (-2000, 50, 5, True),
        (2000, -50, 5, True),
        (2000, 50, -5, True),
        (2000, 50, 5, "Not a boolean"),
    ])
    def test_car_invalid_inputs(self, create_car, year, tank_size, consumption, technical_inspection):
        with pytest.raises(ValueError):
            create_car(year, tank_size, consumption, technical_inspection)


class TestBike:
    @pytest.mark.parametrize("year, consumption, saddle_comfort, expected_distance", [
        (2005, 1, True, 200),  # Comfortable saddle
        (2005, 1, False, 100),  # Uncomfortable saddle
        (2005, 2, True, 100),  # Higher consumption, comfortable saddle
        (2005, 2, False, 50),  # Higher consumption, uncomfortable saddle
        # Lower consumption, comfortable saddle
        # Older bike, medium consumption, uncomfortable saddle
        # Very low consumption
        (2005, 10, False, 10),  # Very high consumption
    ])
    def test_bike_compute_maximal_distance(self, create_bike, year, consumption, saddle_comfort, expected_distance):
        bike = create_bike(year, consumption, saddle_comfort)
        assert bike.compute_maximal_distance() == expected_distance

    def test_bike_attributes(self, create_bike):
        bike = create_bike(2005, 1, True)
        assert bike.year == 2005
        assert bike.tank_size == 0
        assert bike.consumption == 1
        assert bike.saddle_comfort is True

    def test_bike_str_representation(self, create_bike):
        bike = create_bike(2005, 1, True)
        expected_str = "Bike(year=2005, consumption=1, saddle_comfort=True)"
        assert str(bike) == expected_str

    @pytest.mark.parametrize("year, consumption, saddle_comfort", [
        (-2000, 1, True),
        (2000, -1, True),
        (2000, 1, "Not a boolean"),
    ])
    def test_bike_invalid_inputs(self, create_bike, year, consumption, saddle_comfort):
        with pytest.raises(ValueError):
            create_bike(year, consumption, saddle_comfort)


class TestFindBestVehicle:
    @pytest.mark.parametrize("vehicle1, vehicle2, expected", [
        (Car(2005, 50, 5, True), Car(2015, 50, 5, True), 1),  # Newer car wins
        (Car(2005, 50, 5, True), Car(2005, 50, 5, False), 0),  # Car with passed inspection wins
        (Bike(2005, 1, True), Bike(2005, 1, False), 0),  # Bike with comfortable saddle wins
        (Car(2005, 200, 5, True), Bike(2005, 5, False), 0),  # Car wins over bike
        (Car(2005, 10, 5, True), Bike(2005, 1, True), 1),  # Bike wins over car with small tank
        (Car(2010, 60, 6, True), Bike(2005, 1, True), 1),  # Bike with very low consumption wins

    ])
    def test_find_best_vehicle(self, vehicle1, vehicle2, expected):
        result = find_best_vehicle(vehicle1, vehicle2)
        expected_vehicle = [vehicle1, vehicle2][expected]
        assert result is expected_vehicle, f"Expected {type(expected_vehicle).__name__}, but got {type(result).__name__}"

    def test_find_best_vehicle_equal_distance(self, create_car):
        car1 = create_car(2005, 50, 5, True)
        car2 = create_car(2005, 50, 5, True)
        result = find_best_vehicle(car1, car2)
        assert result is car2, "Expected the second vehicle when distances are equal"

    def test_find_best_vehicle_with_different_types(self, create_car, create_bike):
        car = create_car(2005, 200, 5, True)
        bike = create_bike(2005, 5, False)
        result = find_best_vehicle(car, bike)
        assert result is car, "Expected car to win over bike with equal distances"

    def test_find_best_vehicle_edge_cases(self, create_car, create_bike):
        # Test with a car that has failed inspection vs a bike
        failed_car = create_car(2005, 50, 5, False)
        normal_bike = create_bike(2005, 1, True)
        assert find_best_vehicle(failed_car, normal_bike) is normal_bike

    def test_find_best_vehicle_invalid_inputs(self):
        with pytest.raises(AttributeError):
            find_best_vehicle("Not a vehicle", Car(2005, 50, 5, True))
        with pytest.raises(AttributeError):
            find_best_vehicle(Car(2005, 50, 5, True), "Not a vehicle")
