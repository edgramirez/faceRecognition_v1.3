import lib.common as com

AVAILABLE_SERVICES = ('find', 'blackList', 'whiteList', 'recurrence', 'ageAndGender')
SERVICE_DEFINITION = {
        "find": {
            'obligaroty': {
                'enabled':      'bool',
                'source':       'str',
                'faceDbFile':   'str'
                },
            'optional': {
                'checkBlackList':   'bool',
                'checkWhieteList':  'bool',
                'ignorePreviousDb': 'bool',
                'saveFacesDb':      'bool'
                }
        }
    }


def mac_address_in_config(mac_config):
    for machine_id in com.get_machine_macaddresses():
        if mac_config == machine_id: 
            return True
    return False

def check_service_keys(data):
    if not isinstance(data, dict):
        com.log_error("Configuration error - data must be a dictionary - type: {} / content: {}".format(type(data), data))

    # double validation config is for this mathine
    config_content = {}
    for key in data.keys():
        if mac_address_in_config(key):
            config_content = data[key]
            break

    if len(config_content) == 0:
        com.log_error("The provided configuration does not match this server")

    # check all requested services provided by the configuration are actually offered by AVAILABLE_SERVICES
    for service_name in config_content.keys():
        if service_name not in AVAILABLE_SERVICES:
            com.log_error("Configuration error - Requested service: {} / available services: {}".format(type(service_name), AVAILABLE_SERVICES))

    # check the keys and its values match the coded definition in "SERVICE_DEFINITION"
    for item in config_content.keys():
        com.log_debug("Validating config of service: '--{}--' against the definition".format(item))
        check_obligatory_keys(config_content[item], SERVICE_DEFINITION[item])
        check_optional_keys(config_content[item], SERVICE_DEFINITION[item])

    quit()
    return True


def check_obligatory_keys(data, service_definition):
    for item in service_definition['obligaroty'].keys():
        if item not in data.keys():
            com.log_error("      Configuration error - Missing Obligatory parameter: {}".format(item))
        if str(type(data[item])).split("'")[1] != service_definition['obligaroty'][item]:
            com.log_error("      Configuration error - Parameter '{}' value must be type : {}, Current value: {}".format(item, service_definition['obligaroty'][item], str(type(data[item])).split("'")[1]))
    com.log_debug("      All obligatory parameters are OK")
    return True


def check_optional_keys(data, service_definition):
    for item in service_definition['optional'].keys():
        if item in data.keys() and str(type(data[item])).split("'")[1] != service_definition['optional'][item]:
                com.log_error("      Configuration error - Parameter '{}' value must be type : {}, Current value: {}".format(item, service_definition['optional'][item], str(type(data[item])).split("'")[1]))

    com.log_debug("      All optional parameters are OK")
    return True


