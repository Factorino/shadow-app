from src.models.user import User
from src.repositories.user_repository import UserRepository
from src.services.user_service import UserService
from src.services.auth_service import AuthService
from src.database import Database

# Инициализация зависимостей
def setup_services():
    # Создаем базу данных (в реальном приложении здесь была бы настоящая БД)
    database = Database()

    # Создаем репозиторий и сервисы
    user_repository = UserRepository(database)
    user_service = UserService(user_repository)
    auth_service = AuthService(user_service)

    return user_service, auth_service

def demonstrate_user_service():
    print("=== ДЕМОНСТРАЦИЯ USER SERVICE ===\n")

    user_service, auth_service = setup_services()

    # 1. Создание пользователей
    print("1. СОЗДАНИЕ ПОЛЬЗОВАТЕЛЕЙ:")
    try:
        user1 = User(username="alex", password="password123")
        created_user1 = user_service.add(user1)
        print(f"   Создан пользователь: {created_user1.username} (ID: {created_user1.id})")

        user2 = User(username="maria", password="securepass456")
        created_user2 = user_service.add(user2)
        print(f"   Создан пользователь: {created_user2.username} (ID: {created_user2.id})")

        user3 = User(username="john", password="johnspass789", is_active=False)
        created_user3 = user_service.add(user3)
        print(f"   Создан пользователь: {created_user3.username} (ID: {created_user3.id}, активен: {created_user3.is_active})")

    except ValueError as e:
        print(f"   Ошибка при создании пользователя: {e}")

    print()

    # 2. Получение всех пользователей
    print("2. ВСЕ ПОЛЬЗОВАТЕЛИ:")
    all_users = user_service.get_all()
    for user in all_users:
        print(f"   - {user.username} (ID: {user.id}, активен: {user.is_active})")

    print()

    # 3. Получение пользователя по ID
    print("3. ПОИСК ПОЛЬЗОВАТЕЛЯ ПО ID:")
    try:
        user_by_id = user_service.get_by_id(created_user1.id)
        print(f"   Найден пользователь: {user_by_id.username}")
    except ValueError as e:
        print(f"   Ошибка: {e}")

    print()

    # 4. Получение пользователя по имени
    print("4. ПОИСК ПОЛЬЗОВАТЕЛЯ ПО ИМЕНИ:")
    try:
        user_by_username = user_service.get_by_username("maria")
        print(f"   Найден пользователь: {user_by_username.username} (ID: {user_by_username.id})")
    except ValueError as e:
        print(f"   Ошибка: {e}")

    print()

    # 5. Получение активных и неактивных пользователей
    print("5. ФИЛЬТРАЦИЯ ПОЛЬЗОВАТЕЛЕЙ:")
    active_users = user_service.get_active_users()
    print(f"   Активных пользователей: {len(active_users)}")

    inactive_users = user_service.get_inactive_users()
    print(f"   Неактивных пользователей: {len(inactive_users)}")

    print()

    # 6. Деактивация пользователя
    print("6. ДЕАКТИВАЦИЯ ПОЛЬЗОВАТЕЛЯ:")
    try:
        deactivated_user = user_service.deactivate_user(created_user2.id)
        print(f"   Пользователь {deactivated_user.username} деактивирован")
    except ValueError as e:
        print(f"   Ошибка: {e}")

    print()

    # 7. Смена пароля
    print("7. СМЕНА ПАРОЛЯ:")
    try:
        user_with_new_password = user_service.change_password(created_user1.id, "newpassword123")
        print(f"   Пароль пользователя {user_with_new_password.username} изменен")
    except ValueError as e:
        print(f"   Ошибка: {e}")

    print()

    # 8. Проверка активных пользователей после изменений
    print("8. АКТИВНЫЕ ПОЛЬЗОВАТЕЛИ ПОСЛЕ ИЗМЕНЕНИЙ:")
    active_users_after = user_service.get_active_users()
    for user in active_users_after:
        print(f"   - {user.username} (ID: {user.id})")

