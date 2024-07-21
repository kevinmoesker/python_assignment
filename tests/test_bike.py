import pytest
from technical_test_fortis.bike import Bike


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
