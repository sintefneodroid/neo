#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time
from math import sqrt, floor, ceil
from typing import Iterable

import cv2
from matplotlib import pyplot
import numpy
from matplotlib import animation

from draugr import (
    generator_batch,
    horizontal_imshow,
    uint_hwc_to_chw_float_batch,
    torch_vision_normalize_chw,
    float_chw_to_hwc_uint_batch,
    reverse_torch_vision_normalize_chw,
    to_tensor,
)
from draugr.torch_utilities.images.channel_transform import rgb_drop_alpha_batch
from neodroid.environments.unity_environment import UnityEnvironment
from neodroid.environments.unity_environment.deprecated.batched_unity_environments import (
    VectorWrapper,
)
from neodroid.utilities.unity_specifications.prefabs.neodroid_camera_extraction import (
    extract_all_as_camera,
)
from neodroid.wrappers.observation_wrapper.mixed_observation_wrapper import (
    MixedObservationWrapper,
)
from warg.named_ordered_dictionary import NOD

__author__ = "Christian Heider Nielsen"
__doc__ = ""


def main():
    env = MixedObservationWrapper()

    data_iter = generator_batch(iter(env), 5 * 3)

    inputs, true_label = zip(*next(data_iter))

    inputs = torch_vision_normalize_chw(
        uint_hwc_to_chw_float_batch(
            rgb_drop_alpha_batch(to_tensor(inputs, device="cpu"))
        )
    )

    inputs = float_chw_to_hwc_uint_batch(reverse_torch_vision_normalize_chw(inputs))

    horizontal_imshow(inputs, true_label, columns=5)
    pyplot.show()


if __name__ == "__main__":
    main()
