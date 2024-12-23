from accuweather import *
from weather_check import *

def report_for_city(number, mode, name, api_key):
    key = get_location_key_name(api_key, name)[0]

    current = get_conditions_by_key(api_key, key)
    forecast = get_forecast(api_key, key)

    is_ok, reasons = weather_check(current, mode)

    reasons_key = {
        'temperature': 'температуры',
        'humidity': 'влажности',
        'wind_speed': 'скорости ветра',
        'precipitation_probability': 'вероятности осадков'
    }

    ans = f'Погода для {number} города - {name}:\n\n'
    ans += {True: 'Текущая погода вам подходит', False: 'Текущая погода вам неподходит из-за: '}[is_ok] + ', '.join(list(map(lambda x: reasons_key[x], reasons))) + '\n'
    ans += f'Прогноз погоды на 5 дней:\n\n'

    for day in forecast:
        ans += f"Дата: {day['date'].split('T')[0]}\n"
        ans += f"Макс. температура: {day['max_temp']} °C\n"
        ans += f"Мин. температура: {day['min_temp']} °C\n"
        ans += f"Вероятность осадков: {day['precipitation_probability']}%\n"
        ans += f"Скорость ветра: {day['wind_speed']} км/ч\n\n"

    return ans