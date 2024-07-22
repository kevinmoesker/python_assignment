import pytest
from technical_test_fortis.car import Car
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


class TestVehicle:
    def test_vehicle_abstract_class(self):
        with pytest.raises(TypeError):
            Vehicle(2000, 50, 5)


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
