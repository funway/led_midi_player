# LED MIDI Player

Lighting WS2812 LED strip by parsing a midi file on Raspberry Pi.

## Dependency

- rpi_ws281x 
- adafruit-circuitpython-neopixel
- mido
- python-rtmidi

```python
sudo pip3 install rpi_ws281x adafruit-circuitpython-neopixel mido python-rtmidi
```

## Hardware

- Raspberry Pi

- WS2812 LED strip ([taobao](https://item.taobao.com/item.htm?spm=a1z09.2.0.0.3fda2e8daeF7Er&id=522197656009&_u=61v2hvc1159))

  74 pixels/m or 144 pixels/m is better, but still has some disalignment to piano keys.

  I used 74 pixels/m strip and cut it to 12~15 pixels per segment, then soldering those segments by myself for aligning led pixel to piano key one by one.

- 5V 10A DC power supply ([taobao](https://item.taobao.com/item.htm?spm=a1z09.2.0.0.3fda2e8daeF7Er&id=557471244558&_u=61v2hvc4a6b))

- DC 5.5*2.5MM power jack socket connector ([taobao](https://item.taobao.com/item.htm?spm=a1z09.2.0.0.3fda2e8daeF7Er&id=40871207077&_u=61v2hvcaa1a))

- [bread board](https://detail.tmall.com/item.htm?id=41286068835&spm=a1z09.2.0.0.3fda2e8daeF7Er&_u=61v2hvcf4c3) and [wires](https://detail.tmall.com/item.htm?id=41251229542&spm=a1z09.2.0.0.3fda2e8daeF7Er&_u=61v2hvcd854) 

## Wiring Diagram

![](/images/Snipaste_2019-09-08_19-28-24.png)

![](/images/Snipaste_2019-09-08_19-28-44.png)

## Usage

`sudo python3 play.py -f music.mid [-p audio_port]`

