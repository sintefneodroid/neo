#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time

import torch
from PIL import Image

from executables.guiclient.utilities import DiceCoeff, rgb_segment
from neodroid.utilities.messaging_utilities.neodroid_camera_extraction import extract_neodroid_camera

__author__ = 'cnheider'

import neodroid as neo
import matplotlib.pyplot as plt


def collect_states(_environments, num=4):
  states_c = []
  for _ in range(num):
    actions = _environments.action_space.sample()
    states = _environments.react(actions)
    state = next(iter(states.values()))
    terminated = state.terminated
    states_c.append(state)
  return states_c


def plot_images(rgb_im, seg_im, red_img, green_img, blue_img, red_masked_img, green_masked_img,
                blue_masked_img):
  fig = plt.figure()

  (ax1, ax2), (ax3, ax4), (ax5, ax6), (ax7, ax8) = fig.subplots(4, 2)

  ax1.imshow(rgb_im)
  ax2.imshow(seg_im)

  ax3.imshow(red_img)
  ax4.imshow(red_masked_img)

  ax5.imshow(green_img)
  ax6.imshow(green_masked_img)

  ax7.imshow(blue_img)
  ax8.imshow(blue_masked_img)

  fig.tight_layout()
  plt.show()


i = 0


def save(rgb_im, seg_im):
  global i
  path = '/home/heider/Datasets/Neodroid/Segmentation/train'

  r_im = Image.fromarray(rgb_im)
  r_im.save(path + f'/image/image_{i}.png')
  s_im = Image.fromarray(seg_im)
  s_im.save(path + f'/mask/image_{i}_mask.png')
  i = i + 1


def process_states(states):
  rgb_imgs = []
  for state in states:
    rgb_img, seg_img, *_ = extract_neodroid_camera(state)

    red_img, green_img, blue_img, red_masked_img, green_masked_img, blue_masked_img = rgb_segment(rgb_img,
                                                                                                  seg_img)
    normed = red_img[:, :, 0] / 255.
    rgb_imgs.append((rgb_img / 255., normed))
    # save(rgb_img, red_img)

    # plot_images(rgb_im,seg_im,red_img, green_img, blue_img, red_masked_img, green_masked_img,
    # blue_masked_img)

  return rgb_imgs


from torch import nn
from torch.nn import functional as F


class CNN(nn.Module):

  def __init__(self):
    super().__init__()

    self.conv1 = nn.Conv2d(3, 16, kernel_size=3, padding=1)
    # self.bn1 = nn.BatchNorm2d(16)
    self.pool1 = nn.MaxPool2d(2)
    self.conv2 = nn.Conv2d(16, 16, kernel_size=3, padding=1)
    # self.bn2 = nn.BatchNorm2d(16)
    # self.upsample1 = nn.Upsample(scale_factor=2, mode='bilinear', align_corners=True)
    # self.upsample2 = nn.Upsample(scale_factor=2, mode='bilinear', align_corners=True)
    self.tconv1 = nn.ConvTranspose2d(16, 1, kernel_size=2, stride=2)

  def forward(self, x):
    x = self.conv1(x)
    # x = self.bn1(x)
    x = F.relu(x)
    x = self.pool1(x)
    x = self.conv2(x)
    # x = self.bn1(x)
    x = F.relu(x)
    # x = self.upsample1(x)
    x = self.tconv1(x)
    # x = self.upsample2(x)
    return x.transpose(1, -1).squeeze()


def main():
  _environments = neo.make(environment_name='seg', connect_to_running=True)
  _environments.reset()

  i = 0
  freq = 100
  time_s = time.time()

  net = CNN()
  optimiser = torch.optim.Adam(net.parameters())
  loss = DiceCoeff()

  while _environments.is_connected:
    states = collect_states(_environments)

    la = process_states(states)

    inputs, labels = zip(*la)
    inputs = torch.Tensor(inputs).transpose(1, -1)
    labels = torch.Tensor(labels).transpose(1, -1)

    preds = net(inputs).contiguous()

    los = loss(preds, labels.contiguous())

    los.backward(retain_graph=True)
    optimiser.step()
    optimiser.zero_grad()

    terminated = False

    time_now = time.time()
    if i % freq == 0:
      fps = (1 / (time_now - time_s))
      print(f'fps:[{fps}], loss:[{los}]')

      if i % (10 * freq) == 0:
        fig = plt.figure()

        (ax1, ax2) = fig.subplots(1, 2)

        preds2 = preds.detach().numpy()
        ax1.imshow(preds2[0])
        ax2.imshow(labels[0])

        fig.tight_layout()
        plt.show()

    i += 1
    time_s = time_now

    if terminated:
      _environments.reset()


if __name__ == '__main__':
  main()
