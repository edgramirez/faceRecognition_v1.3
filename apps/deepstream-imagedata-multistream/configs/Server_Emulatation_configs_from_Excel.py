{ 
    "FA:KE:4b:8d:49:68" : {
        "service1": {
            "serviceType": "find",
            "source": "file:///tmp/amlo.mp4",
            "cameraId": "camera1_mac_address",
            "enabled": true,
            "generalFaceDectDbFile": "found_service1.dat",
            "checkBlackList": true,
            "checkWhieteList": true,
            "ignorePreviousDb": true,
            "saveFacesDb": true
            },
        "service2": {
            "serviceType": "find",
            "source": "file:///tmp/amlo.mp4",
            "cameraId": "camera2_mac_address",
            "enabled": true,
            "generalFaceDectDbFile": "found_service2.dat",
            "checkBlackList": true,
            "checkWhieteList": true,
            "ignorePreviousDb": true,
            "saveFacesDb": true
            }
        },
    "00:04:4b:8d:49:68" : {
        "service1": {
            "serviceType": "find",
            "source": "file:///tmp/amlo.mp4",
            "cameraId": "camera1_mac_address",
            "enabled": false,
            "generalFaceDectDbFile": "found_service1.dat",
            "checkBlackList": true,
            "checkWhieteList": true,
            "ignorePreviousDb": true,
            "saveFacesDb": true
            },
        "service2": {
            "serviceType": "whiteList",
            "source": "file:///tmp/amlo.mp4",
            "cameraId": "camera2_mac_address",
            "enabled": true
            },
        "service3": {
            "serviceType": "ageAndGender",
            "source": "file:///tmp/amlo.mp4",
            "cameraId": "camera3_mac_address",
            "enabled": false,
            "generalFaceDectDbFile": "age_and_gender_service3.dat"
            },
        "service4": {
            "serviceType": "recurrence",
            "source": "file:///tmp/amlo.mp4",
            "cameraId": "camera2_mac_address",
            "enabled": false,
            "generalFaceDectDbFile": "recurrence_service2.dat",
            "checkBlackList": true,
            "checkWhiteList": true
            },
        "service6": {
            "serviceType": "blackList",
            "source": "file:///tmp/amlo.mp4",
            "cameraId": "camera2_mac_address",
            "enabled": true
            }
        }
}
