def weather_check(conditions, mode='center'):
    """
        weather_check возвращает True если погода благоприятна для mode и False если неблагоприятна

        conditions: dict - {text_conditions, temperature, humidity, wind_speed, precipitation_probability}
        mode: str - 'south', 'center', 'north' (режим оценки погоды для разных типов людей)
        (south для препочитающих тепло, center для препочитающих средние температуры, north для препочитающих холод)
        return: bool, list (причины неблагоприятной погоды)
    """

    result = True
    reasons = []

    if mode == 'south':
        if conditions['temperature'] < 0 or conditions['temperature'] > 40:
            result = False
            reasons += ['temperature']
        if conditions['humidity'] > 90:
            result = False
            reasons += ['humidity']
        if conditions['wind_speed'] > 50:
            result = False
            reasons += ['wind_speed']
        if conditions['precipitation_probability'] > 80:
            result = False
            reasons += ['precipitation_probability']
    elif mode == 'center':
        if conditions['temperature'] < -20 or conditions['temperature'] > 35:
            result = False
            reasons += ['temperature']
        if conditions['humidity'] > 80:
            result = False
            reasons += ['humidity']
        if conditions['wind_speed'] > 50:
            result = False
            reasons += ['wind_speed']
        if conditions['precipitation_probability'] > 80:
            result = False
            reasons += ['precipitation_probability']
    elif mode == 'north':
        if conditions['temperature'] < -30 or conditions['temperature'] > 26:
            result = False
            reasons += ['temperature']
        if conditions['humidity'] > 70:
            result = False
            reasons += ['humidity']
        if conditions['wind_speed'] > 20:
            result = False
            reasons += ['wind_speed']
        if conditions['precipitation_probability'] > 80:
            result = False
            reasons += ['precipitation_probability']
    else:
        raise ValueError('Нет такого mode')

    return result, tuple(reasons)
