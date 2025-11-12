#!/usr/bin/env python3
"""!
@file movie_manager.py
@author Filonenko Daryna (rina4203)
@version 2.1
@date 2025-11-12
@brief Module defining the core business logic and data models for the cinema system.

@details
    This module contains the entity classes (dataclasses) `Movie`, `Screening`, `Booking`,
    and the main service class `CinemaManager`. This version includes
    bug fixes identified during unit testing.

@see main.py, unit_test.py
"""

import json
import uuid
from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime


@dataclass
class Movie:
    """!
    @brief A data container class (dataclass) for representing a movie.
    @details Stores all key information about a movie.
    """
    title: str              ##< The title of the movie.
    year: int               ##< The release year of the movie.
    director: str           ##< The director of the movie.
    genres: List[str] = field(default_factory=list)     ##< A list of genres.
    actors: List[str] = field(default_factory=list)     ##< A list of main actors.
    runtime_minutes: int = 0  ##< The runtime of the movie in minutes.
    rating: float = 0.0     ##< The movie's rating (e.g., out of 10.0).

    def __post_init__(self):
        """!
        @brief Validates data after object initialization.
        @throws ValueError If the rating is outside the range [0, 10].
        @throws ValueError If the release year is earlier than 1888.
        @throws ValueError If the film runtime is negative.
        """
        if not (0 <= self.rating <= 10):
            raise ValueError("Rating must be between 0 and 10.")
        if self.year < 1888:
            raise ValueError("Movie release year cannot be earlier than 1888.")
        if self.runtime_minutes < 0:
            raise ValueError("Movie runtime cannot be negative.")

@dataclass
class Screening:
    """!
    @brief A data container class (dataclass) for representing a movie screening.
    @details Stores information about the showtime, movie, and seat capacity.
    """
    movie_title: str        ##< The title of the movie being shown.
    screening_time: str     ##< The time of the screening in 'YYYY-MM-DD HH:MM' format.
    total_seats: int        ##< The total number of seats in the theater.
    screening_id: str = field(default_factory=lambda: str(uuid.uuid4())) ##< Unique ID for the screening (UUIDv4).
    booked_seats: int = 0   ##< The number of seats already booked.

    @property
    def available_seats(self) -> int:
        """!
        @brief Calculates the number of available seats.
        @return The number of seats available for booking.
        """
        return self.total_seats - self.booked_seats

@dataclass
class Booking:
    """!
    @brief A data container class (dataclass) for representing a booking.
    @details Links a user (implicitly) to a specific screening and number of tickets.
    """
    screening_id: str       ##< The ID of the screening being booked.
    movie_title: str        ##< The title of the movie (for convenience).
    num_tickets: int        ##< The number of tickets booked.
    booking_id: str = field(default_factory=lambda: str(uuid.uuid4())) ##< Unique ID for the booking (UUIDv4).


def create_default_movies() -> List[Movie]:
    """!
    @brief Creates an initial list of movies.
    @return A list of Movie objects with test data.
    """
    return [
        Movie("The Shawshank Redemption", 1994, "Frank Darabont", ["Drama"], ["Tim Robbins", "Morgan Freeman"], 142, 9.3),
        Movie("The Godfather", 1972, "Francis Ford Coppola", ["Crime", "Drama"], ["Marlon Brando", "Al Pacino"], 175, 9.2),
        Movie("The Dark Knight", 2008, "Christopher Nolan", ["Action", "Crime", "Drama"], ["Christian Bale", "Heath Ledger"], 152, 9.0),
        Movie("Pulp Fiction", 1994, "Quentin Tarantino", ["Crime", "Drama"], ["John Travolta", "Uma Thurman", "Samuel L. Jackson"], 154, 8.9),
        Movie("Forrest Gump", 1994, "Robert Zemeckis", ["Drama", "Romance"], ["Tom Hanks", "Robin Wright"], 142, 8.8),
        Movie("Inception", 2010, "Christopher Nolan", ["Action", "Adventure", "Sci-Fi"], ["Leonardo DiCaprio", "Joseph Gordon-Levitt"], 148, 8.8),
        Movie("The Matrix", 1999, "Lana Wachowski", ["Action", "Sci-Fi"], ["Keanu Reeves", "Laurence Fishburne"], 136, 8.7),
        Movie("Fight Club", 1999, "David Fincher", ["Drama"], ["Brad Pitt", "Edward Norton"], 139, 8.8),
        Movie("Goodfellas", 1990, "Martin Scorsese", ["Biography", "Crime", "Drama"], ["Robert De Niro", "Ray Liotta", "Joe Pesci"], 146, 8.7),
        Movie("Parasite", 2019, "Bong Joon Ho", ["Comedy", "Drama", "Thriller"], ["Song Kang-ho", "Lee Sun-kyun"], 132, 8.6)
    ]


