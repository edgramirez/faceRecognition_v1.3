{ 
    "FA:KE:4b:8d:49:68" : {
        "service1": {
            "serviceType": "find",
            "source": "file:///tmp/amlo.mp4",
            "enabled": true,
            "faceDbFile": "found_service1.dat",
            "checkBlackList": true,
            "checkWhieteList": true,
            "ignorePreviousDb": true,
            "saveFacesDb": true
            },
        "service2": {
            "serviceType": "find",
            "source": "file:///tmp/amlo.mp4",
            "enabled": true,
            "faceDbFile": "found_service2.dat",
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
            "enabled": false,
            "faceDbFile": "found_service1.dat",
            "checkBlackList": true,
            "checkWhieteList": true,
            "ignorePreviousDb": true,
            "saveFacesDb": true
            },
        "service2": {
            "serviceType": "recurrence",
            "source": "file:///tmp/amlo.mp4",
            "enabled": true,
            "faceDbFile": "recurrence_service2.dat",
            "checkBlackList": true,
            "checkWhieteList": true
            },
        "service3": {
            "serviceType": "ageAndGender",
            "source": "file:///tmp/amlo.mp4",
            "enabled": false,
            "faceDbFile": "age_and_gender_service3.dat"
            }
        }
}