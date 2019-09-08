#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created by PyCharm.
# User: funway
# Date: 2019/9/7
# Time: 13:30

"""

"""

import argparse
import logging
import time
import timeit
import queue
import mido
import threading
from config import *
from led_strip import LEDStrip

VERSION = '0.1'


class FadeMessage(object):
    """灯光淡入淡出的事件"""
    is_meta = False

    def __init__(self, type, channel, note, velocity, note_time):
        super(FadeMessage, self).__init__()

        assert type == 'fade_in' or type == 'fade_out', 'type error'
        self.type = type
        self.channel = channel
        self.note = note
        self.velocity = velocity
        self.note_time = note_time

    def __repr__(self):
        return '<message {} channel={} note={}> velocity={} note_time={}'.format(
            self.type,
            self.channel,
            self.note,
            self.velocity,
            self.note_time)


class LEDPlayThread(threading.Thread):
    """
    LED播放线程
    """

    def __init__(self, strip, msg_queue):
        """
        构造函数
        :param strip: LEDStrip实例
        :param msg_queue: 消息队列
        """
        super(LEDPlayThread, self).__init__()

        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.info('init a %s instance.', self.__class__.__name__)

        self.msg_queue = msg_queue
        self.note_msg = [None] * 109
        self.strip = strip
        pass

    def run(self):
        self.logger.info('led play thread start')
        while True:
            key, msg = self.msg_queue.get()
            self.logger.debug('get (%s, %s)', key, msg)
            if key == 'end':
                break

            if key == 'show':
                self.strip.show()
                continue

            if msg.type == 'fade_in':
                if self.note_msg[msg.note] is None:
                    self.logger.debug('note[%s] fade in', msg.note)
                    self.strip.write_note(msg.note, COLOR_FADE_IN, auto_show=False)
                continue
            if msg.type == 'fade_out':
                if self.note_msg[msg.note] is not None and self.note_msg[msg.note] < key:
                    self.logger.debug('note[%s] fade out', msg.note)
                    self.strip.write_note(msg.note, COLOR_FADE_OUT, auto_show=False)
                continue
            if msg.type == 'note_on' and msg.velocity > 0:
                self.logger.debug('note[%s] on', msg.note)
                self.strip.write_note(msg.note, COLOR_NOTE_ON, auto_show=False)
                self.note_msg[msg.note] = key
            elif msg.type == 'note_off' or (msg.type == 'note_on' and msg.velocity == 0):
                self.logger.debug('note[%s] off', msg.note)
                self.strip.write_note(msg.note, COLOR_NOTE_OFF, auto_show=False)
                self.note_msg[msg.note] = None

        self.logger.info('led play thread end.')
        pass


def add_message(messages, key, msg):
    """
    将消息msg以key为主键添加到messages字典中
    messages = {key1:[msg, msg], key2:[msg, msg, msg], key3:[msg]}
    :param messages: 目标消息字典
    :param key:
    :param msg:
    :return:
    """
    if key not in messages:
        messages[key] = [msg]
    else:
        messages[key].append(msg)
    pass


