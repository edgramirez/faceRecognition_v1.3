#!/bin/bash
#rm -f data/video_encoded_faces/*

#./load_subject.py blacklist

#cp data/encoded_known_faces/knownFaces.dat /tmp/data/encoded_known_faces/
#ls -lartc data/encoded_known_faces/knownFaces.dat

#rm -rf /tmp/stream_0; python3 face_detection.py     file:///tmp/obama_biden.mp4     /tmp/stream_0
#rm -rf /tmp/stream_0; python3 subject_search.py     rtsp://192.168.128.6:9000/live /tmp/stream_0
#rm -rf /tmp/stream_0; python3 face_detection.py     file:///tmp/obama_biden.mp4            /tmp/stream_0
rm -rf /tmp/stream_0; python3 subject_search.py     file:///tmp/amlo.mp4            /tmp/stream_0
#rm -rf /tmp/stream_0; python3 face_detection.py     file:///tmp/amlo.mp4            /tmp/stream_0
#rm -rf /tmp/stream_0; python3 face_detection.py     file:///tmp/HD_CCTV_Camera.mp4  /tmp/stream_0

exit 111
ssh edgar@192.168.130.5 'rm -rf /tmp/stream_0'
ssh edgar@192.168.130.5 'rm -f /tmp/resultados/*'

scp -r /tmp/stream_0         edgar@192.168.130.5:/tmp
scp    /tmp/found_elements/* edgar@192.168.130.5:/tmp/resultados/
