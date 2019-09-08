#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created by PyCharm.
# User: funway
# Date: 2019/9/6
# Time: 10:51

"""
This script light on led for aligning led pixel to piano key.
LED灯珠与钢琴琴键校准
"""

from led_strip import LEDStrip
from config import *


def main():
    led = LEDStrip(pin=LED_CONTROL_PIN, ppn=LED_PIXELS_PER_NOTE,
                   offset=LED_PIXELS_OFFSET, brightness=LED_BRIGHTNESS)
    led.alignment()
    pass


if __name__ == "__main__":
    main()
