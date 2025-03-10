def decode(number):
    even = [2, 3, 5, 7, 11, 13, 17]
    result = [0, 1]

    for i in even:
        if number % i == 0:
            result.append(i)

    return result

def own(subject, list):
    try:
        for element in list:
            if subject == element:
                return True
        return False
    except Exception:
        print(f'error in own function')

def map_name(id):
    maps = {
        1 : 'Средневековье',
        2 : 'Древний Египет'
    }

    return maps[id]

def map_size(id):
    map_size = {
        0 : 'маленькая',
        1 : 'средняя',
        2 : 'большая'
    }

    return map_size[id]

def game_status(status):
    statuses = {
        'created' : 'создана',
        'started' : 'началась'
    }

    return statuses[status]