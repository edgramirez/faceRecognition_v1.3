import lib.common as com


def check_config_keys_exist(config_dictionary):
    joint_elements = []
    for item in com.SERVICE_DEFINITION[config_dictionary['serviceType']]:
        for elem in com.SERVICE_DEFINITION[config_dictionary['serviceType']][item].keys():
            joint_elements.append(elem)
    for item in config_dictionary:
        if item != 'serviceType':
            if item not in joint_elements:
                com.log_error("Configuration error - Pameter: {}, does not exist in the service definition:".format(item))


def validate_sources(data):
    '''
    Validate the configuration source recovered from server contains correct values
    '''
    for camera_service_id in data:
        pattern_not_found = True
        for pattern in com.SOURCE_PATTERNS:
            if data[camera_service_id]['source'][0:len(pattern)] == pattern:
                if data[camera_service_id]['source'][:7] == 'file://' and com.file_exists(data[camera_service_id]['source'][7:]) is False:
                    com.log_error("Configuration error - Source file: {}, does not exist".format(data[camera_service_id]['source'][7:]))
                pattern_not_found = False
                break
        if pattern_not_found:
            com.log_error("Configuration error - Source value must start with any of this patterns: {}, Current value: {}".format(com.SOURCE_PATTERNS, data[camera_service_id]['source']))

    com.log_debug('All source values are correct')
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


def check_service_against_definition(data):
    if not isinstance(data, dict):
        com.log_error("Configuration error - data must be a list of dictionaries - type: {} / content: {}".format(type(data), data))

    for dictionary in data.keys():
        com.log_debug("Validating config of service: '--{} / {}--' against the definition".format(dictionary, data[dictionary]['serviceType']))
        for parameters in data[dictionary]:
            check_config_keys_exist(data[dictionary])
        check_obligatory_keys(data[dictionary], com.SERVICE_DEFINITION[data[dictionary]['serviceType']])
        check_optional_keys(data[dictionary], com.SERVICE_DEFINITION[data[dictionary]['serviceType']])
    return True


def validate_service_exists(data):
    service_list = com.SERVICE_DEFINITION.keys()
    for camera_service_id in data.keys():
        if data[camera_service_id]['serviceType'] not in service_list:
            com.log_error("Configuration error - Requested service: {} - Available services: {}".format(service_parameter, service_list))
    return True


def get_config_filtered_by_active_service(config_data):
    if not isinstance(config_data, dict):
        com.log_error("Configuration error - Config data must be a dictionary - type: {} / content: {}".format(type(config_data), config_data))
    active_services = {}
    for key in config_data.keys():
        # This variable will be incremented if the service name key already exists
        service_consecutive = 0 
        for inner_key in config_data[key]:
            if config_data[key][inner_key]['enabled']:

                new_key_name = key + "_" + inner_key + "_" + config_data[key][inner_key]['serviceType'] + "_" + str(service_consecutive)
                if len(active_services) > 0 and new_key_name in active_services:
                    service_consecutive += 1
                    new_key_name = key + "_" + inner_key + "_" + config_data[key][inner_key]['serviceType'] + "_" + str(service_consecutive)

                active_services[new_key_name] = config_data[key][inner_key]
                com.log_debug("Service type '{}' of Service '{}' enabled value is: {}".
                    format(config_data[key][inner_key]['serviceType'], inner_key, config_data[key][inner_key]['enabled']))

    if len(active_services) < 1:
        com.log_error("\nConfiguration does not contain any active service for this server: \n\n{}".format(config_data))

    return active_services


def mac_address_in_config(mac_config):
    for machine_id in com.get_machine_macaddresses():
        if mac_config == machine_id:
            return True
    return False


def get_config_filtered_by_local_mac(config_data):
    '''
    By now we only support one nano server and one interface 
    but it can be a big server with multiple interfaces so I 
    leave the logic with to handle this option
    '''
    services_data = {}
    for key in config_data.keys():
        if mac_address_in_config(key):
            services_data[key] = config_data[key]
    if services_data:
        return services_data

    com.log_error("The provided configuration does not match any of server interfaces mac address")


def parse_parameters_and_values_from_config(config_data):
    # filter config and get only data for this server using the mac to match
    scfg = get_config_filtered_by_local_mac(config_data)

    # filter config and get only data of active services
    scfg = get_config_filtered_by_active_service(scfg)

    # validate requested services exists in code
    validate_service_exists(scfg)

    # Check all obligatory and optional parameters and values types provided by the dashboard config
    check_service_against_definition(scfg)

    # Check all source values to ensure they are correct and in the case of files they actually exists
    validate_sources(scfg)

    return scfg

