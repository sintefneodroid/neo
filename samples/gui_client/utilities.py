#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'cnheider'

import io

import numpy as np
from PIL import Image


def get_masked_depth_image(depth_image, light_mask_image, lower_limit, upper_limit):
  mask = Image.open(light_mask_image).convert('L')
  mask_array = np.asarray(mask)
  mask_array = mask_array.reshape((mask_array.shape[0], mask_array.shape[1], 1))
  mask_array.setflags(write=1)
  above_threshold = mask_array[:, :, 0] > upper_limit
  mask_array[above_threshold] = 0
  below_threshold = mask_array[:, :, 0] < lower_limit
  mask_array[below_threshold] = 0
  rest = mask_array[:, :, 0] == 0
  depth_image = Image.open(depth_image).convert('L')
  depth_image_array = np.asarray(depth_image)
  ori = depth_image_array.shape
  depth_image_array = depth_image_array.reshape(
      (depth_image_array.shape[0], depth_image_array.shape[1], 1)
      )
  depth_image_array.setflags(write=1)
  depth_image_array[rest] = 0
  depth_image_array = depth_image_array.reshape(ori)
  final = Image.fromarray(depth_image_array)
  img_byte_array = io.BytesIO()
  final.save(img_byte_array, format='png')
  img_byte_array.seek(0)
  return img_byte_array


def rgb_segment(rgb_im, seg_im):
  RED, GREEN, BLUE, ALPHA = (0, 1, 2, 3)

  red_img = np.zeros((rgb_im.shape[1], rgb_im.shape[0], 3), np.uint8)
  green_img = np.zeros((rgb_im.shape[1], rgb_im.shape[0], 3), np.uint8)
  blue_img = np.zeros((rgb_im.shape[1], rgb_im.shape[0], 3), np.uint8)

  red_masked_img = np.zeros((rgb_im.shape[1], rgb_im.shape[0], 3), np.uint8)
  green_masked_img = np.zeros((rgb_im.shape[1], rgb_im.shape[0], 3), np.uint8)
  blue_masked_img = np.zeros((rgb_im.shape[1], rgb_im.shape[0], 3), np.uint8)

  reds = seg_im[:, :, RED]
  greens = seg_im[:, :, GREEN]
  blues = seg_im[:, :, BLUE]

  red_mask = reds == 255
  green_mask = greens == 255
  blue_mask = blues == 255

  red_img[red_mask] = [255, 0, 0]
  green_img[green_mask] = [0, 255, 0]
  blue_img[blue_mask] = [0, 0, 255]

  red_masked_img[red_mask] = rgb_im[red_mask]
  green_masked_img[green_mask] = rgb_im[green_mask]
  blue_masked_img[blue_mask] = rgb_im[blue_mask]

  return red_img, green_img, blue_img, red_masked_img, green_masked_img, blue_masked_img
