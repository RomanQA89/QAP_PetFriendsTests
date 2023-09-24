from api import PetFriends
from settings import valid_email, valid_password, unvalid_email, unvalid_password

pf = PetFriends()

                             # Позитивные тесты.


def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """ Проверяем что запрос api ключа возвращает статус 200 и в результате содержится слово key"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 200
    assert 'key' in result


def test_get_all_pets_with_valid_key(filter=''):
    """ Проверяем что запрос всех питомцев возвращает не пустой список.
    Для этого сначала получаем api ключ и сохраняем в переменную auth_key. Далее используя этого ключ
    запрашиваем список всех питомцев и проверяем что список не пустой.
    Доступное значение параметра filter - 'my_pets' либо '' """

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 200
    assert len(result['pets']) > 0


def test_add_new_pet_with_valid_data(name='Барбос', animal_type='терьер',
                                     age='49', pet_photo='images/cat1.jpg'):
    """Проверяем что можно добавить питомца с корректными данными"""

    # Запрашиваем ключ api и сохраняем в переменную auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name


def test_successful_delete_self_pet():
    """Проверяем возможность удаления питомца"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Суперкот", "кот", "3", "images/cat1.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
    assert status == 200
    assert pet_id not in my_pets.values()


def test_successful_update_self_pet_info(name='игорь', animal_type='кот', age=7):
    """Проверяем возможность обновления информации о питомце"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Если список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 200
        assert result['name'] == name
    else:
        # если список питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")


def test_add_new_pet_with_valid_data_without_photo(name='Jeronimo', animal_type='supermen',
                                     age='77'):
    """Проверяем что можно добавить питомца без фото с корректными данными"""

    # Запрашиваем ключ api и сохраняем в переменную auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name


def test_success_add_photo_of_pet(pet_photo='images/P1040103.jpg'):
    """Проверяем что можно успешно добавить фото питомца"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Если список своих питомцев не пустой, то отправляем данные серверу
    if len(my_pets['pets']) > 0:
        pet_id = my_pets['pets'][0]['id']
        status, result = pf.add_photo_of_pet(auth_key, pet_id, pet_photo)

        # Проверяем что статус ответа равен 200 и в списке питомцев есть питомец с обновленным фото
        assert status == 200
        assert result['pet_photo'] == pet_photo
    else:
        raise Exception("There is no my pets")


                             # Негативные тесты.


def test_get_api_key_with_unvalid_email(email=unvalid_email, password=valid_password):
    """Проверяем что запрос api ключа с невалидным email возвращает статус 403"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 403


def test_get_api_key_with_unvalid_password(email=valid_email, password=unvalid_password):
    """Проверяем что запрос api ключа с невалидным паролем возвращает статус 403"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 403


def test_add_new_pet_with_unvalid_auth_key_without_photo(name='Tom', animal_type='dog',
                                     age='5'):
    """Проверяем добавление питомца без фото с некорректным auth_key на 403 статус"""

    # Запрашиваем ключ api и сохраняем в переменную auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet_without_photo_with_unvalid_auth_key(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 403


def test_add_new_pet_without_photo_with_unvalid_name(name='MjIeBfj0TO7blscy5xZGbwahNOEVAcxkp37H98fHKoZJYnyErUJLimvC5Z6M0h4j34UkgDb0j9pOdITkGneP4S2uZP7NY5xqThxQbs4pMFhSt92qRDHhBYAGNuLvQfPLfwfkoFrO452M5OYtssJcpWJCbKDtUqXaWYFxwXcLt4uYYLMffuKeVtcbrR7oXG9s6QMpOEtBGgwziqEU3f1fr5XdEkAo0Nx6YoDejoBSTzSQIRkxffWh25u6yWC3Oyfr', animal_type='',
                                     age='6'):
    """Проверяем добавление питомца без фото с именем в 256 символов на 400 статус"""
    """Баг не воспроизводится так как нет ограничений на вводимые данные!"""

    # Запрашиваем ключ api и сохраняем в переменную auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 400


def test_add_new_pet_without_photo_with_unvalid_animal_type(name='Том', animal_type='MjIeBfj0TO7blscy5xZGbwahNOEVAcxkp37H98fHKoZJYnyErUJLimvC5Z6M0h4j34UkgDb0j9pOdITkGneP4S2uZP7NY5xqThxQbs4pMFhSt92qRDHhBYAGNuLvQfPLfwfkoFrO452M5OYtssJcpWJCbKDtUqXaWYFxwXcLt4uYYLMffuKeVtcbrR7oXG9s6QMpOEtBGgwziqEU3f1fr5XdEkAo0Nx6YoDejoBSTzSQIRkxffWh25u6yWC3Oyfr',
                                     age='6'):
    """Проверяем добавление питомца без фото с animal_type в 256 символов на 400 статус"""
    """Баг не воспроизводится так как нет ограничений на вводимые данные!"""

    # Запрашиваем ключ api и сохраняем в переменную auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 400


def test_add_new_pet_without_photo_with_unvalid_age(name='Том', animal_type='кот',
                                     age='-68689676'):
    """Проверяем добавление питомца без фото с отрицательным возрастом на 400 статус"""
    """Баг не воспроизводится так как нет ограничений на вводимые данные!"""

    # Запрашиваем ключ api и сохраняем в переменную auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 400


def test_unsuccessful_get_all_pets(filter=''):
    """ Проверяем что запрос всех питомцев с невалидным ключом будет иметь 403 статус."""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets_with_unvalid_auth_key(auth_key, filter)

    assert status == 403


def test_unsuccessful_add_new_pet(name='Bil', animal_type='hen',
                                     age='9', pet_photo='images/cat1.jpg'):

    """Проверяем добавление питомца с невалидным ключом на 403 статус"""

    # Запрашиваем ключ api и сохраняем в переменную auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet_with_incorrect_auth_key(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 403


def test_unsuccessful_add_photo_of_pet(pet_photo='images/P1040103.jpg'):
    """Проверка на 403 статус при добавлении фото питомца с невалидным ключом"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Если список своих питомцев не пустой, то отправляем данные серверу
    if len(my_pets['pets']) > 0:
        pet_id = my_pets['pets'][0]['id']
        status, result = pf.add_photo_of_pet_with_unvalid_auth_key(auth_key, pet_id, pet_photo)

        # Проверяем что статус ответа равен 403
        assert status == 403


def test_unsuccessful_delete_self_pet_():
    """Проверка на 403 статус при невозможности удаления питомца"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Суперкот", "кот", "2", "images/cat1.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet_with_unvalid_auth_key(auth_key, pet_id)

    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем что статус ответа равен 403
    assert status == 403
