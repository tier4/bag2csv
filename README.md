# bag2csv

## Requirements

- ROS kinetic(Ubuntu 16.04)


## Dependencies

    $ pip install tqdm


## Usage

    $ python bag2csv.py --bags [rosbag1] ... [rosbagN] --topics [topic1] ... [topicN]
    
    
## Arguments Details
  ```
  -h, --help            show this help message and exit
  -b [BAGS [BAGS ...]], --bags [BAGS [BAGS ...]]
                        rosbag filepaths
  -t [TOPICS [TOPICS ...]], --topics [TOPICS [TOPICS ...]]
                        topics name you want to save ( don't forget slash!!)
  ```
