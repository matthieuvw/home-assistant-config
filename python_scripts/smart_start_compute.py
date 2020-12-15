
time_entity_id = data.get("time_entity_id")
computed_time_entity_id = data.get("computed_time_entity_id")
temperature_entity_id = data.get('external_temperature_entity_id')

def compute_time_offset(delta_temperature):
    tmp = delta_temperature
    if delta_temperature <= 5:
        return 30
    elif delta_temperature >= 25:
        return 60 * 4
    return tmp * 6 + (tmp - 10) * 6


if time_entity_id and temperature_entity_id:

    time_entity_state_value = hass.states.get(time_entity_id).state

    if time_entity_state_value:

        # set default value for computed time
        service_data = {"entity_id": computed_time_entity_id, "time": time_entity_state_value}

        external_temperature_state_value = hass.states.get(temperature_entity_id).state

        if external_temperature_state_value:

            external_temperature = float(str(external_temperature_state_value))

            time_offset = compute_time_offset(21 - external_temperature)

            logger.info(f'time_offset=${time_offset}')

            if time_offset > 0:
                new_time_in_minutes = int(time_entity_state_value[0:2]) * 60 + int(time_entity_state_value[3:5]) - time_offset
                new_time_hours = int(new_time_in_minutes // 60)
                if new_time_hours < 0:
                    new_time_hours = 0
                new_time_minutes = int(new_time_in_minutes % 60)
                service_data = {"entity_id": computed_time_entity_id, "time": str(new_time_hours) + ':' + str(new_time_minutes)}

        else:

            logger.warn(f'Can not find state for entity {temperature_entity_id}')
    
        hass.services.call("input_datetime", "set_datetime", service_data, False)

    else:

        logger.warn(f'Can not find state for entity {time_entity_id}')