def validate_find(data):
    check_service_keys(data)

    #optional_config_keys = ['checkBlackList', 'checkWhieteList', 'ignorePreviousDb', 'saveFacesDb']
    #check_optional_keys(data, optional_config_keys)
    quit()

    if 'enabled' not in data.keys():
        com.error_msg('Key element enabled does not exists in the data provided:\n\n {}'.format(data))
    else:
        if not isinstance(data['enabled'], str):
            com.error_msg("'aforo_data' parameter, most be True or False, current value: {}".format(data['enabled']))

    if 'reference_line_coordinates' in data.keys():
        reference_line_coordinates = data['reference_line_coordinates']
        reference_line_coordinates = reference_line_coordinates.replace('(', '')
        reference_line_coordinates = reference_line_coordinates.replace(')', '')
        reference_line_coordinates = reference_line_coordinates.replace(' ', '')
        reference_line_coordinates = reference_line_coordinates.split(',')
        try:
            reference_line_coordinates = [(int(reference_line_coordinates[0]), int(reference_line_coordinates[1])), (int(reference_line_coordinates[2]), int(reference_line_coordinates[3]))]
            data.update({'reference_line_coordinates': reference_line_coordinates})
        except Exception as e:
            com.error_msg("Exception: Unable to create reference_line_coordinates".format(str(e)))

        if not isinstance(data['reference_line_coordinates'], list):
            com.error_msg("reference_line_coordinate, most be a list. Undefining variable")

        if len(data['reference_line_coordinates']) != 2:
            com.error_msg("coordinates, most be a pair of values.")

        for coordinate in data['reference_line_coordinates']:
            if not isinstance(coordinate[0], int) or not isinstance(coordinate[1], int):
                com.error_msg("coordinates elements, most be integers")

        if 'reference_line_width' not in data.keys():
            data.update({'reference_line_width': 2})
        else:
            new_value = float(data['reference_line_width'])
            new_value = int(new_value)
            data.update({'reference_line_width': new_value})

        if 'reference_line_color' not in data.keys():
            data.update({'reference_line_color': [1, 1, 1, 1]})
        else:
            reference_line_color = reference_line_color.replace('(', '')
            reference_line_color = reference_line_color.replace(')', '')
            reference_line_color = reference_line_color.replace(' ', '')
            reference_line_color = reference_line_color.split(',')
            try:
                reference_line_color = [int(reference_line_color[0]), int(reference_line_color[1]), int(reference_line_color[2]), int(reference_line_color[3])]
                data.update({'reference_line_color': reference_line_color})
            except Exception as e:
                com.error_msg("Exception: Unable to create reference_line_color".format(str(e)))

        if not isinstance(data['reference_line_color'], list):
            com.error_msg("coordinates color elements, most be a list of integers")

        for color in data['reference_line_color']:
            if not isinstance(color, int) or color < 0 or color > 255:
                com.error_msg("color values should be integers and within 0-255")

        if 'reference_line_outside_area' not in data.keys():
            com.error_msg("If reference line is define 'outside_area' must also be defined")
        else:
            reference_line_outside_area = float(data['reference_line_outside_area'])
            reference_line_outside_area = int(reference_line_outside_area)
            if reference_line_outside_area not in [1, 2]:
                com.error_msg("outside_area, most be an integer 1 or 2")
            data.update({'reference_line_outside_area': reference_line_outside_area})

    if 'area_of_interest' in data.keys() and data['area_of_interest'] != '':
        if 'area_of_interest_type' not in data.keys():
            com.error_msg("Missing 'type' in 'area_of_interest' object")

        if data['area_of_interest_type'] not in ['horizontal', 'parallel', 'fixed']:
            com.error_msg("'type' object value must be 'horizontal', 'parallel' or 'fixed'")

        UpDownLeftRight = data['area_of_interest'].replace(' ', '')
        UpDownLeftRight = UpDownLeftRight.split(',')
        try:
            data.update({'area_of_interest': {'up': int(UpDownLeftRight[0]), 'down': int(UpDownLeftRight[1]), 'left': int(UpDownLeftRight[2]), 'right': int(UpDownLeftRight[3])} }) 
        except Exception as e:
            com.error_msg("Exception: Unable to get the up, down, left and right values... Original exception: ".format(str(e)))

        if data['area_of_interest_type'] == 'horizontal':
            horizontal_keys = ['up', 'down', 'left', 'right']
            for param in horizontal_keys:
                if param not in data['area_of_interest'].keys():
                    com.error_msg("Missing '{}' parameter in 'area_of_interest' object".format(param))
        
                if not isinstance(data['area_of_interest'][param], int) or data['area_of_interest'][param] < 0:
                    com.error_msg("{} value should be integer and positive".format(params))
        elif data['area_of_interest_type'] == 'parallel':
            print('type parallel not defined')
        elif data['area_of_interest_type'] == 'fixed':
            inner_keys = ['topx', 'topy', 'height', 'width']
            for param in inner_keys:
                if param not in data['area_of_interest'].keys():
                    com.error_msg("Missing '{}' parameter in 'area_of_interest' object".format(param))
                if not isinstance(data['area_of_interest'][param], int) or data['area_of_interest'][param] < 0:
                    com.error_msg("{} value should be integer and positive".format(params))
        
    if 'area_of_interest' in data.keys() and 'reference_line_coordinates' in data.keys() and data['area_of_interest_type'] == 'fixed':
        com.error_msg("Incompatible parameters....  reference_line is not needed when having an area_of_interest type fixed")

    return data
