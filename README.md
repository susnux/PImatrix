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

| Universe | Channel | Payload                    |
|----------|---------|----------------------------|
|  1       |  1      | Mode                       |
|  1       |  2      | Brightness                 |
|  1       |  3      | Speed (0: slow, 255: fast) |
|  1       |  4-63   | reserved for some modes    |
|  1       |  64-255 | Static data `(R,G,B)`      |
|  2       |  0-255  | Static data `(R,G,B)`      |

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

Mode `Spectrum` has some custom arguments:
`mode` on channel 4 and `bands` on channel 5,
`bands` sets up the number of bands for the spectrum analysis / FFT.

| `mode` | Description                             |
|--------|-----------------------------------------|
| `0`    | Default spectrum                        |
| `1`    | Same as `0` but without peaks           |
| `2`    | Rainbow colored spectrum (like `0`)     |
| `3`    | Same as `2` but without peaks           |
| `4`    | Rainbow colored spectrum bars           |
| `5`    | Same as `4` but without peaks           |
| `6`    | Endless horizontal spectrum (scrolling) |
