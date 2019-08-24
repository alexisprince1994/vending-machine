import hypothesis.strategies as st
from hypothesis import given
import pytest


from vending_machine.utils import position_from_coordinates, coordinates_from_position


class TestPositionFromCoordinates:
    def test_valid_output(self):  # pylint: disable=no-self-use,invalid-name
        """
        Test case to ensure that the correct column
        gets looked up, and row gets passed through.
        """

        coordinates = position_from_coordinates(3, 2)
        assert coordinates == ("C", 2)

    @given(
        column=st.integers(min_value=1, max_value=26),
        row=st.integers(min_value=1, max_value=300),
    )
    def test_row_never_gets_changed(
        self, column: int, row: int
    ):  # pylint: disable=no-self-use,invalid-name
        """
        Tests to ensure that the row value doesn't gets altered
        by passing it through the function.
        """

        coordinates = position_from_coordinates(column, row)
        _, output_row = coordinates

        assert row == output_row

    @given(column=st.integers(min_value=1, max_value=26))
    def test_column_letter_only_one(
        self, column: int
    ):  # pylint: disable=no-self-use,invalid-name
        """
        Tests to ensure that the column letter output
        by the function is only one letter, not multiple (AB, BC, etc.)
        """
        row = 5
        coordinates = position_from_coordinates(column, row)
        letter, _ = coordinates

        assert len(letter) == 1

    @given(
        column=st.integers(min_value=1, max_value=26),
        row=st.integers(min_value=1, max_value=26),
    )
    def test_inverse_of_coordinates_from_position(
        self, column: int, row: int
    ):  # pylint: disable=no-self-use,invalid-name

        letter, row = position_from_coordinates(column, row)

        column_out, row = coordinates_from_position((letter, row))

    @given(column=st.integers(min_value=27), row=st.integers(min_value=1, max_value=26))
    def test_position_from_coordinates_raises_indexerror(
        self, column: int, row: int
    ):  # pylint: disable=no-self-use,invalid-name
        """
        Ensures that any column value larger than 26 (larger than string.ascii_uppercase)
        returns None
        """

        with pytest.raises(IndexError):
            _, _ = position_from_coordinates(column, row)
