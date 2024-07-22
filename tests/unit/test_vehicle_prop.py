import pytest
from hypothesis import given, strategies as st
from technical_test_fortis.car import Car
from technical_test_fortis.bike import Bike
from technical_test_fortis.vehicle import Vehicle, find_best_vehicle

# Define strategies for valid inputs
valid_years = st.integers(min_value=1800, max_value=2100)
valid_tank_sizes = st.integers(min_value=1, max_value=100)
valid_consumptions = st.integers(min_value=1, max_value=20)
valid_technical_inspections = st.booleans()
valid_saddle_comforts = st.booleans()

# Define composite strategies for valid cars and bikes
valid_cars = st.builds(
    Car,
    year=valid_years,
    tank_size=valid_tank_sizes,
    consumption=valid_consumptions,
    technical_inspection=valid_technical_inspections
)

valid_bikes = st.builds(
    Bike,
    year=valid_years,
    consumption=valid_consumptions,
    saddle_comfort=valid_saddle_comforts
)

# Strategy for generating either a car or a bike
valid_vehicles = st.one_of(valid_cars, valid_bikes)


class TestVehicle:
    def test_vehicle_abstract_class(self):
        with pytest.raises(TypeError):
            Vehicle(2000, 50, 5)


class TestFindBestVehicle:
    @given(valid_vehicles, valid_vehicles)
    def test_find_best_vehicle(self, vehicle1, vehicle2):
        """Test find_best_vehicle function with randomly generated vehicles."""
        result = find_best_vehicle(vehicle1, vehicle2)
        assert result in (vehicle1, vehicle2), "Result should be one of the input vehicles"

        distance1 = vehicle1.compute_maximal_distance()
        distance2 = vehicle2.compute_maximal_distance()

        if distance1 > distance2:
            assert result == vehicle1, "Vehicle with greater distance should win"
        elif distance2 > distance1:
            assert result == vehicle2, "Vehicle with greater distance should win"
        else:
            assert result == vehicle2, "Second vehicle should win when distances are equal"

    @given(valid_cars, valid_cars)
    def test_find_best_vehicle_cars(self, car1, car2):
        """Test find_best_vehicle function with two cars."""
        result = find_best_vehicle(car1, car2)
        assert isinstance(result, Car), "Result should be a Car"
        self._assert_best_vehicle(car1, car2, result)

    @given(valid_bikes, valid_bikes)
    def test_find_best_vehicle_bikes(self, bike1, bike2):
        """Test find_best_vehicle function with two bikes."""
        result = find_best_vehicle(bike1, bike2)
        assert isinstance(result, Bike), "Result should be a Bike"
        self._assert_best_vehicle(bike1, bike2, result)

    @given(valid_cars, valid_bikes)
    def test_find_best_vehicle_car_and_bike(self, car, bike):
        """Test find_best_vehicle function with a car and a bike."""
        result = find_best_vehicle(car, bike)
        assert isinstance(result, (Car, Bike)), "Result should be either a Car or a Bike"
        self._assert_best_vehicle(car, bike, result)

    def _assert_best_vehicle(self, vehicle1, vehicle2, result):
        distance1 = vehicle1.compute_maximal_distance()
        distance2 = vehicle2.compute_maximal_distance()
        if distance1 > distance2:
            assert result == vehicle1, "Vehicle with greater distance should win"
        elif distance2 > distance1:
            assert result == vehicle2, "Vehicle with greater distance should win"
        else:
            assert result == vehicle2, "Second vehicle should win when distances are equal"

    def test_find_best_vehicle_edge_cases(self):
        """Test find_best_vehicle function with edge cases."""
        failed_car = Car(2005, 50, 5, False)
        normal_bike = Bike(2005, 1, True)
        assert find_best_vehicle(failed_car,
                                 normal_bike) == normal_bike, "Bike should win over car with failed inspection"

        zero_distance_car = Car(2005, 0, 5, True)
        zero_distance_bike = Bike(2005, 100, False)
        result = find_best_vehicle(zero_distance_car, zero_distance_bike)
        assert result in (zero_distance_car, zero_distance_bike), "One of the zero-distance vehicles should be returned"
        assert result == zero_distance_bike, "Second vehicle should be returned when both have zero distance"

    @pytest.mark.parametrize("invalid_input", [
        "Not a vehicle",
        123,
        None,
        [],
        {}
    ])
    def test_find_best_vehicle_invalid_inputs(self, invalid_input):
        """Test find_best_vehicle function with invalid inputs."""
        valid_car = Car(2005, 50, 5, True)
        with pytest.raises(AttributeError):
            find_best_vehicle(invalid_input, valid_car)
        with pytest.raises(AttributeError):
            find_best_vehicle(valid_car, invalid_input)