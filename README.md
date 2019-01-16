# bag2csv

## Requirements

- ROS kinetic(Ubuntu 16.04)

## Dependencies

    $ pip install tqdm

## Usage

    $ python bag2csv.py [rosbag] [topic1] [tpoic2] ... [tpoicN]


In addition, you can use the following shell script for multiple rosbags.

    $ ./bag2csv_multi_bag.sh [rosbag1] [rosbag2] ... []rosbagN]
When you specify more topics to output, please edit `TOPICS` variable in `bag2csv_multi_bag.sh`.
     
