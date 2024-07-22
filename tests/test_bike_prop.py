import pytest
from hypothesis import given, strategies as st
from technical_test_fortis.bike import Bike

# Define strategies for valid inputs
valid_years = st.integers(min_value=1800, max_value=2100)
valid_consumptions = st.integers(min_value=1, max_value=100)
valid_saddle_comforts = st.booleans()

# Define composite strategy for valid bikes
valid_bikes = st.builds(
    Bike,
    year=valid_years,
    consumption=valid_consumptions,
    saddle_comfort=valid_saddle_comforts
)


class TestBike:
    @given(valid_bikes)
    def test_bike_attributes(self, bike):
        """Test that bike attributes are correctly set during initialization."""
        assert 1800 <= bike.year <= 2100
        assert bike.tank_size == 0
        assert 1 <= bike.consumption <= 100
        assert isinstance(bike.saddle_comfort, bool)


    @given(valid_bikes)
    def test_bike_compute_maximal_distance(self, bike):
        """Test the compute_maximal_distance method for various scenarios."""
        distance = bike.compute_maximal_distance()
        assert isinstance(distance, int)
        assert distance >= 0
        assert distance <= 200  # Maximum possible distance


    @given(valid_bikes)
    def test_bike_str_representation(self, bike):
        """Test the string representation of the Bike class."""
        expected_str = f"Bike(year={bike.year}, consumption={bike.consumption}, saddle_comfort={bike.saddle_comfort})"
        assert str(bike) == expected_str

    @given(
        year=st.one_of(
            st.integers(max_value=1799),
            st.integers(min_value=2101),
            st.floats(),
            st.text()
        ),
        consumption=st.one_of(
            st.integers(max_value=0),
            st.floats(),
            st.text()
        ),
        saddle_comfort=st.one_of(
            st.integers(),
            st.floats(),
            st.text()
        )
    )
    def test_bike_invalid_inputs(self, year, consumption, saddle_comfort):
        """Test that invalid inputs raise appropriate exceptions."""
        with pytest.raises((ValueError, TypeError)):
            Bike(year, consumption, saddle_comfort)


