#!/usr/bin/env python3
"""!
@file unit_test.py
@author Filonenko Daryna (rina4203)
@version 1.2
@date 2025-11-12
@brief Unit test file for `CinemaManager`.

@details
    This file contains a test case (TestCase) for the `CinemaManager`
    using the built-in `unittest` module.
    The tests cover basic logic (CRUD) and specific
    edge cases (search, sorting, error handling) identified
    during development (TDD).

@note
    For these tests to run correctly, `movie_manager_update.py` must be
    located in the parent directory relative to this file.

"""

import unittest
import sys
import os
from datetime import datetime 

# Add the parent directory to the Python path
# to allow importing movie_manager_update
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from movie_manager_update import Movie, CinemaManager, Screening, Booking

class TestCinemaManagerBugs(unittest.TestCase):
    """!
    @brief A test suite for the CinemaManager class.
    
    @details
        Contains 21 tests that verify the correctness of
        adding, searching, booking, and canceling,
        as well as handling specific bugs and edge cases.
    @see CinemaManager
    """
    
    def setUp(self):
        """!
        @brief Sets up the test environment (fixture).
        
        @details
            This method is called automatically before *every*
            single test (test_*). It creates a new, clean instance
            of `CinemaManager` to ensure that tests
            do not interfere with each other.
        """
        self.manager = CinemaManager()

    def test_01_initial_movies_loaded_successfully(self):
        """!
        @brief Verifies that the initial list of 10 movies is loaded.
        @details
            Checks that `get_all_movies()` returns 10 movies
            and that the expected movie 'The Matrix' is among them.
        """
        self.assertEqual(len(self.manager.get_all_movies()), 10)
        # A specific expected movie is in the list
        self.assertTrue(
            any(m.title == "The Matrix" for m in self.manager.get_all_movies()),
            "Expected movie 'The Matrix' was not found in the initial list."
        )

    def test_02_add_unique_movie_successfully(self):
        """!
        @brief Verifies successful addition of a new, unique movie.
        @details
            Checks that `add_movie()` correctly increases the total
            movie count and that the added movie's data
            matches the expected values.
        """
        # successful addition of a new, unique movie
        initial_count = len(self.manager.get_all_movies())
        new_movie = Movie("Interstellar", 2014, "Christopher Nolan", ["Sci-Fi"], ["Matthew McConaughey"], 169, 8.6)
        self.manager.add_movie(new_movie)
        
        all_movies = self.manager.get_all_movies()
        self.assertEqual(len(all_movies), initial_count + 1)
        
        # find the added movie and check its data
        added_movie = next((m for m in all_movies if m.title == "Interstellar"), None)
        self.assertIsNotNone(added_movie)
        self.assertEqual(added_movie.year, 2014)
        self.assertEqual(added_movie.director, "Christopher Nolan")

    def test_03_add_duplicate_movie_is_ignored(self):
        """!
        @brief Verifies that attempting to add a duplicate movie is ignored.
        @details
            Checks that `add_movie()` does not add a movie if one
            with the same title and year already exists.
        """
        # attempt to add a duplicate movie is ignored
        initial_count = len(self.manager.get_all_movies())
        duplicate_movie = Movie("The Dark Knight", 2008, "Christopher Nolan")
        self.manager.add_movie(duplicate_movie)
        
        self.assertEqual(len(self.manager.get_all_movies()), initial_count)
        
        # there is ONE such movie in the system
        results = self.manager.find_movie_by_title("The Dark Knight")
        self.assertEqual(len(results), 1)
        # check the year
        self.assertEqual(results[0].year, 2008)

    def test_04_find_movie_by_full_title(self):
        """!
        @brief Verifies finding a movie by its full title (case-insensitive).
        """
        # find movie by full title
        results = self.manager.find_movie_by_title("the dark knight")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].title, "The Dark Knight")

    def test_05_find_movies_by_keyword(self):
        """!
        @brief Verifies finding movies by a keyword (partial match).
        """
        # find movies by keyword 'godfather'
        results = self.manager.find_movie_by_title("godfather")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].title, "The Godfather")

    def test_06_find_non_existent_movie_returns_empty(self):
        """!
        @brief Verifies that searching for a non-existent movie returns an empty list.
        """
        # search for non-existent movie returns empty list
        results = self.manager.find_movie_by_title("Non-Existent Movie 123")
        self.assertEqual(len(results), 0)

    def test_07_add_screening_successfully(self):
        """!
        @brief Verifies successful addition of a screening for an existing movie.
        @details
            Checks that `add_screening()` returns a `Screening` object
            and adds it to the internal `self.manager.screenings` list.
        """
        # successful addition of a screening for an existing movie
        screening = self.manager.add_screening("The Matrix", "2025-10-27 20:00", 100)
        self.assertIsNotNone(screening)
        self.assertIn(screening, self.manager.screenings)

    def test_08_add_screening_for_non_existent_movie_fails(self):
        """!
        @brief Verifies that a screening for a non-existent movie is not created.
        @details
            Checks that `add_screening()` returns `None`
            if the movie title is not found in the database.
        """
        # attempt to add screening for non-existent movie returns None
        screening = self.manager.add_screening("Non-Existent Movie 123", "2025-10-27 20:00", 100)
        self.assertIsNone(screening)

    def test_09_get_screening_by_valid_id(self):
        """!
        @brief Verifies finding a screening by its valid ID.
        """
        # find screening by existing ID
        screening = self.manager.add_screening("Inception", "2025-11-01 21:00", 120)
        found_screening = self.manager.get_screening_by_id(screening.screening_id)
        self.assertEqual(screening, found_screening)

    def test_10_get_screening_by_invalid_id_returns_none(self):
        """!
        @brief Verifies finding a screening by an invalid (non-existent) ID.
        """
        # find screening by non-existent ID returns None
        found_screening = self.manager.get_screening_by_id("invalid-uuid")
        self.assertIsNone(found_screening)

    def test_11_book_tickets_successfully(self):
        """!
        @brief Verifies successful booking of tickets.
        @details
            This test checks that `book_tickets` returns a booking object,
            correctly decreases the number of `available_seats`,
            and adds the booking to the `self.manager.bookings` list.
        """
        # successful booking and change in available seats
        screening = self.manager.add_screening("Fight Club", "2025-11-05 22:00", 50)
        initial_seats = screening.available_seats
        booking = self.manager.book_tickets(screening.screening_id, 5)
        
        self.assertIsNotNone(booking)
        self.assertEqual(screening.available_seats, initial_seats - 5)
        self.assertIn(booking, self.manager.bookings)
        
        # booking fields are filled correctly
        self.assertEqual(booking.screening_id, screening.screening_id)
        self.assertEqual(booking.num_tickets, 5)

    def test_12_book_tickets_for_non_existent_screening_fails(self):
        """!
        @brief Verifies that booking for a non-existent screening returns None.
        """
        # booking for non-existent screening returns None
        booking = self.manager.book_tickets("invalid-uuid", 5)
        self.assertIsNone(booking)

    def test_13_book_more_tickets_than_available_fails(self):
        """!
        @brief Verifies booking more tickets than are available.
        @details
            Checks that `book_tickets` returns `None` and does not change
            the number of available seats if not enough tickets are available.
        """
        # booking more tickets than available returns None
        screening = self.manager.add_screening("Parasite", "2025-11-10 19:30", 10)
        booking = self.manager.book_tickets(screening.screening_id, 11)
        self.assertIsNone(booking)
        self.assertEqual(screening.available_seats, 10)

    def test_14_cancel_booking_successfully(self):
        """!
        @brief Verifies successful cancellation of a booking.
        @details
            Checks that `cancel_booking` returns `True`,
            seats are returned to `available_seats`,
            and the booking is removed from the list.
        """
        # successful cancellation of booking and return of seats
        screening = self.manager.add_screening("Forrest Gump", "2025-12-01 18:00", 80)
        booking = self.manager.book_tickets(screening.screening_id, 10)
        self.assertEqual(screening.available_seats, 70)
        
        result = self.manager.cancel_booking(booking.booking_id)
        self.assertTrue(result)
        self.assertEqual(screening.available_seats, 80)
        # booking is actually removed from the list
        self.assertNotIn(booking, self.manager.bookings)

    def test_15_cancel_non_existent_booking_fails(self):
        """!
        @brief Verifies cancellation of a non-existent booking returns False.
        """
        # cancellation of non-existent booking returns False
        result = self.manager.cancel_booking("invalid-uuid")
        self.assertFalse(result)

    def test_16_get_screenings_for_movie_requires_exact_match(self):
        """!
        @brief Verifies `get_screenings_for_movie` uses an exact match.
        @details
            This test checks a bug where `get_screenings_for_movie("Father")`
            incorrectly returned screenings for "The Godfather" due to using `in`.
            It expects only the one, exact result.
        """
        self.manager.add_screening("The Godfather", "2025-10-28 19:00", 100)
        self.manager.add_movie(Movie("The Father", 2020, "Florian Zeller"))
        self.manager.add_screening("The Father", "2025-10-28 21:00", 50)
        
        screenings = self.manager.get_screenings_for_movie("The Father")
    
        self.assertEqual(len(screenings), 1, "Error: Screening search is not exact (finds 'The Godfather' when searching for 'The Father').")
        self.assertEqual(screenings[0].movie_title, "The Father")
        

    def test_17_screenings_are_sorted_chronologically(self):
        """!
        @brief Verifies that screenings are sorted by time.
        @details
            Adds screenings in the wrong order (22:00, then 10:00).
            Checks that `get_screenings_for_movie` returns them
            in chronological order (10:00, then 22:00).
        """
        title = "Inception"
        time1 = "2025-11-01 22:00"
        time2 = "2025-11-01 10:00"
        self.manager.add_screening(title, time1, 100)
        self.manager.add_screening(title, time2, 100)
        
        screenings = self.manager.get_screenings_for_movie(title)
        
        self.assertEqual(screenings[0].screening_time, time2, "Error: Screenings are not sorted by time (earlier screening is not first).")

    def test_18_cancel_booking_can_result_in_negative_seats(self):
        """!
        @brief Verifies that cancellation does not result in negative seats.
        @details
            Simulates a situation where `booked_seats` was externally
            changed to 0, and then a cancellation occurs. `booked_seats`
            should not become less than 0.
        """
        screening = self.manager.add_screening("The Dark Knight", "2025-11-20 20:00", 20)
        booking = self.manager.book_tickets(screening.screening_id, 5)

        screening.booked_seats = 0 # Simulate state error
        
        self.manager.cancel_booking(booking.booking_id)
        
        self.assertGreaterEqual(screening.booked_seats, 0, "Error: Booked seats cannot be negative after cancellation.")
        
    def test_19_add_screening_is_ambiguous_for_same_titles(self):
        """!
        @brief Verifies ambiguity when adding screenings for identical titles.
        @details
            Adds two movies named "Solaris" (1972 and 2002).
            `add_screening("Solaris")` doesn't know which movie to add to.
            The test expects the system to handle this ambiguity (return None).
        """
        solaris_1972 = Movie("Solaris", 1972, "Andrei Tarkovsky")
        solaris_2002 = Movie("Solaris", 2002, "Steven Soderbergh")
        self.manager.add_movie(solaris_1972)
        self.manager.add_movie(solaris_2002)
    
        screening = self.manager.add_screening("Solaris", "2025-12-25 19:00", 50)

        self.assertIsNone(screening, "Error: Adding a screening for duplicate titles should be disallowed (or require a movie ID).")

    def test_20_time_is_string_not_datetime(self):
        """!
        @brief Verfies that the system validates the time format.
        @details
            Checks if the system will allow creating a screening with an
            invalid time string ("not a date"). Expects None to be returned.
        """
        # system handles invalid time format
        screening = self.manager.add_screening("The Matrix", "not a date", 100)
        
        # system should validate time and return None
        self.assertIsNone(screening, "Error: The system should not allow creating screenings with an invalid time format.")
        
    def test_21_booking_with_non_integer_crashes(self):
        """!
        @brief Verifies that passing a non-integer (str) to `book_tickets` does not crash.
        @details
            The system should not crash with a `TypeError` if a user
            tries to book "two" tickets. It should handle the
            error gracefully (e.g., try-except) and return `None`.
        """
        screening = self.manager.add_screening("Parasite", "2025-11-30 21:00", 100)
        try:
            result = self.manager.book_tickets(screening.screening_id, "two")
            self.assertIsNone(result, "Error: Booking a non-integer number of tickets should return None.")
        except TypeError:
            self.fail("Error: The function crashed with TypeError instead of gracefully handling bad data.")
        except Exception as e:
            self.fail(f"Error: An unexpected error {type(e).__name__} occurred instead of graceful handling.")

if __name__ == '__main__':
    unittest.main()