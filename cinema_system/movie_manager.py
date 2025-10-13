
# movie_manager.py
import json
import uuid
from dataclasses import dataclass, field, asdict
from typing import List, Optional, Dict, Any

# --- Класи для представлення сутностей ---

@dataclass
class Movie:
    """Клас для представлення фільму з розширеними атрибутами."""
    title: str
    year: int
    director: str
    genres: List[str] = field(default_factory=list)
    actors: List[str] = field(default_factory=list)
    runtime_minutes: int = 0
    rating: float = 0.0

    def __post_init__(self):
        # Валідація даних
        if not (0 <= self.rating <= 10):
            raise ValueError("Рейтинг має бути в межах від 0 до 10.")
        if self.year < 1888:
            raise ValueError("Рік випуску фільму не може бути раніше 1888.")
        if self.runtime_minutes < 0:
            raise ValueError("Тривалість фільму не може бути від'ємною.")

@dataclass
class Screening:
    """Клас для представлення кіносеансу."""
    movie_title: str
    screening_time: str  # Наприклад, "2023-10-27 19:00"
    total_seats: int
    screening_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    booked_seats: int = 0

    @property
    def available_seats(self) -> int:
        return self.total_seats - self.booked_seats

@dataclass
class Booking:
    """Клас для представлення бронювання."""
    screening_id: str
    movie_title: str
    num_tickets: int
    booking_id: str = field(default_factory=lambda: str(uuid.uuid4()))

# --- Функція для створення початкової колекції ---

def create_default_movies() -> List[Movie]:
    """Створює та повертає початкову колекцію з 10 фільмів."""
    return [
        Movie("Втеча з Шоушенка", 1994, "Френк Дарабонт", ["Драма"], ["Тім Роббінс", "Морган Фрімен"], 142, 9.3),
        Movie("Хрещений батько", 1972, "Френсіс Форд Коппола", ["Кримінал", "Драма"], ["Марлон Брандо", "Аль Пачіно"], 175, 9.2),
        Movie("Темний лицар", 2008, "Крістофер Нолан", ["Екшн", "Кримінал", "Драма"], ["Крістіан Бейл", "Хіт Леджер"], 152, 9.0),
        Movie("Кримінальне чтиво", 1994, "Квентін Тарантіно", ["Кримінал", "Драма"], ["Джон Траволта", "Ума Турман", "Семюел Л. Джексон"], 154, 8.9),
        Movie("Форрест Гамп", 1994, "Роберт Земекіс", ["Драма", "Романтика"], ["Том Хенкс", "Робін Райт"], 142, 8.8),
        Movie("Початок", 2010, "Крістофер Нолан", ["Екшн", "Пригоди", "Фантастика"], ["Леонардо Ді Капріо", "Джозеф Гордон-Левітт"], 148, 8.8),
        Movie("Матриця", 1999, "Лана Вачовскі", ["Екшн", "Фантастика"], ["Кіану Рівз", "Лоуренс Фішберн"], 136, 8.7),
        Movie("Бійцівський клуб", 1999, "Девід Фінчер", ["Драма"], ["Бред Пітт", "Едвард Нортон"], 139, 8.8),
        Movie("Славні хлопці", 1990, "Мартін Скорсезе", ["Біографія", "Кримінал", "Драма"], ["Роберт Де Ніро", "Рей Ліотта", "Джо Пеші"], 146, 8.7),
        Movie("Паразити", 2019, "Пон Джун Хо", ["Комедія", "Драма", "Трилер"], ["Сон Кан Хо", "Лі Сон Гюн"], 132, 8.6)
    ]

# --- Головний керуючий клас ---

class CinemaManager:
    """Головний клас для управління кінотеатром: фільмами, сеансами та бронюваннями."""

    def __init__(self, movies: Optional[List[Movie]] = None):
        self._movies: List[Movie] = movies if movies is not None else create_default_movies()
        self.screenings: List[Screening] = []
        self.bookings: List[Booking] = []

    # --- Методи для управління фільмами ---
    
    def get_all_movies(self) -> List[Movie]:
        return self._movies
        
    def add_movie(self, movie: Movie):
        """Додає фільм до колекції, якщо його ще немає."""
        for m in self._movies:
            if m.title.lower() == movie.title.lower() and m.year == movie.year:
                return
        self._movies.append(movie)

    def find_movie_by_title(self, title_query: str) -> List[Movie]:
        """Знаходить фільми, назва яких містить запит."""
        return [m for m in self._movies if title_query.lower() in m.title.lower()]

    # --- Методи для управління сеансами ---

    def add_screening(self, movie_title: str, screening_time: str, total_seats: int) -> Optional[Screening]:
        """Додає новий сеанс для фільму, якщо такий фільм існує."""
        found_movies = [m for m in self._movies if m.title.lower() == movie_title.lower()]
        if not found_movies:
            return None
        
        new_screening = Screening(movie_title=found_movies[0].title, screening_time=screening_time, total_seats=total_seats)
        self.screenings.append(new_screening)
        return new_screening

    def get_screenings_for_movie(self, movie_title: str) -> List[Screening]:
        """Повертає всі сеанси для вказаного фільму."""
        return [s for s in self.screenings if movie_title.lower() in s.movie_title.lower()]

    def get_screening_by_id(self, screening_id: str) -> Optional[Screening]:
        """Знаходить сеанс за його ID."""
        for screening in self.screenings:
            if screening.screening_id == screening_id:
                return screening
        return None

    # --- Методи для управління бронюваннями ---

    def book_tickets(self, screening_id: str, num_tickets: int) -> Optional[Booking]:
        """Бронює квитки на сеанс."""
        screening = self.get_screening_by_id(screening_id)
        if not screening:
            return None  # Сеанс не знайдено
        
        if not (0 < num_tickets <= screening.available_seats):
            return None # Неправильна кількість квитків або недостатньо місць
        
        screening.booked_seats += num_tickets
        new_booking = Booking(
            screening_id=screening_id, 
            movie_title=screening.movie_title,
            num_tickets=num_tickets
        )
        self.bookings.append(new_booking)
        return new_booking

    def cancel_booking(self, booking_id: str) -> bool:
        """Скасовує бронювання та повертає квитки."""
        booking_to_cancel = next((b for b in self.bookings if b.booking_id == booking_id), None)
        
        if not booking_to_cancel:
            return False

        screening = self.get_screening_by_id(booking_to_cancel.screening_id)
        if screening:
            screening.booked_seats -= booking_to_cancel.num_tickets
        
        self.bookings.remove(booking_to_cancel)
        return True
