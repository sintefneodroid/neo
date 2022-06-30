#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from draugr import batch_generator
from draugr.python_utilities.torch_like_channel_transformation import (
    reverse_torch_vision_normalize_batch_nchw,
    rgb_drop_alpha_batch_nhwc,
    torch_vision_normalize_batch_nchw,
)
from draugr.torch_utilities import (
    float_chw_to_hwc_uint_tensor,
    to_tensor,
    uint_hwc_to_chw_float_tensor,
)
from draugr.visualisation.matplotlib_utilities import horizontal_imshow
from matplotlib import pyplot

from neodroid.wrappers.observation_wrapper.mixed_observation_wrapper import (
    MixedObservationWrapper,
)

__author__ = "Christian Heider Nielsen"
__doc__ = r"""
"""


def main():
    env = MixedObservationWrapper()

    data_iter = batch_generator(iter(env), 5 * 3)

    inputs, true_label = zip(*next(data_iter))

    inputs = torch_vision_normalize_batch_nchw(
        uint_hwc_to_chw_float_tensor(
            rgb_drop_alpha_batch_nhwc(to_tensor(inputs, device="cpu"))
        )
    )

    inputs = float_chw_to_hwc_uint_tensor(
        reverse_torch_vision_normalize_batch_nchw(inputs)
    )

    horizontal_imshow(inputs, true_label, num_columns=5)
    pyplot.show()


if __name__ == "__main__":
    main()
