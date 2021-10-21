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
        },
        "blackList": {
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
        },
        "whiteList": {
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
        },
        "recurrence": {
            'obligaroty': {
                'enabled':      'bool',
                'source':       'str',
                'faceDbFile':   'str'
                },
            'optional': {
                'ignorePreviousDb': 'bool',
                }
        },
        "gender": {
            'obligaroty': {
                'enabled':      'bool',
                'source':       'str',
                'faceDbFile':   'str'
                },
            'optional': {
                'ignorePreviousDb': 'bool',
                'saveFacesDb':      'bool'
                }
        }
    }


def check_config_keys_exist(config_dictionary):
    joint_elements = []
    for item in SERVICE_DEFINITION[config_dictionary['serviceType']]:
        for elem in SERVICE_DEFINITION[config_dictionary['serviceType']][item].keys():
            joint_elements.append(elem)
    for item in config_dictionary:
        if item != 'serviceType':
            if item not in joint_elements:
                com.log_error("Configuration error - Pameter: {}, does not exist in the service definition:".format(item))


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
        check_config_keys_exist(dictionary)
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
                com.log_error("Configuration error - Parameter '{}' value must be type : {}, Current value: {}".format(item, service_definition['optional'][item], str(type(data[item])).split("'")[1]))

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

