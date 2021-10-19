**No further development because PIs (especially the SD card) dies too often if the powersupply is turned of without shutting the PI down before**
I ported everything to run on an ESP32, so there is no more SD card problem.

## PImatrix
This is a simple controller for a LED matrix using WS2811 LEDs and a RaspberryPI.
It was designed for a 13+25 x 8 matrix built into our stage back panel.

You can probably adjust it quite simple by modifying the matrix dimensions in led.py.

### Features
The main feature the ability to controll the matrix using ArtNet (e.g. QLCplus).
But there are also some prebuilt modes, which can be selected and configured:

* Basic modes:
  * Blackout
  * Static color (ArtNet)
  * Color fading
  * Rainbow fading
* Advanced modes:
  * VU meter
  * Spectrum analyzer
    * Multiple color modes for bars / spikes
    
## ArtNet
Universe can be modified in `server.py`

| Universe | Channel  | Payload                     |  Mode      |
|----------|----------|-----------------------------|------------|
|  1       |  1       | Mode                        |   -        |
|  1       |  2       | Brightness                  |  all       |
|  1       |  3       | Speed (0: slow, 255: fast)  |  all       |
|  1       |  4       | Color red                   |  all       |
|  1       |  5       | Color green                 |  all       |
|  1       |  6       | Color blue                  |  all       |
|  **1**   | **7-63** | **reserved for some modes** |  -         |
|  1       |  7       | Spectrum mode, see below    | `spectrum` |
|  1       |  8       | Number of bands for the spectrum analysis / FFT| `spectrum` |
|  1       |  9       | Text mode, see below        | `text`     |
|  1       |  32-64   | Text                        | `text`     |
|  1       |  110-255 | Static data `(R,G,B)`       | `static`   |
|  2       |  0-255   | Static data `(R,G,B)`       | `static`   |

### Modes
| Number | Mode     | Description                  |Optional arguments |
|--------|----------|------------------------------|-------------------|
|  0     | Blackout | Shut down LEDs               | -                 |
|  1     | Fade     | Color fade / wheel           | (only speed)      |
|  2     | Rainbow  | Rainbow fade                 | (only speed)      |
|  3     | Fish     | Fish tank                    | (only speed)      |
|  4     | Static   | Show static data             | Static data       |
|  5     | VU Meter | Show loudness of audio input | -                 |
|  6     | Spectrum | Show audio spectrum          | `mode`, `bands`   |
|  7     | Text     | Show text                    | `text`, `color`   |

#### Mode `Spectrum`

| `mode` | Description                             |
|--------|-----------------------------------------|
| `0`    | Default spectrum                        |
| `1`    | Same as `0` but without peaks           |
| `2`    | Rainbow colored spectrum (like `0`)     |
| `3`    | Same as `2` but without peaks           |
| `4`    | Rainbow colored spectrum bars           |
| `5`    | Same as `4` but without peaks           |
| `6`    | Endless horizontal spectrum (scrolling) |

#### Mode `Text`

| `mode` | Description                             |
|--------|-----------------------------------------|
| `0`    | Condensed RGB                           |
| `1`    | Condensed Rainbow                       |
| `127`  | Normal RGB                              |
| `128`  | Normal Rainbow                          |
