#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from matplotlib import pyplot

from draugr import (
    float_chw_to_hwc_uint_batch,
    generator_batch,
    horizontal_imshow,
    reverse_torch_vision_normalize_chw,
    to_tensor,
    torch_vision_normalize_chw,
    uint_hwc_to_chw_float_batch,
)
from draugr.numpy_utilities.torch_channel_transform import rgb_drop_alpha_batch_nhwc
from neodroid.wrappers.observation_wrapper.mixed_observation_wrapper import (
    MixedObservationWrapper,
)

__author__ = "Christian Heider Nielsen"
__doc__ = ""


def main():
    env = MixedObservationWrapper()

    data_iter = generator_batch(iter(env), 5 * 3)

    inputs, true_label = zip(*next(data_iter))

    inputs = torch_vision_normalize_chw(
        uint_hwc_to_chw_float_batch(
            rgb_drop_alpha_batch_nhwc(to_tensor(inputs, device="cpu"))
        )
    )

    inputs = float_chw_to_hwc_uint_batch(reverse_torch_vision_normalize_chw(inputs))

    horizontal_imshow(inputs, true_label, columns=5)
    pyplot.show()


if __name__ == "__main__":
    main()
