# CLI for the [Donkey Republic](https://www.donkey.bike) API

API Reference: [https://sharedmobility.github.io/Donkey.html](https://sharedmobility.github.io/Donkey.html)

##  Usage
To get the nuber of available bikes for each hub within 800m of Moutstraat 88:
```bash
 donkapi "Moutstraat 88" -b 800
```

## Installation
Clone this repository and install via
```
pip install .
```

To install with an isolated virtual environment, [pipx](https://github.com/pypa/pipx) is recommended: 
```
pipx install .
```