#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys

__author__ = "Christian Heider Nielsen"


def inc(x):
    return x + 1


def test_answer():
    assert inc(4) == 5


def test_sanity():
    assert True
    assert False is not True
    answer_to_everything = str(42)
    assert str(42) == answer_to_everything


def test_print(capsys):
    """Correct my_name argument prints"""
    text = "hello"
    err = "world"
    print(text)
    sys.stderr.write("world")
    captured = capsys.readouterr()
    assert text in captured.head
    assert err in captured.err


if __name__ == "__main__":
    test_sanity()
