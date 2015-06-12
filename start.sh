#!/bin/bash
echo "Starting RPI_SPOTIFY_SPEAKER"
sleep 5

#( cd ~/rpispeaker
#sudo python speaker.py &
#)

# start the speaker
( cd ~/ref-speaker-Debug
./esdk-ref-speaker &
)

# wait for speaker to login
sleep 5

# get the speaker status
statusdata=$(curl --silent http://localhost:15004/status-data)

# start playing to take control
curl http://localhost:15004/action?action=preset-1

# give the player time to switch to new context if necessary 
sleep 3

# the string to the right of the =~ operator is considered an extended regular expression

if [[ "$statusdata" =~ '"shuffle_state":"1"' ]]
then
        echo "got shuffle status: 1"
else
        echo "got shuffle status: 0"
        curl http://localhost:15004/action?action=shuffle
fi

if [[ "$statusdata" =~ '"repeat_state":"1"' ]]
then
        echo "got repeat status: 1"
else
        echo "got repeat status: 0"
        curl http://localhost:15004/action?action=repeat
fi