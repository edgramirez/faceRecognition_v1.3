#!/usr/bin/python3
import sys
import lib.common as com

param_length = len(sys.argv)
home_dir = com.HOMEDIR

msg = 'Usage: ' + sys.argv[0] + ' newBlackList | newWhiteList | addToBlackList | addToWhiteList | remoteBlackList | removeWhiteList '

if param_length < 2:
    com.log_error(msg)

if sys.argv[1] == 'newBlackList':
    if param_length == 2:
        known_faces = 'data/black_list'
        data_file = home_dir + '/BlackList.dat'
    else:
        com.log_error(msg)

    import lib.biblioteca as biblio 
    com.create_data_dir()
    biblio.encode_known_faces_from_images_in_dir(known_faces, data_file, 'blacklist')
elif sys.argv[1] == 'newWhiteList':
    if param_length == 2:
        known_faces = 'data/white_list'
        data_file = home_dir + '/WhiteList.dat'
    else:
        com.log_error(msg)

    import lib.biblioteca as biblio 
    com.create_data_dir()
    biblio.encode_known_faces_from_images_in_dir(known_faces, data_file, 'whitelist')
else:
    com.log_error(msg)
