#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created by PyCharm.
# User: funway
# Date: 2019/9/6
# Time: 16:02

import logging
import board

LOG_FORMAT = "%(asctime)s pid[%(process)d] tid[%(thread)d] %(levelname)7s %(name)s.%(funcName)s - %(message)s"

LOG_LEVEL = logging.INFO

# 控制信号针脚
LED_CONTROL_PIN = board.D18

# 每个音符对应几个LED灯珠
LED_PIXELS_PER_NOTE = 1

# 逻辑上选中的第一颗灯珠与实际LED头的位移
LED_PIXELS_OFFSET = 10

# LED灯珠亮度
LED_BRIGHTNESS = 0.2

COLOR_NOTE_ON = (255, 0, 0)

COLOR_NOTE_OFF = (0, 0, 0)

COLOR_FADE_IN = (30, 30, 0)

COLOR_FADE_OUT = (40, 0, 0)

# 预处理时候，使用该因子将浮点的时间提升成整形来进行运算。
# 即将浮点的秒换成整形的微秒进行后续处理
TIME_FACTOR = 1000000

# 播放时sleep的时间精度
TIME_PRECISION = 0.001

# LED亮灯前多少秒开始淡入
# 0表示不做淡入效果
TIME_FADE_IN = 0.1

# LED亮灯后多少秒开始淡出
# 0表示不做淡出效果
TIME_FADE_OUT = 0.1