def pre_process(mid):
    """
    将原生的midi消息预处理成字典的形式，并增加LED灯光的淡入淡出事件。
    字典的key是事件发生的时间点（用TIME_FACTOR换算成整形表示的微秒），value是该时间点发生的所有事件列表。
    :param mid: a mido.MidiFile instance
    :return: processed messages dictionary. eg: {time_key1:[msg, msg], time_key2:[msg, msg, msg], time_key3:[msg]}
    """
    messages = dict()
    play_time = 0
    for msg in mid:
        play_time += msg.time
        key = round(play_time * TIME_FACTOR)
        add_message(messages, key, msg)

        if msg.type == 'note_on' and msg.velocity != 0:
            # 把fade in, fade out事件加入到dict中
            if TIME_FADE_IN != 0:
                fade_in_msg = FadeMessage(type='fade_in', channel=msg.channel, note=msg.note,
                                          velocity=msg.velocity, note_time=play_time)
                fade_in_time = play_time - TIME_FADE_IN
                add_message(messages, round(fade_in_time * TIME_FACTOR), fade_in_msg)
            if TIME_FADE_OUT != 0:
                fade_out_msg = FadeMessage(type='fade_out', channel=msg.channel, note=msg.note,
                                           velocity=msg.velocity, note_time=play_time)
                fade_out_time = play_time + TIME_FADE_OUT
                add_message(messages, round(fade_out_time * TIME_FACTOR), fade_out_msg)
            pass
        pass

    # 打印处理后的消息列表
    logging.debug('pre_processed midi messages:')
    logging.debug('================================')
    for key in sorted(messages.keys()):
        logging.debug('key: %s, msg: %s', key, messages[key])
    logging.debug('================================')

    return messages


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file',
                        dest='file',
                        required=True,
                        help=u"midi file to load")
    parser.add_argument('-p', '--port',
                        dest='port',
                        required=False,
                        default=None,
                        help=u"port name of audio output")
    parser.add_argument("-v", "--version",
                        action="version",
                        version="%(prog)s " + VERSION)

    args = parser.parse_args()
    return args


def led_play(mid, audio_port):
    # 1. init a LEDStrip instance
    led = LEDStrip(pin=LED_CONTROL_PIN, ppn=LED_PIXELS_PER_NOTE,
                   offset=LED_PIXELS_OFFSET, brightness=LED_BRIGHTNESS)
    led.test()

    # 2. pre process midi messages to dictionary
    messages = pre_process(mid)
    msg_queue = queue.Queue()

    # 5. init a LEDPlayThread instance then run
    led_thread = LEDPlayThread(led, msg_queue)
    led_thread.start()

    # 6. sort messages dictionary keys
    sorted_keys = sorted(messages.keys())
    logging.info('estimated play time(with fade message): %s seconds',
                 (sorted_keys[-1] - sorted_keys[0]) / TIME_FACTOR)

    start_timer = timeit.default_timer()
    logging.info('start play. start_timer=%s', start_timer)

    # 7. start play
    for key in sorted_keys:
        current_time = timeit.default_timer() - start_timer
        play_time = (key - sorted_keys[0]) / TIME_FACTOR
        sleep_delta = play_time - current_time
        if sleep_delta > TIME_PRECISION:
            time.sleep(sleep_delta)

        for msg in messages[key]:
            if msg.is_meta:
                continue

            # 输出声音
            if msg.type[:4] != 'fade' and audio_port is not None:
                audio_port.send(msg)

            # 将亮灯消息推入led线程的消息队列
            if msg.type[:4] == 'fade' or msg.type[:4] == 'note':
                msg_queue.put_nowait((key, msg))

            pass
        # 只有当同一时刻的亮灯消息都写入后才手动触发点亮动作
        msg_queue.put_nowait(('show', None))
        pass

    # 等待led线程终止
    logging.info('all messages sent.')
    msg_queue.put_nowait(('end', None))
    led_thread.join()

    logging.info('end play. real play time: %s seconds', timeit.default_timer() - start_timer)
    pass


def main():
    logging.basicConfig(level=LOG_LEVEL, format=LOG_FORMAT)
    args = parse_arguments()

    # 1. load midi file
    mid = mido.MidiFile(args.file)
    logging.info('<midi file {!r} type {}, {} tracks, {:.3f} seconds, {} messages>'.format(
        mid.filename, mid.type, len(mid.tracks), mid.length, sum([len(track) for track in mid.tracks])))

    # 2. set audio output
    out_port = None
    if args.port is not None:
        out_port = mido.open_output(args.port)
        logging.info('use audio output port: %s', out_port)
        # for msg in mid:
        #     time.sleep(msg.time)
        #     if not msg.is_meta:
        #         out_port.send(msg)
    else:
        logging.info('not audio output')

    # 3. start play
    led_play(mid, out_port)
    pass


if __name__ == "__main__":
    main()
