#!/usr/bin/env python
# -*- coding: utf-8 -*-
from random import randint


class RandomSleepSecondGen:
    def __init__(self, min, max, mulProb=3, mulRate=5):
        self.min = min
        self.max = max
        self.mulProb = mulProb
        self.mulRate = mulRate

    def getNextSleepSecond(self):
        base = randint(self.min, self.max)
        shouldMul = randint(0, 10) <= self.mulProb
        ssecond = base * self.mulRate if shouldMul else base
        return ssecond


def main():
    print("Hello world!")


if __name__ == '__main__':
    main()
