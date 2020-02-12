#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Christian Heider Nielsen"
__doc__ = r"""

           Created on 03/01/2020
           """

from math import sin, cos, acos, sqrt
from typing import Iterable

import numpy

__all__ = ["normalise_vector", "Quaternion"]


def normalise_vector(vector: Iterable, tolerance=0.00001) -> numpy.ndarray:
    mag2 = sum(n * n for n in vector)
    if abs(mag2 - 1.0) > tolerance:
        mag = sqrt(mag2)
        vector = tuple(n / mag for n in vector)
    return numpy.array(vector)


class Quaternion:
    @staticmethod
    def from_axisangle(theta, vector):
        vector = normalise_vector(vector)

        new_quaternion = Quaternion()
        new_quaternion._axisangle_to_q(theta, vector)
        return new_quaternion

    @staticmethod
    def from_value(value):
        new_quaternion = Quaternion()
        new_quaternion.components = value
        return new_quaternion

    def _axisangle_to_q(self, theta, v):
        x = v[0]
        y = v[1]
        z = v[2]

        w = cos(theta / 2.0)
        x = x * sin(theta / 2.0)
        y = y * sin(theta / 2.0)
        z = z * sin(theta / 2.0)

        self.components = numpy.array([w, x, y, z])

    def __mul__(self, b):

        if isinstance(b, Quaternion):
            return self._multiply_with_quaternion(b)
        elif isinstance(b, (list, tuple, numpy.ndarray)):
            if len(b) != 3:
                raise Exception(f"Input vector has invalid length {len(b)}")
            return self._multiply_with_vector(b)
        else:
            raise Exception(f"Multiplication with unknown type {type(b)}")

    def _multiply_with_quaternion(self, q2):
        w1, x1, y1, z1 = self.components
        w2, x2, y2, z2 = q2.components
        w = w1 * w2 - x1 * x2 - y1 * y2 - z1 * z2
        x = w1 * x2 + x1 * w2 + y1 * z2 - z1 * y2
        y = w1 * y2 + y1 * w2 + z1 * x2 - x1 * z2
        z = w1 * z2 + z1 * w2 + x1 * y2 - y1 * x2

        result = Quaternion.from_value(numpy.array((w, x, y, z)))
        return result

    def _multiply_with_vector(self, vector: Iterable):
        q2 = Quaternion.from_value(numpy.append(0.0, vector))
        return (self * q2 * self.get_conjugate()).components[1:]

    def get_conjugate(self):
        w, x, y, z = self.components
        result = Quaternion.from_value(numpy.array((w, -x, -y, -z)))
        return result

    def __repr__(self):
        theta, vector = self.get_axisangle()
        return f"(({theta:.6f}; {vector[0]:.6f}, {vector[1]:.6f}, {vector[2]:.6f}))"

    def get_axisangle(self):
        w, axis = self.components[0], self.components[1:]
        theta = acos(w) * 2.0

        return theta, normalise_vector(axis)

    def tolist(self):
        return self.components.tolist()

    def vector_norm(self):
        w, v = self.get_axisangle()
        return numpy.linalg.norm(v)


if __name__ == "__main__":

    x_axis_unit = (1, 0, 0)
    y_axis_unit = (0, 1, 0)
    z_axis_unit = (0, 0, 1)

    r1 = Quaternion.from_axisangle(numpy.pi / 2, x_axis_unit)
    r2 = Quaternion.from_axisangle(numpy.pi / 2, y_axis_unit)
    r3 = Quaternion.from_axisangle(numpy.pi / 2, z_axis_unit)

    # Quaternion - vector multiplication
    v = r1 * y_axis_unit
    v = r2 * v
    v = r3 * v

    print(v)

    # Quaternion - quaternion multiplication
    r_total = r3 * r2 * r1
    v = r_total * y_axis_unit

    print(v)
