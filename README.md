# py1900B

This Python module provides a wrapper for the serial interface of the BK Precision 1900B. With modification, it should
also be usable for models 1685B, 1687B, 1688B, 1901B and 1902B as they all share the command set from the
[programming manual](https://bkpmedia.s3.amazonaws.com/downloads/programming_manuals/en-us/1900B_Series_programming_manual.pdf)

## Use

```py
from py1900b import PowerSupply

# Establish connection
ps = PowerSupply("/dev/ttyUSB0")

# Get the current output voltage
voltage = ps.voltage

# Set the output voltage limit
ps.voltage = 15.2

# Get the current current limit
current_limit = ps.current_limit

# Disable the output
ps.enable_output(False)
```

## Limitations

When reading or setting values through the serial connection, the front panel knobs are unusable.
