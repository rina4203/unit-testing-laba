import unittest
import sys
import os
from datetime import datetime 

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from movie_manager_update import Movie, CinemaManager, Screening, Booking

class TestCinemaManagerBugs(unittest.TestCase):
    def setUp(self):
        self.manager = CinemaManager()

    def test_01_initial_movies_loaded_successfully(self):
        self.assertEqual(len(self.manager.get_all_movies()), 10)
        #конкретний очікуваний фільм є у списку
        self.assertTrue(
            any(m.title == "Матриця" for m in self.manager.get_all_movies()),
            "Очікуваний фільм 'Матриця' не знайдено серед початкових."
        )

    def test_02_add_unique_movie_successfully(self):
        # успішне додавання нового, унікального фільму
        initial_count = len(self.manager.get_all_movies())
        new_movie = Movie("Інтерстеллар", 2014, "Крістофер Нолан", ["Фантастика"], ["Меттью Макконахі"], 169, 8.6)
        self.manager.add_movie(new_movie)
        
        all_movies = self.manager.get_all_movies()
        self.assertEqual(len(all_movies), initial_count + 1)
        
        # знаходимо доданий фільм і перевіряємо його дані
        added_movie = next((m for m in all_movies if m.title == "Інтерстеллар"), None)
        self.assertIsNotNone(added_movie)
        self.assertEqual(added_movie.year, 2014)
        self.assertEqual(added_movie.director, "Крістофер Нолан")

    def test_03_add_duplicate_movie_is_ignored(self):
        # спроба додати дублікат фільму ігнорується
        initial_count = len(self.manager.get_all_movies())
        duplicate_movie = Movie("Темний лицар", 2008, "Крістофер Нолан")
        self.manager.add_movie(duplicate_movie)
        
        self.assertEqual(len(self.manager.get_all_movies()), initial_count)
        
        # в системі є ОДИН такий фільм
        results = self.manager.find_movie_by_title("Темний лицар")
        self.assertEqual(len(results), 1)
        # перевіряємо рік
        self.assertEqual(results[0].year, 2008)

    def test_04_find_movie_by_full_title(self):
        # пошук фільму за повною назвою
        results = self.manager.find_movie_by_title("темний лицар")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].title, "Темний лицар")

    def test_05_find_movies_by_keyword(self):
        # пошук фільмів за ключовим словом 'батько'
        results = self.manager.find_movie_by_title("батько")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].title, "Хрещений батько")

    def test_06_find_non_existent_movie_returns_empty(self):
        # пошук неіснуючого фільму повертає порожній список
        results = self.manager.find_movie_by_title("Неіснуючий Фільм 123")
        self.assertEqual(len(results), 0)

    def test_07_add_screening_successfully(self):
        # успішне додавання сеансу для існуючого фільму
        screening = self.manager.add_screening("Матриця", "2025-10-27 20:00", 100)
        self.assertIsNotNone(screening)
        self.assertIn(screening, self.manager.screenings)

    def test_08_add_screening_for_non_existent_movie_fails(self):
        # спроба додати сеанс для неіснуючого фільму повертає None
        screening = self.manager.add_screening("Неіснуючий Фільм 123", "2025-10-27 20:00", 100)
        self.assertIsNone(screening)

    def test_09_get_screening_by_valid_id(self):
        # пошук сеансу за існуючим ID
        screening = self.manager.add_screening("Початок", "2025-11-01 21:00", 120)
        found_screening = self.manager.get_screening_by_id(screening.screening_id)
        self.assertEqual(screening, found_screening)

    def test_10_get_screening_by_invalid_id_returns_none(self):
        # пошук сеансу за неіснуючим ID повертає None
        found_screening = self.manager.get_screening_by_id("invalid-uuid")
        self.assertIsNone(found_screening)

    def test_11_book_tickets_successfully(self):
        # успішне бронювання та зміну кількості вільних місць
        screening = self.manager.add_screening("Бійцівський клуб", "2025-11-05 22:00", 50)
        initial_seats = screening.available_seats
        booking = self.manager.book_tickets(screening.screening_id, 5)
        
        self.assertIsNotNone(booking)
        self.assertEqual(screening.available_seats, initial_seats - 5)
        self.assertIn(booking, self.manager.bookings)
        
        # поля бронювання заповнені коректно
        self.assertEqual(booking.screening_id, screening.screening_id)
        self.assertEqual(booking.num_tickets, 5)

    def test_12_book_tickets_for_non_existent_screening_fails(self):
        # бронювання на неіснуючий сеанс повертає None
        booking = self.manager.book_tickets("invalid-uuid", 5)
        self.assertIsNone(booking)

    def test_13_book_more_tickets_than_available_fails(self):
        # бронювання більшої кількості квитків, ніж є, повертає None
        screening = self.manager.add_screening("Паразити", "2025-11-10 19:30", 10)
        booking = self.manager.book_tickets(screening.screening_id, 11)
        self.assertIsNone(booking)
        self.assertEqual(screening.available_seats, 10)

    def test_14_cancel_booking_successfully(self):
        # успішне скасування бронювання та повернення місць
        screening = self.manager.add_screening("Форрест Гамп", "2025-12-01 18:00", 80)
        booking = self.manager.book_tickets(screening.screening_id, 10)
        self.assertEqual(screening.available_seats, 70)
        
        result = self.manager.cancel_booking(booking.booking_id)
        self.assertTrue(result)
        self.assertEqual(screening.available_seats, 80)
        #бронювання дійсно видалено зі списку
        self.assertNotIn(booking, self.manager.bookings)

    def test_15_cancel_non_existent_booking_fails(self):
        # скасування неіснуючого бронювання повертає False
        result = self.manager.cancel_booking("invalid-uuid")
        self.assertFalse(result)

    #пошук сеансів використовує точну відповідність назві
    def test_16_get_screenings_for_movie_requires_exact_match(self):
        self.manager.add_screening("Хрещений батько", "2025-10-28 19:00", 100)
        self.manager.add_movie(Movie("Батько", 2020, "Флоріан Зеллер"))
        self.manager.add_screening("Батько", "2025-10-28 21:00", 50)
        
        screenings = self.manager.get_screenings_for_movie("Батько")
    
        self.assertEqual(len(screenings), 1, "Помилка: Пошук сеансів не є точним (знаходить 'Хрещений батько' при пошуку 'Батько').")
        self.assertEqual(screenings[0].movie_title, "Батько")
        

    #сеанси відсортовані.
    def test_17_screenings_are_sorted_chronologically(self):
        title = "Початок"
        time1 = "2025-11-01 22:00"
        time2 = "2025-11-01 10:00"
        self.manager.add_screening(title, time1, 100)
        self.manager.add_screening(title, time2, 100)
        
        screenings = self.manager.get_screenings_for_movie(title)
        
        self.assertEqual(screenings[0].screening_time, time2, "Помилка: Сеанси не відсортовані за часом (раніший сеанс не йде першим).")

    def test_18_cancel_booking_can_result_in_negative_seats(self):
        screening = self.manager.add_screening("Темний лицар", "2025-11-20 20:00", 20)
        booking = self.manager.book_tickets(screening.screening_id, 5)

        screening.booked_seats = 0 
        
        self.manager.cancel_booking(booking.booking_id)
        
        self.assertGreaterEqual(screening.booked_seats, 0, "Помилка: Кількість заброньованих місць не може бути від'ємною після скасування.")
        
    def test_19_add_screening_is_ambiguous_for_same_titles(self):
        solaris_1972 = Movie("Соляріс", 1972, "Андрій Тарковський")
        solaris_2002 = Movie("Соляріс", 2002, "Стівен Содерберг")
        self.manager.add_movie(solaris_1972)
        self.manager.add_movie(solaris_2002)
    
        screening = self.manager.add_screening("Соляріс", "2025-12-25 19:00", 50)

        self.assertIsNone(screening, "Помилка: Додавання сеансу для фільмів з однаковою назвою має бути неможливим (або вимагати ID фільму).")

    def test_20_time_is_string_not_datetime(self):
        # система обробляє невалідний формат часу
        screening = self.manager.add_screening("Матриця", "це не дата", 100)
        
        #  система має валідувати час і повернути None
        self.assertIsNone(screening, "Помилка: Система не повинна дозволяти створювати сеанси з некоректним форматом часу.")
        

    def test_21_booking_with_non_integer_crashes(self):
        screening = self.manager.add_screening("Паразити", "2025-11-30 21:00", 100)
        try:
            result = self.manager.book_tickets(screening.screening_id, "два")
            self.assertIsNone(result, "Помилка: Бронювання нецілого числа квитків має повертати None.")
        except TypeError:
            self.fail("Помилка: Функція впала з TypeError замість коректної обробки невірних даних.")
        except Exception as e:
             self.fail(f"Помилка: Виникла неочікувана помилка {type(e).__name__} замість коректної обробки.")

if __name__ == '__main__':
    unittest.main()