class CinemaManager:
    """!
    @brief The main class for managing the cinema's operations.
    
    @details
        Aggregates and manages the collections of movies, screenings, and bookings.
        Provides a public API for interacting with the system.
        
    @example
    @code
        manager = CinemaManager()
        # Add a screening for an existing movie
        s = manager.add_screening("The Matrix", "2025-12-01 21:00", 100)
        
        if s:
            # Book tickets
            booking = manager.book_tickets(s.screening_id, 2)
            if booking:
                # Cancel the booking
                manager.cancel_booking(booking.booking_id)
    @endcode
    @see Movie, Screening, Booking
    """

    def __init__(self, movies: Optional[List[Movie]] = None):
        """!
        @brief Constructor for the CinemaManager class.
        @param movies
            An optional list of movies. If `None`,
            the default list is loaded.
        @see create_default_movies()
        """
        self._movies: List[Movie] = movies if movies is not None else create_default_movies()
        self.screenings: List[Screening] = []
        self.bookings: List[Booking] = []

    def get_all_movies(self) -> List[Movie]:
        """!
        @brief Returns the complete list of movies.
        @return List[Movie] A list of all movies.
        """
        return self._movies
        
    def add_movie(self, movie: Movie) -> None:
        """!
        @brief Adds a new movie to the collection.
        @note If a duplicate (by title and year) is found, the addition is ignored.
        @param movie The `Movie` object to add.
        @return None
        """
        for m in self._movies:
            if m.title.lower() == movie.title.lower() and m.year == movie.year:
                return
        self._movies.append(movie)

    def find_movie_by_title(self, title_query: str) -> List[Movie]:
        """!
        @brief Finds movies by a partial title (substring search).
        @param title_query The string to search for (case-insensitive).
        @return List[Movie] A list of found movies.
        """
        return [m for m in self._movies if title_query.lower() in m.title.lower()]

    def add_screening(self, movie_title: str, screening_time: str, total_seats: int) -> Optional[Screening]:
        """!
        @brief Adds a new screening (with validation).
        
        @note
            Will return `None` if:
            1. The `screening_time` format is not 'YYYY-MM-DD HH:MM'.
            2. Exactly one movie with `movie_title` is not found (i.e., 0 or >1 matches).
            
        @param movie_title The exact title of the movie.
        @param screening_time The time string (e.g., '2025-10-28 21:00').
        @param total_seats The total number of seats.
        
        @return Optional[Screening] The created `Screening` object, or `None` if validation fails.
        """
        try:
            # 1. Validate time format
            datetime.strptime(screening_time, '%Y-%m-%d %H:%M')
        except ValueError:
            return None # Invalid time format
            
        # 2. Find movie by exact title
        found_movies = [m for m in self._movies if m.title.lower() == movie_title.lower()]
        
        # 3. Check for ambiguity or no-match
        if len(found_movies) != 1:
            return None # Movie not found or title is ambiguous
        
        movie = found_movies[0]
        new_screening = Screening(movie_title=movie.title, screening_time=screening_time, total_seats=total_seats)
        self.screenings.append(new_screening)
        return new_screening

    def get_screenings_for_movie(self, movie_title: str) -> List[Screening]:
        """!
        @brief Gets all screenings for a movie, sorted chronologically.
        
        @details
            Finds screenings by **exact** title match (case-insensitive)
            and returns them sorted by `screening_time`.
            
        @param movie_title The exact movie title to search for.
        @return List[Screening] A chronologically sorted list of screenings (can be empty).
        """
        found_screenings = [s for s in self.screenings if movie_title.lower() == s.movie_title.lower()]
        # Sort by the time string
        return sorted(found_screenings, key=lambda s: s.screening_time)

    def get_screening_by_id(self, screening_id: str) -> Optional[Screening]:
        """!
        @brief Finds a screening by its unique ID.
        
        @param screening_id The unique identifier (UUID) of the screening.
        @return Optional[Screening] The found `Screening` object or `None`.
        """
        for screening in self.screenings:
            if screening.screening_id == screening_id:
                return screening
        return None


    def book_tickets(self, screening_id: str, num_tickets: int) -> Optional[Booking]:
        """!
        @brief Books a specified number of tickets for a screening.
        
        @details
            Validates that `num_tickets` is an integer.
            Checks if the screening exists and has enough available seats.
            
        @param screening_id The ID of the screening to book.
        @param num_tickets The number of tickets (must be an `int` > 0).
        
        @return Optional[Booking]
            The created `Booking` object on success,
            or `None` if validation fails.
        @see Booking, Screening.available_seats
        """
        # 1. Validate input type
        if not isinstance(num_tickets, int):
            return None

        screening = self.get_screening_by_id(screening_id)
        
        # 2. Validate screening existence
        if not screening:
            return None
        
        # 3. Validate ticket count and availability
        if not (0 < num_tickets <= screening.available_seats):
            return None
        
        # Update state
        screening.booked_seats += num_tickets
        
        # Create booking record
        new_booking = Booking(
            screening_id=screening_id, 
            movie_title=screening.movie_title,
            num_tickets=num_tickets
        )
        self.bookings.append(new_booking)
        return new_booking

    def cancel_booking(self, booking_id: str) -> bool:
        """!
        @brief Cancels an existing booking by its ID.
        
        @details
            Finds the booking by `booking_id`. If found,
            it locates the corresponding screening and returns
            the booked tickets (decrements `booked_seats`).
            
        @note
            Uses `max(0, ...)` to prevent the seat count from ever
            becoming negative, ensuring data integrity.
            
        @param booking_id The unique ID of the booking to cancel.
        
        @return bool `True` if cancellation was successful, `False` otherwise.
        """
        booking_to_cancel = next((b for b in self.bookings if b.booking_id == booking_id), None)
        
        if not booking_to_cancel:
            return False

        screening = self.get_screening_by_id(booking_to_cancel.screening_id)
        if screening:
            # Return seats, ensuring the count cannot go below zero
            screening.booked_seats = max(0, screening.booked_seats - booking_to_cancel.num_tickets)
        
        self.bookings.remove(booking_to_cancel)
        return True