import pytest
from technical_test_fortis.car import  Car
@pytest.fixture
def create_car():
    def _create_car(year, tank_size, consumption, technical_inspection):
        return Car(year, tank_size, consumption, technical_inspection)

    return _create_car


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
