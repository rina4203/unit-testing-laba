# main.py
from movie_manager import CinemaManager, Movie

def print_movies(movies: list[Movie]):
    """Друкує список фільмів у гарному форматі."""
    if not movies:
        print("Фільмів не знайдено.")
        return
    for movie in movies:
        print(f"  - '{movie.title}' ({movie.year}), реж. {movie.director}, "
              f"рейтинг: {movie.rating}, жанри: {', '.join(movie.genres)}")

def main():
    """Головна функція для запуску консольного інтерфейсу."""
    cinema = CinemaManager()
    print("Ласкаво просимо до системи управління кінотеатром!")

    while True:
        print("\n--- ГОЛОВНЕ МЕНЮ ---")
        print("1. Переглянути всі фільми")
        print("2. Знайти фільм за назвою")
        print("3. Переглянути сеанси для фільму")
        print("4. Додати сеанс")
        print("5. Забронювати квитки")
        print("6. Переглянути мої бронювання")
        print("7. Скасувати бронювання")
        print("0. Вийти")
        
        choice = input("Ваш вибір: ")

        if choice == '1':
            print("\n--- Список усіх фільмів ---")
            all_movies = cinema.get_all_movies()
            print_movies(all_movies)

        elif choice == '2':
            title = input("Введіть назву для пошуку: ")
            found_movies = cinema.find_movie_by_title(title)
            print(f"\n--- Результати пошуку для '{title}' ---")
            print_movies(found_movies)

        elif choice == '3':
            title = input("Введіть назву фільму для перегляду сеансів: ")
            screenings = cinema.get_screenings_for_movie(title)
            print(f"\n--- Доступні сеанси для '{title}' ---")
            if not screenings:
                print("Наразі сеансів для цього фільму немає.")
            else:
                for s in screenings:
                    print(f"  - ID: {s.screening_id}")
                    print(f"    Час: {s.screening_time}")
                    print(f"    Вільних місць: {s.available_seats} з {s.total_seats}")

        elif choice == '4':
            print("\n--- Додавання нового сеансу ---")
            title = input("Введіть точну назву фільму: ")
            time = input("Введіть дату та час сеансу (напр., 2025-10-28 21:00): ")
            try:
                seats = int(input("Введіть загальну кількість місць: "))
                new_screening = cinema.add_screening(title, time, seats)
                if new_screening:
                    print(f"Сеанс для '{title}' успішно додано! ID: {new_screening.screening_id}")
                else:
                    print(f"Помилка: Фільм з назвою '{title}' не знайдено в базі.")
            except ValueError:
                print("Помилка: Кількість місць має бути числом.")

        elif choice == '5':
            print("\n--- Бронювання квитків ---")
            screening_id = input("Введіть ID сеансу: ")
            try:
                tickets = int(input("Скільки квитків забронювати? "))
                booking = cinema.book_tickets(screening_id, tickets)
                if booking:
                    print("\nКвитки успішно заброньовано!")
                    print(f"  Фільм: {booking.movie_title}")
                    print(f"  Кількість: {booking.num_tickets}")
                    print(f"  Ваш ID бронювання: {booking.booking_id}")
                else:
                    print("Помилка бронювання. Перевірте ID сеансу та кількість вільних місць.")
            except ValueError:
                print("Помилка: Кількість квитків має бути числом.")

        elif choice == '6':
            print("\n--- Ваші бронювання ---")
            if not cinema.bookings:
                print("У вас ще немає активних бронювань.")
            else:
                for b in cinema.bookings:
                    print(f"  - ID бронювання: {b.booking_id}")
                    print(f"    Фільм: {b.movie_title}")
                    print(f"    Квитків: {b.num_tickets}")
                    print(f"    ID сеансу: {b.screening_id}")
        
        elif choice == '7':
            booking_id = input("Введіть ID бронювання для скасування: ")
            if cinema.cancel_booking(booking_id):
                print(f"Бронювання {booking_id} успішно скасовано.")
            else:
                print("Помилка: Бронювання з таким ID не знайдено.")

        elif choice == '0':
            print("Дякуємо за використання системи! До побачення.")
            break
        
        else:
            print("Невірний вибір. Спробуйте ще раз.")

if __name__ == "__main__":
    main()

