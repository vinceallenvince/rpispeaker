#!/bin/bash
echo "Starting RPI_SPOTIFY_SPEAKER"
sleep 5
( cd ~/rpispeaker
sudo python speaker.py &
)
( cd ~/ref-speaker-Debug
./esdk-ref-speaker &
)