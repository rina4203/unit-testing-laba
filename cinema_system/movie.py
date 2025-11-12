#!/usr/bin/env python3
"""!
@file movie_manager.py
@author Filonenko (rina4203)
@version 1.1
@date 2025-11-12
@brief Module defining the core business logic for the cinema system.

@details
    This module contains the entity classes (dataclasses) `Movie`, `Screening`, `Booking`,
    and the main service class `CinemaManager`, which handles all operations.
    It is responsible for managing the movie catalog, screening schedules, and
    ticket bookings.


"""

import json
import uuid
from dataclasses import dataclass, field, asdict
from typing import List, Optional, Dict, Any

# --- Data Classes ---

@dataclass
class Movie:
    """!
    @brief A data container class (dataclass) for representing a movie.
    
    @details
        Stores all key information about a movie, such as title, year,
        director, genres, actors, runtime, and rating.
        Performs validation on the data immediately after object creation.
    """
    title: str
    year: int
    director: str
    genres: List[str] = field(default_factory=list)
    actors: List[str] = field(default_factory=list)
    runtime_minutes: int = 0
    rating: float = 0.0

    def __post_init__(self):
        """!
        @brief Performs field validation after object initialization.
        
        @details
            This method is automatically called by the dataclass.
            It checks if the rating, year, and runtime
            are within acceptable ranges.
            
        @throws ValueError If the rating is outside the range [0, 10].
        @throws ValueError If the release year is earlier than 1888 (the first film).
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
    
    @details
        Stores information about the movie title, screening time,
        total seats, and booked seats.
        Automatically generates a unique `screening_id` (UUIDv4) upon creation.
    """
    movie_title: str
    screening_time: str  # Example: "2023-10-27 19:00"
    total_seats: int
    screening_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    booked_seats: int = 0

    @property
    def available_seats(self) -> int:
        """!
        @brief A computed property to get the number of available seats.
        
        @details
            Dynamically calculates the number of free seats as the difference
            between total seats and booked seats.
            
        @return int The number of available seats (total_seats - booked_seats).
        """
        return self.total_seats - self.booked_seats

@dataclass
class Booking:
    """!
    @brief A data container class (dataclass) for representing a booking.
    
    @details
        Stores a reference to the screening ID, the movie title, and
        the number of tickets booked.
        Automatically generates a unique `booking_id` (UUIDv4) upon creation.
    """
    screening_id: str
    movie_title: str
    num_tickets: int
    booking_id: str = field(default_factory=lambda: str(uuid.uuid4()))


# --- Helper Function ---

