from enum import Enum

import serial

class SupplyMode(Enum):
    ConstantVoltage = 0
    ConstantCurrent = 1

class PowerSupply:
    """
    Represent a PowerSupply
    """
    
    def __init__(self,serial_string) -> None:
        """
        Initialise connection to power supply
        :param serial_string Path for serial port
        """
        self._serial = serial.Serial(serial_string)
    
    def _read_response(self):
        """
        Read a single line of response from the supply
        :returns The response from the supply
        """
        response = b""
        while True:
            response += self._serial.read()
            if chr(response[-1]) == '\r':
                return response.decode("UTF-8")
    
    def _send_command(self,command,expect_response=False):
        """
        Send a command to the supply
        :param command String containing the command to be sent (without '\r')
        :param expect_response Set to `True` if the power supply is expected to respond with a line before "OK\r"
        :returns The response string if expect_response=True, else None
        :raises Exception if expected response is not returned
        """
        self._serial.write(bytes(command + '\r',"UTF-8"))
        response = None
        if expect_response:
            response = self._read_response()
            if response == "OK\r":
                raise Exception(f"Command '{command}' did not return an expected response")
        check_ok = self._read_response()
        if check_ok != "OK\r":
            print(f"Warning: Command {command} did not return 'OK'")
        return response
    
    def get_display(self):
        """
        Get the current display values
        :returns A tuple of current display values of voltage, current and supply mode enum value
        """
        result = self._send_command("GETD",expect_response=True)
        voltage = int(result[0:4]) * 0.01
        current = int(result[4:8]) * 0.01
        status = SupplyMode.ConstantVoltage if int(result[8]) == 0 else SupplyMode.ConstantCurrent
        return (voltage,current,status)
    
    def get_settings(self):
        """
        Get the current voltage and current limit settings
        :returns A tuple of the current voltage and current limits
        """
        result = self._send_command("GETS",expect_response=True)
        voltage = int(result[0:3]) * 0.1
        current = int(result[3:6]) * 0.1
        return (voltage,current)
    
    @property
    def voltage(self):
        """
        The current display voltage
        Setting this property will set the output voltage limit
        :raises ValueError if set to unsupported voltage
        """
        return self.get_display()[0]
    
    @voltage.setter
    def voltage(self,value):
        self.voltage_limit = value

    @property
    def current(self):
        """
        The current display current
        Setting this property will set the output current limit
        :raises ValueError if set to unsupported current
        """
        return self.get_display()[1]
    
    @current.setter
    def current(self,value):
        self.current_limit = value
    
    @property
    def power(self):
        """
        The current output power (read-only)
        """
        voltage,current,_ = self.get_display()[1]
        return voltage*current
    
    @property
    def voltage_limit(self):
        """
        The current voltage limit
        Setting this property will set the output voltage limit
        :raises ValueError if set to unsupported voltage
        """
        return self.get_settings()[0]
    
    @voltage_limit.setter
    def voltage_limit(self,value):
        lower_limit = 0.8
        upper_limit = 16.2
        if value < lower_limit or value > upper_limit:
            raise ValueError(f"Supported voltage range is {lower_limit} to {upper_limit}")
        value = int(value * 10)
        self._send_command(f"VOLT{value:03d}")
     
    @property
    def current_limit(self):
        """
        The current current limit
        Setting this property will set the output current limit
        :raises ValueError if set to unsupported current
        """
        return self.get_settings()[1]
    
    @current_limit.setter
    def current_limit(self,value):
        lower_limit = 0.0
        upper_limit = 63.0
        if value < lower_limit or value > upper_limit:
            raise ValueError(f"Supported voltage range is {lower_limit} to {upper_limit}")
        value = int(value * 10)
        self._send_command(f"CURR{value:03d}")
    
    def enable_output(self,enable):
        """
        Enable or disable the power supply output
        :param enable Set to True to enable output, or False to disable
        """
        if enable:
            self._send_command("SOUT0")
        else:
            self._send_command("SOUT1")
    