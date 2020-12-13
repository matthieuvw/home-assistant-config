
time_entity_id = data.get("time_entity_id")
temperature_entity_id = data.get('temperature_entity_id')

def compute_time_offset(delta_temperature):

    tmp = delta_temperature

    if delta_temperature <= 5:
        return 30
    elif delta_temperature >= 25:
        return 60 * 4

    return tmp * 6 + (tmp - 10) * 6

if time_entity_id and temperature_entity_id:

    logger.info('time_entity_id=%s', time_entity_id)
    logger.info('temperature_entity_id=%s', temperature_entity_id)

    current_time_value = hass.states.get(time_entity_id).state
    temperature = float(str(hass.states.get(temperature_entity_id).state))

    logger.info('current time=%s', current_time_value)
    logger.info('temperature=%s', temperature)

    time_offset = compute_time_offset(21 - temperature)

    if time_offset > 0:
        new_time_in_minutes = int(current_time_value[0:2]) * 60 + int(current_time_value[3:5]) - time_offset
        new_time_hours = int(new_time_in_minutes // 60)
        if new_time_hours < 0:
            new_time_hours = 0
        new_time_minutes = int(new_time_in_minutes % 60)
        service_data = {"entity_id": time_entity_id, "time": str(new_time_hours) + ':' + str(new_time_minutes)}
        hass.services.call("input_datetime", "set_datetime", service_data, False)

