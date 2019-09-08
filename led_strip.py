#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created by PyCharm.
# User: funway
# Date: 2019/9/6
# Time: 23:46

import time
import logging
import neopixel

NOTE_START = 21
NOTE_END = 108
NOTE_NUMBERS = 88

COLOR_RED = (255, 0, 0)
COLOR_GREEN = (0, 128, 0)
COLOR_BLUE = (0, 0, 255)
COLOR_YELLOW = (255, 255, 0)
COLOR_PURPLE = (128, 0, 128)
COLOR_WHITE = (255, 255, 255)
COLOR_OFF = (0, 0, 0)


class LEDStrip(object):
    """"""
    
    def __init__(self, pin, ppn, offset, brightness):
        """
        构造函数
        :param pin: Raspberry Pi control pin number
        :param ppn: LED pixels per note
        :param offset: LED pixels offset
        :param brightness: LED brightness
        """
        super(LEDStrip, self).__init__()
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.info('init a %s instance.', self.__class__.__name__)

        self.control_pin = pin
        self.pixels_per_note = ppn
        self.pixels_offset = offset
        self.brightness = brightness
        self.pixels = neopixel.NeoPixel(pin=pin,
                                        n=offset + ppn * NOTE_NUMBERS,
                                        auto_write=False,
                                        brightness=brightness)
        self.logger.info('led length: %s pixels(%s offset), %s pixels per note.', len(self.pixels), offset, ppn)
        pass
    
    def test(self):
        """
        LED自检
        """
        self.pixels.fill(COLOR_GREEN)
        self.pixels.show()
        time.sleep(0.5)
        self.pixels.fill(COLOR_OFF)
        self.pixels.show()

        for i in range(NOTE_START, NOTE_END+1):
            self.write_note(i, COLOR_RED)
            # time.sleep(0.01)
        for i in range(NOTE_START, NOTE_END+1):
            self.write_note(i, COLOR_OFF)
            # time.sleep(0.01)
        pass

    def alignment(self):
        """
        LED灯珠与琴键位置校准
        """
        self.write_note(60, COLOR_RED)

        for i in range(1, 50):
            left = 60 - i
            right = 60 + i
            if left > NOTE_START:
                self.write_note(left, COLOR_BLUE)
            elif left == NOTE_START:
                self.write_note(left, COLOR_RED)
            if right < NOTE_END:
                self.write_note(right, COLOR_BLUE)
            elif right == NOTE_END:
                self.write_note(right, COLOR_RED)

        pass

    def write_note(self, note, color, auto_show=True):
        """
        将与note音符对应的灯珠的点亮信息写入到pixels列表中，
        并执行点亮操作（可选）
        :param note: midi文件中的note number
        :param color: 要显示的颜色，用(r, g, b)三元组表示。 (0, 0, 0)表示熄灭
        :param auto_show: 是否在方法末尾调用led的show函数来点亮灯珠
        :return:
        """

        assert NOTE_START <= note <= NOTE_END, 'note {} out of range[{}, {}]'.format(note, NOTE_START, NOTE_END)

        note_start_pixel = self.pixels_offset + (note - NOTE_START) * self.pixels_per_note
        for i in range(self.pixels_per_note):
            self.logger.debug('write note=%s, pixel index=%s', note, note_start_pixel + i)
            self.pixels[note_start_pixel + i] = color

        if auto_show:
            self.logger.debug('show light(auto)')
            self.pixels.show()
        pass

    def show(self):
        """
        点亮LED灯带
        """
        self.logger.debug('show light(manual)')
        self.pixels.show()
        pass
