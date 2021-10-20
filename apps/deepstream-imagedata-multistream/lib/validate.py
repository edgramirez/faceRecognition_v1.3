import lib.common as com

SOURCE_PATTERNS = ('file:///', 'rtsp://')
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


def validate_sources(data):
    '''
    Validate the configuration source recovered from server contains correct values
    '''
    for dictionary in data:
        pattern_not_found = True
        i = 0
        for pattern in SOURCE_PATTERNS:
            if dictionary['source'][0:len(pattern)] == pattern:
                if i == 0 and com.file_exists(dictionary['source']):
                    com.log_error("Configuration error - Source file: {}, does not exist: {}".format(dictionary['source']))
                pattern_not_found = False
                break
            i += 1
        if pattern_not_found:
            com.log_error("Configuration error - Source value must start with any of this patterns: {}, Current value: {}".format(SOURCE_PATTERNS, dictionary['source']))

    com.log_debug('All source values are correct')
    return True


def check_service_against_definition(data):
    if not isinstance(data, list):
        com.log_error("Configuration error - data must be a list of dictionaries - type: {} / content: {}".format(type(data), data))

    for dictionary in data:
        com.log_debug("Validating config of service: '--{}--' against the definition".format(dictionary['serviceType']))
        check_obligatory_keys(dictionary, SERVICE_DEFINITION[dictionary['serviceType']])
        check_optional_keys(dictionary, SERVICE_DEFINITION[dictionary['serviceType']])

    return True


def check_obligatory_keys(data, service_definition):
    '''
    Validate the configuration recovered from server provided the defined minimum parameters and their values are valid
    '''
    for item in service_definition['obligaroty'].keys():
        if item not in data.keys():
            com.log_error("Configuration error - Missing Obligatory parameter: {}".format(item))
        if str(type(data[item])).split("'")[1] != service_definition['obligaroty'][item]:
            com.log_error("Configuration error - Parameter '{}' value must be type : {}, Current value: {}".format(item, service_definition['obligaroty'][item], str(type(data[item])).split("'")[1]))
    com.log_debug("All obligatory parameters are OK")
    return True


def check_optional_keys(data, service_definition):
    '''
    Validate the optional configuration recovered from server and its values
    '''
    for item in service_definition['optional'].keys():
        if item in data.keys() and str(type(data[item])).split("'")[1] != service_definition['optional'][item]:
                com.log_error("      Configuration error - Parameter '{}' value must be type : {}, Current value: {}".format(item, service_definition['optional'][item], str(type(data[item])).split("'")[1]))

    com.log_debug("All optional parameters are OK")
    return True


def validate_service_exits(data):
    for element in data:
        com.log_debug('Checking service: "{}" exists'.format(element['serviceType']))
        if element['serviceType'] not in AVAILABLE_SERVICES:
            com.log_error("Configuration error - Requested service: {} - Available services: {}".format(element['serviceType'], AVAILABLE_SERVICES))
    return True


def get_config_filtered_by_active_service(config_data):
    active_services = []
    for key in config_data.keys():
        com.log_debug("Checking if service '{}/{}' is active".format(key, config_data[key]['serviceType']))
        if config_data[key]['enabled']:
            com.log_debug("Service '{}' enabled status: {}".format(config_data[key]['serviceType'], config_data[key]['enabled']))
            active_services.append(config_data[key])

    if len(active_services) < 1:
        com.log_error("\nConfiguration does not contain any active service for this server: \n\n{}".format(config_data))
    return active_services


def mac_address_in_config(mac_config):
    for machine_id in com.get_machine_macaddresses():
        if mac_config == machine_id:
            return True
    return False


def get_config_filtered_by_local_mac(config_data):
    services_data = {}
    for key in config_data.keys():
        if mac_address_in_config(key):
            return config_data[key]
    com.log_error("The provided configuration does not match any of server interfaces mac address")


def parse_parameters_and_values_from_config(config_data):
    # filter config and get only data for this server using the mac to match
    scfg = get_config_filtered_by_local_mac(config_data)

    # filter config and get only data of active services
    scfg = get_config_filtered_by_active_service(scfg)

    # validate requested services exists in code
    validate_service_exits(scfg)

    # Check all obligatory and optional parameters and values types provided by the dashboard config
    check_service_against_definition(scfg)

    # Check all source values to ensure they are correct and in the case of files they actually exists
    validate_sources(scfg)
    return scfg

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
