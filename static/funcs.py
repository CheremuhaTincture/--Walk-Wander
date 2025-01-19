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