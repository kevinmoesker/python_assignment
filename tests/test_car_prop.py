import pytest
from hypothesis import given, strategies as st
from technical_test_fortis.car import Car

# Define strategies for valid inputs
valid_years = st.integers(min_value=1800, max_value=2100)
valid_tank_sizes = st.integers(min_value=1, max_value=100)
valid_consumptions = st.integers(min_value=1, max_value=20)
valid_technical_inspections = st.booleans()

# Define composite strategy for valid cars
valid_cars = st.builds(
    Car,
    year=valid_years,
    tank_size=valid_tank_sizes,
    consumption=valid_consumptions,
    technical_inspection=valid_technical_inspections
)


class TestCar:
    @given(
        year=valid_years,
        tank_size=valid_tank_sizes,
        consumption=valid_consumptions,
        technical_inspection=valid_technical_inspections
    )
    def test_car_initialization(self, year, tank_size, consumption, technical_inspection):
        """Test that a Car can be correctly initialized with valid inputs."""
        car = Car(year, tank_size, consumption, technical_inspection)
        assert car.year == year
        assert car.tank_size == tank_size
        assert car.consumption == consumption
        assert car.technical_inspection == technical_inspection


    def test_car_str_representation(self):
        """Test the string representation of the Car class."""
        car = Car(2000, 50, 5, True)
        expected_str = "Car(year=2000, tank_size=50, consumption=5, technical_inspection=True)"
        assert str(car) == expected_str

    @given(
        year=st.one_of(st.integers(max_value=1799), st.integers(min_value=2101), st.floats(), st.text()),
        tank_size=st.one_of(st.integers(max_value=0), st.floats(), st.text()),
        consumption=st.one_of(st.integers(max_value=0), st.floats(), st.text()),
        technical_inspection=st.one_of(st.integers(), st.floats(), st.text())
    )
    def test_car_invalid_inputs(self, year, tank_size, consumption, technical_inspection):
        """Test that invalid inputs raise appropriate exceptions."""
        with pytest.raises((ValueError, TypeError)):
            Car(year, tank_size, consumption, technical_inspection)

    @given(valid_cars)
    def test_car_edge_cases(self, car):
        """Test edge cases for car creation and computation."""
        distance = car.compute_maximal_distance()

        if not car.technical_inspection:
            assert distance == 0
        elif car.tank_size == 1 and car.consumption == 1:
            assert 0 <= distance <= 1
        elif car.year == 1800:
            assert distance <= car.tank_size // car.consumption
        elif car.year == 2100:
            assert distance >= car.tank_size // car.consumption