#!/usr/bin/env python

import re
import sys
import os
from tqdm import tqdm
import rosbag
import inspect


class MessageParser(object):

    def __init__(self, msg):
        self.__msg = msg
        self.__header = ""
        self.__data = ""

    def parse(self):
        self.__header = ""
        self.__data = ""
        self.__parse_message_recursive(self.__msg)
        self.__header = self.__header.rstrip(",")
        self.__data = self.__data.rstrip(",")
        self.__header += "\n"
        self.__data += "\n"

    def get_data(self):
        return self.__data

    def get_header(self):
        return self.__header

    def __parse_message_recursive(self, elem, recursive_str=""):
        attrs = self.__extract_attributes(elem)
        attrs = self.__ego_sort(attrs)

        for attr in attrs:
            val = getattr(elem, attr)
            if self.__is_primitive(val) is True:
                self.__header = self.__header + recursive_str + attr + ","

                # if data is binary str
                if type(val) is str:
                    if '\0' in val:
                        self.__data = self.__data + "binary" + ","
                    else:
                        self.__data = self.__data + str(val) + ","
                else:
                    self.__data = self.__data + str(val) + ","
            elif self.__is_list(val) is True:
                for i, v in enumerate(val):
                    self.__parse_message_recursive(v, recursive_str=recursive_str + attr + "[" + str(i) + "]_")
            else:
                self.__parse_message_recursive(val, recursive_str=recursive_str + attr + "_")

    @staticmethod
    def __ego_sort(attrs):
        # for header
        if "header" in attrs:
            val = attrs.pop(attrs.index("header"))
            attrs.insert(0, val)

        # for stamp
        if "stamp" in attrs:
            val = attrs.pop(attrs.index("stamp"))
            attrs.insert(0, val)

        # for position and orientation
        if "position" in attrs and "orientation" in attrs:
            idx1 = attrs.index("position")
            idx2 = attrs.index("orientation")
            if idx1 > idx2:
                attrs[idx2], attrs[idx1] = attrs[idx1], attrs[idx2]

        # for x y z w
        if "w" in attrs:
            val = attrs.pop(attrs.index("w"))
            attrs.append(val)

        # for secs nsecs
        if "secs" in attrs and "nsecs" in attrs:
            idx1 = attrs.index("secs")
            idx2 = attrs.index("nsecs")
            if idx1 > idx2:
                attrs[idx2], attrs[idx1] = attrs[idx1], attrs[idx2]

        # for linear and angular
        if "linear" in attrs and "angular" in attrs:
            idx1 = attrs.index("linear")
            idx2 = attrs.index("angular")
            if idx1 > idx2:
                attrs[idx2], attrs[idx1] = attrs[idx1], attrs[idx2]

        return attrs

    @staticmethod
    def __extract_attributes(elem):
        attrs = dir(elem)
        attrs = [s for s in attrs if not s.startswith('_') and not inspect.ismethod(getattr(elem, s))]

        return attrs

    @staticmethod
    def __is_primitive(val):
        if type(val) is int or type(val) is float or type(val) is bool or type(val) is str:
            return True
        else:
            return False

    @staticmethod
    def __is_list(val):
        if type(val) is list:
            return True
        else:
            return False


def generate_csv(b, tpc, opn):
    is_header_written = False

    # file open
    with open(opn, "w") as f:

        # progress bar
        progress_time = 0
        with tqdm(total=(int(b.get_end_time()) - int(b.get_start_time()))) as pbar:

            # processing
            for topic, msg, t in b.read_messages(topics=tpc):
                mp = MessageParser(msg)
                mp.parse()

                if not is_header_written:
                    f.write("time_rospy_secs,time_rospy_nsecs,time_rospy," + mp.get_header())
                    is_header_written = True
                time_rospy = t.secs + t.nsecs * 1e-9
                f.write('{0},{1},{2:.9f},{3}'.format(t.secs, t.nsecs , time_rospy,  mp.get_data()))

                if (int(t.secs) - int(bag.get_start_time())) != progress_time:
                    progress_time += 1
                    pbar.update(1)


if __name__ == '__main__':

    args = sys.argv

    # confirm the length of args
    if len(args) > 2 and re.match('.*.bag', args[1]):
        print "valid args" + str(args)
    else:
        print "usage: python bag2csv.py [rosbag] [topic1] [topic2] ... [topicN]"
        sys.exit(1)

    # pop unnecessary arg
    dummy = args.pop(0)

    # file read
    filepath = args.pop(0)
    basename, ext = os.path.splitext(os.path.basename(filepath))

    print "opening: '" + filepath + "'..."

    with rosbag.Bag(filepath) as bag:
        topics = bag.get_type_and_topic_info()[1].keys()
        # loop for topics
        for arg in args:
            if arg in topics:
                output_name = basename + str(arg).replace('/', '_') + ".csv"
                print "output topic: " + arg
                print "save as: " + output_name + "..."
                generate_csv(b=bag, tpc=arg, opn=output_name)
            else:
                print "'" + arg + "' not found..."



