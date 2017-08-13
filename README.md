# ADS1115
I have created a class ads1x15 for accessing ADS111x chips.
Tested only on ADS1115 but should work with any ADS111x - only you have to remember MUX limits for other devices.
I license my code uder MIT license so u can do what want with it :)

# Pre-req.
Lib require smbus for python3 so it need to be installed beforehand.
On RPi:
```pi@raspberrypi:~ $ sudo apt install python3-smbus```

# To-Do
Very short list todo:
* Support for ADS1015 (12bit ADC)

# Class interface:
See: [ads1x15.md](ads1x15.md)

# EOF