import time

from py1900b import PowerSupply, SupplyMode

ps = PowerSupply("/dev/ttyUSB0")

lastDisplayTime = 0

busyIndicator = '-'

busyIndicatorIdx = 0
busyArray = [ '-','\\','|','/' ]

def updateBusyIndicator():
    global busyIndicatorIdx
    global busyIndicator
    busyIndicatorIdx = (busyIndicatorIdx + 1) % 4
    busyIndicator = busyArray[busyIndicatorIdx]


while True:
    currentTime = time.time()
    if currentTime - lastDisplayTime >= 0.25:
        voltage,current,mode = ps.get_display()
		
        cv = '\u2022' if mode == SupplyMode.ConstantVoltage else '\u25E6'
        cc = '\u2022' if mode == SupplyMode.ConstantCurrent else '\u25E6'
        
        print(f"{busyIndicator} Voltage: {voltage:5.2f}V Current: {current:5.2f}A CV:{cv} CC:{cc}\r",end='')
        updateBusyIndicator()
        lastDisplayTime = currentTime