def create_default_movies() -> List[Movie]:
    """!
    @brief Creates and returns an initial collection of 10 movies.
    
    @details
        Used for the initial population of `CinemaManager`
        if no other list of movies is provided.
        
    @return List[Movie] A list of `Movie` objects.
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


# --- Main Service Class ---

class CinemaManager:
    """!
    @brief The main class for managing the cinema.
    
    @details
        Aggregates and manages the collections of movies (_movies),
        screenings (screenings), and bookings (bookings).
        Provides a public API for interacting with the system (add,
        find, book, cancel).
        
    @example
    @code
        # Initialize the manager
        manager = CinemaManager()
        
        # Add a screening
        manager.add_screening("The Matrix", "2025-12-01 21:00", 100)
        
        # Find the screening
        s_list = manager.get_screenings_for_movie("The Matrix")
        s_id = s_list[0].screening_id
        
        # Book tickets
        booking = manager.book_tickets(s_id, 2)
        
        # Cancel the booking
        if booking:
            manager.cancel_booking(booking.booking_id)
    @endcode
    """

    def __init__(self, movies: Optional[List[Movie]] = None):
        """!
        @brief Constructor for the CinemaManager class.
        @param movies
            An optional list of movies for initialization.
            If `None`, the default list from
            `create_default_movies()` will be used.
        """
        self._movies: List[Movie] = movies if movies is not None else create_default_movies()
        self.screenings: List[Screening] = []
        self.bookings: List[Booking] = []

    def get_all_movies(self) -> List[Movie]:
        """!
        @brief Returns the complete list of movies.
        @return List[Movie] A list of all movies stored in the manager.
        """
        return self._movies
        
    def add_movie(self, movie: Movie) -> None:
        """!
        @brief Adds a new movie to the collection.
        
        @details
            Performs a check for duplicates based on title (case-insensitive)
            and year. If a duplicate is found,
            the addition is ignored.
            
        @param movie The `Movie` object to add.
        @return None
        """
        for m in self._movies:
            if m.title.lower() == movie.title.lower() and m.year == movie.year:
                return  # Ignore if duplicate
        self._movies.append(movie)

    def find_movie_by_title(self, title_query: str) -> List[Movie]:
        """!
        @brief Finds movies by a partial title.
        
        @details
            The search is case-insensitive.
            It checks if `title_query` is a substring of the movie titles.
            
        @param title_query The string to search for in movie titles.
        @return List[Movie] A list of movies matching the query.
        """
        return [m for m in self._movies if title_query.lower() in m.title.lower()]

    def add_screening(self, movie_title: str, screening_time: str, total_seats: int) -> Optional[Screening]:
        """!
        @brief Adds a new screening for an existing movie.
        
        @details
            Searches for a movie by its **exact** title (case-insensitive).
            If the movie is found, creates a new `Screening` object
            and adds it to the `self.screenings` list.
            
        @note
            If multiple movies exist with the same title
            (e.g., remakes), this method will add the screening for the first one found.
            
        @param movie_title The exact title of the movie.
        @param screening_time The screening time as a string (e.g., "2025-10-28 21:00").
        @param total_seats The total number of seats in the theater (must be > 0).
        
        @return Optional[Screening]
            The created `Screening` object on success,
            or `None` if the movie was not found.
        """
        # Find movie by exact title
        found_movies = [m for m in self._movies if m.title.lower() == movie_title.lower()]
        if not found_movies:
            return None  # Movie not found
        
        # Use the canonical movie title (with correct capitalization)
        canonical_title = found_movies[0].title
        
        new_screening = Screening(
            movie_title=canonical_title, 
            screening_time=screening_time, 
            total_seats=total_seats
        )
        self.screenings.append(new_screening)
        return new_screening

    def get_screenings_for_movie(self, movie_title: str) -> List[Screening]:
        """!
        @brief Gets all screenings for a specific movie.
        
        @details
            The search is performed using a partial title match
            (case-insensitive).
            
        @param movie_title The movie title to search for (can be partial).
        @return List[Screening] A list of screenings for that movie.
        """
        return [s for s in self.screenings if movie_title.lower() in s.movie_title.lower()]

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
            Checks if the screening exists, if `num_tickets` is a positive
            number, and if there are enough available seats.
            If all conditions are met, updates `booked_seats`
            on the screening and creates a new `Booking` object.
            
        @param screening_id The ID of the screening to book.
        @param num_tickets The number of tickets to book.
        
        @return Optional[Booking]
            The created `Booking` object on success,
            or `None` if the booking failed
            (invalid ID, not enough seats, 0 or negative
            number of tickets).
        """
        screening = self.get_screening_by_id(screening_id)
        
        # Validation 1: Screening must exist
        if not screening:
            return None
        
        # Validation 2: Must book a positive number of tickets and seats must be available
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
            It then removes the `Booking` object from the `self.bookings` list.
            
        @note
            If the screening associated with the booking was deleted,
            the booking will still be canceled (removed from the list),
            but the seats will not be returned.
            
        @param booking_id The unique ID of the booking to cancel.
        
        @return bool `True` if the booking was successfully found
                     and canceled, `False` otherwise.
        """
        # Find the booking by ID
        booking_to_cancel = next((b for b in self.bookings if b.booking_id == booking_id), None)
        
        if not booking_to_cancel:
            return False  # Booking not found

        # Find the corresponding screening
        screening = self.get_screening_by_id(booking_to_cancel.screening_id)
        
        # Return the seats if the screening still exists
        if screening:
            screening.booked_seats -= booking_to_cancel.num_tickets
            # Prevent negative seat counts if booking was "stale"
            if screening.booked_seats < 0:
                screening.booked_seats = 0
        
        # Remove the booking
        self.bookings.remove(booking_to_cancel)
        return True