def demonstrate_auth_service():
    print("\n=== ДЕМОНСТРАЦИЯ AUTH SERVICE ===\n")

    user_service, auth_service = setup_services()

    # 1. Регистрация новых пользователей
    print("1. РЕГИСТРАЦИЯ:")
    try:
        registered_user1 = auth_service.register("testuser", "testpassword123")
        print(f"   Зарегистрирован: {registered_user1.username} (ID: {registered_user1.id})")

        registered_user2 = auth_service.register("demo", "demopassword456")
        print(f"   Зарегистрирован: {registered_user2.username} (ID: {registered_user2.id})")

    except ValueError as e:
        print(f"   Ошибка регистрации: {e}")

    print()

    # 2. Успешный логин
    print("2. УСПЕШНЫЙ ЛОГИН:")
    try:
        logged_in_user = auth_service.login("testuser", "testpassword123")
        print(f"   Успешный вход: {logged_in_user.username}")
    except ValueError as e:
        print(f"   Ошибка входа: {e}")

    print()

    # 3. Неуспешный логин (неверный пароль)
    print("3. НЕУСПЕШНЫЙ ЛОГИН (НЕВЕРНЫЙ ПАРОЛЬ):")
    try:
        auth_service.login("testuser", "wrongpassword")
    except ValueError as e:
        print(f"   Ошибка входа: {e}")

    print()

    # 4. Смена пароля через AuthService
    print("4. СМЕНА ПАРОЛЯ ЧЕРЕЗ AUTH SERVICE:")
    try:
        user_with_changed_password = auth_service.change_password(
            registered_user1.id,
            "testpassword123",
            "newsecurepassword789"
        )
        print(f"   Пароль пользователя {user_with_changed_password.username} успешно изменен")
    except ValueError as e:
        print(f"   Ошибка смены пароля: {e}")

    print()

    # 5. Проверка аутентификации
    print("5. ПРОВЕРКА АУТЕНТИФИКАЦИИ:")
    is_auth = auth_service.is_authenticated(registered_user1.id)
    print(f"   Пользователь с ID {registered_user1.id} аутентифицирован: {is_auth}")

    is_auth_invalid = auth_service.is_authenticated(999)  # Несуществующий ID
    print(f"   Пользователь с ID 999 аутентифицирован: {is_auth_invalid}")

    print()

    # 6. Получение текущего пользователя
    print("6. ПОЛУЧЕНИЕ ТЕКУЩЕГО ПОЛЬЗОВАТЕЛЯ:")
    current_user = auth_service.get_current_user(registered_user1.id)
    if current_user:
        print(f"   Текущий пользователь: {current_user.username}")
    else:
        print("   Пользователь не найден")

    non_existent_user = auth_service.get_current_user(999)
    if non_existent_user:
        print(f"   Текущий пользователь: {non_existent_user.username}")
    else:
        print("   Пользователь с ID 999 не найден")

def demonstrate_error_cases():
    print("\n=== ДЕМОНСТРАЦИЯ ОБРАБОТКИ ОШИБОК ===\n")

    user_service, auth_service = setup_services()

    # 1. Создание пользователя с некорректными данными
    print("1. СОЗДАНИЕ С НЕКОРРЕКТНЫМИ ДАННЫМИ:")
    try:
        invalid_user = User(username="ab", password="short")  # Слишком короткие данные
        user_service.add(invalid_user)
    except ValueError as e:
        print(f"   Ошибка: {e}")

    print()

    # 2. Создание пользователя с пустым именем
    print("2. СОЗДАНИЕ С ПУСТЫМ ИМЕНЕМ:")
    try:
        empty_username_user = User(username="", password="validpassword123")
        user_service.add(empty_username_user)
    except ValueError as e:
        print(f"   Ошибка: {e}")

    print()

    # 3. Поиск несуществующего пользователя
    print("3. ПОИСК НЕСУЩЕСТВУЮЩЕГО ПОЛЬЗОВАТЕЛЯ:")
    try:
        user_service.get_by_id(9999)
    except ValueError as e:
        print(f"   Ошибка: {e}")

    print()

    # 4. Логин с неверными данными
    print("4. ЛОГИН С НЕВЕРНЫМИ ДАННЫМИ:")
    try:
        auth_service.login("nonexistent", "password")
    except ValueError as e:
        print(f"   Ошибка: {e}")

if __name__ == "__main__":
    demonstrate_user_service()
    demonstrate_auth_service()
    demonstrate_error_cases()

    print("\n=== ДЕМОНСТРАЦИЯ ЗАВЕРШЕНА ===")
