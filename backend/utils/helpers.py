from datetime import datetime, date

def calculate_age(birth_date):
    if isinstance(birth_date, str):
        birth_date = datetime.strptime(birth_date, '%Y-%m-%d').date()
    today = date.today()
    return today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))

def calculate_percentage(obtained, total):
    if total == 0:
        return 0
    return round((obtained / total) * 100, 2)
