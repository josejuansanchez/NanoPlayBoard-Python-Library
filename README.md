# NanoPlayBoard-Python-Library
A Python Library for [NanoPlayBoard Firmata][1]. Using this library you can interact with your [NanoPlayBoard][2] writing Python code. It runs on Python 3.

## Installation

You can install it with [`pip`][3]:

```
pip3 install nanoplayboard
```

Or you can also install it from source with:

```
python3 setup.py install
```

You need to have [`setuptools`][4] installed.

## Usage

```python
from nanoplayboard.nanoplayboard import NanoPlayBoard
board = NanoPlayBoard()
board.rgb.on()
```

You can take a look at the examples folder to see how it works.

## Credits

`NanoPyMataCore` class is based on:
  - [pymata_core.py][5] developed by [Alan Yorinks][6].
  - [circuitplayground.py][7] developed by [Tony DiCola][8].

## License

```
Copyright 2016 Antonio Morales and José Juan Sánchez

Licensed under the GNU General Public License, Version 3 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.gnu.org/licenses/gpl-3.0.en.html

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
```

[1]: https://github.com/josejuansanchez/NanoPlayBoard-Firmata
[2]: http://nanoplayboard.org
[3]: https://pip.pypa.io/en/latest/
[4]: https://packaging.python.org/installing/
[5]: https://github.com/MrYsLab/pymata-aio/blob/master/pymata_aio/pymata_core.py
[6]: https://github.com/MrYsLab
[7]: https://github.com/adafruit/CircuitPlaygroundFirmata/blob/master/Python%20Examples/circuitplayground.py
[8]: https://github.com/tdicola
