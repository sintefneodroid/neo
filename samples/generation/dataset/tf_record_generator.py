#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json

from neodroid import PROJECT_APP_PATH
from neodroid.environments.unity_environment import connect

__author__ = "Christian Heider Nielsen"
__doc__ = ""

import tensorflow as tf

tf.enable_eager_execution()


class TFFeature:
    @staticmethod
    def listify(value):
        if isinstance(value, list):
            return value
        return [value]

    @staticmethod
    def bytes(value):
        """Returns a bytes_list from a string / byte."""
        return tf.train.Feature(
            bytes_list=tf.train.BytesList(value=TFFeature.listify(value))
        )

    @staticmethod
    def float(value):
        """Returns a float_list from a float / double."""
        return tf.train.Feature(
            float_list=tf.train.FloatList(value=TFFeature.listify(value))
        )

    @staticmethod
    def int64(value):
        """Returns an int64_list from a bool / enum / int / uint."""
        return tf.train.Feature(
            int64_list=tf.train.Int64List(value=TFFeature.listify(value))
        )


TFF = TFFeature


def neodroid_tf_example(image_string, label, image_shape, bounding_box):
    """

:param bounding_box:
:param image_shape:
:param image_string:
:param label:
:return:
"""

    feature = {
        "height": TFF.int64([image_shape[0]]),
        "width": TFF.int64([image_shape[1]]),
        "depth": TFF.int64([image_shape[2]]),
        "label": TFF.int64([int(label)]),
        "bb_x": TFF.float([bounding_box["x"]]),
        "bb_y": TFF.float([bounding_box["y"]]),
        "bb_w": TFF.float([bounding_box["w"]]),
        "bb_h": TFF.float([bounding_box["h"]]),
        "image_raw": TFF.bytes([image_string.tobytes()]),
    }

    return tf.train.Example(features=tf.train.Features(feature=feature))


def write_tf_record_file(data_tuples, file_name="neodroid_bb_images.tfr"):
    """

"""

    with tf.python_io.TFRecordWriter(file_name) as writer:
        for data_tuple in data_tuples:
            tensorflow_example = neodroid_tf_example(*data_tuple)
            writer.write(tensorflow_example.SerializeToString())


if __name__ == "__main__":

    generate_num = 10
    output_file_name = PROJECT_APP_PATH.user_data / "neodroid_bb_images.tfr"

    if generate_num > 0:
        dt = []
        with connect() as env:
            for i, state in enumerate(env):
                if i >= generate_num:
                    break

                state = state[list(state.keys())[0]]
                label = state.sensor("Class").value
                bb = state.sensor("BoundingBox").value
                image_data = state.sensor("RGB").value
                dt.append((image_data, label, (256, 256, 4), json.loads(bb)))

        write_tf_record_file(dt, file_name=output_file_name)

    raw_image_dataset = tf.data.TFRecordDataset(output_file_name)

    image_feature_description = {
        "height": tf.FixedLenFeature([], tf.int64),
        "width": tf.FixedLenFeature([], tf.int64),
        "depth": tf.FixedLenFeature([], tf.int64),
        "label": tf.FixedLenFeature([], tf.int64),
        "bb_x": tf.FixedLenFeature([], tf.float32),
        "bb_y": tf.FixedLenFeature([], tf.float32),
        "bb_w": tf.FixedLenFeature([], tf.float32),
        "bb_h": tf.FixedLenFeature([], tf.float32),
        "image_raw": tf.FixedLenFeature([], tf.string),
    }  # Create a dictionary describing the features.

    def _parse_image_function(example_proto):
        # Parse the input tf.Example proto using the dictionary above.
        return tf.parse_single_example(example_proto, image_feature_description)

    parsed_image_dataset = raw_image_dataset.map(_parse_image_function)
    for image_features in parsed_image_dataset:

        print(image_features["bb_x"])
        print(image_features["bb_y"])
        print(image_features["bb_w"])
        print(image_features["bb_h"])
