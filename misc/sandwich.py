#!/usr/bin/env python
# encoding: utf-8
import pdb


bread = ["bread"] * 5
loaves = [bread] * 6


def get_slice():
    global bread
    if not bread:
        bread = loaves.pop()
    return bread.pop()


def make_sandwich():
    bottom_slice = get_slice()
    pb = "pb"
    top_slice = get_slice()
    sandwich = [bottom_slice, pb, top_slice]
    return sandwich


def test_sandwich():
    sandwich = make_sandwich()
    assert sandwich == ["bread", "pb", "bread"]


def main():
    pdb.set_trace()
    test_sandwich()
    test_sandwich()
    test_sandwich()


if __name__ == '__main__':
    main()
