#!/bin/bash

TOPICS="/current_pose \
        /estimate_twist \
        /ovp_controller/control_status \
        /ovp_controller/vehicle_status \
        /vehicle_cmd \
        /closest_waypoint"

for x in "$@"
do
    if [[ $x =~ .bag ]]; then
        python bag2csv.py $x $TOPICS
    else
        echo "not match: $x"
    fi   
done
