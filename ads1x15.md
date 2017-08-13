# class ```ADS1X15```


## Constans
In class there are defined constans for most settings in config register.
Default values from ADS1115 are in **bold** .


### ConfigReg[14:12] = MUX[2:0] - Input multiplexer configuration
Constant|Value|Analog IN+|Analog IN-
--------|-----|----------|----------
**ADS_MUX_IN0P_IN1N**|**0x00**|IN0|IN1
ADS_MUX_IN0P_IN3N|0x01|IN0|IN3
ADS_MUX_IN1P_IN3N|0x02|IN1|IN3
ADS_MUX_IN2P_IN3N|0x03|IN2|IN3
ADS_MUX_IN0P_GNDN|0x04|IN0|GND
ADS_MUX_IN1P_GNDN|0x05|IN1|GND
ADS_MUX_IN2P_GNDN|0x06|IN2|GND
ADS_MUX_IN3P_GNDN|0x07|IN3|GND



### ConfigReg[11:9] = PGA[2:0] - Programmable gain amplifier
Constant|Value|Full scale voltage
--------|-----|------------------
ADS_PGA_FS6144|0x00|&plusmn;6.144V
ADS_PGA_FS4096|0x01|&plusmn;4.096V
**ADS_PGA_FS2048**|**0x02**|&plusmn;2.048V
ADS_PGA_FS1024|0x03|&plusmn;1.024V
ADS_PGA_FS0512|0x04|&plusmn;0.512V
ADS_PGA_FS0256|0x05|&plusmn;0.256V
ADS_PGA_FS0256_2|0x06|&plusmn;0.256V (*1
ADS_PGA_FS0256_3|0x07|&plusmn;0.256V (*1
(*1 - This is alternative option for ADS1115


### ConfigReg[8] = MODE[0] - Device operating mode
Constant|Value|Conversion mode
--------|-----|-----------
ADS_MODE_CONTINUOUS|0x00|Continuous
**ADS_MODE_POWER_DOWN_SINGLE_SHOT**|**0x01**|Single Shot (*1
(*1 - each conversion is started by ```SingleShot()``` (or writting 1 to bit OS)


### ConfigReg[7:5] = DR[2:0] - Data rate (data sampling rate)
Constant|Value|samples/sec (SPS)
-|-|-
ADS_DR_8SPS|0x00|8
ADS_DR_16SPS|0x01|16
ADS_DR_32SPS|0x02|32
ADS_DR_64SPS|0x03|64
**ADS_DR_128SPS**|**0x04**|128
ADS_DR_250SPS|0x05|250
ADS_DR_475SPS|0x06|475
ADS_DR_860SPS|0x07|860


### ConfigReg[4] = COMP_MODE[0] -Comparator mode
Constant|Value|Mode
-|-|-
**ADS_COMP_MODE_HYST**|**0**|Traditional comparator<br>with hysteresis
ADS_COMP_MODE_WINDOW|1|Window comparator


### ConfigReg[3] = COMP_POL[0] - Comparator polarity
Constant|Value|Description
-|-|-
**ADS_COMP_POL_ACTIVE_LOW**|**0x00**|Active low
ADS_COMP_POL_ACTIVE_HIGH|0x01|Active high


### ConfigReg[2] = COMP_LAT[0] - Latching comparator
Constant|Value|Description
-|-|-
**ADS_COMP_LAT_NON_LATCHING**|**0**|non-latching comparator mode
ADS_COMP_LAT_LATCHING|1|Latching comparator mode.<br>ALERT/RDY state is keep until Host will read conversion results from ADS


### ConfigReg[1:0] = COMP_QUE[1:0] - Comparator queue and disable
Comparator can be disabled by function ```ComparatorDisable()``` .
Constant|Value|Description
-|-|-
ADS_COMP_QUE_1CONV|0x00|Assert ALERT/RDY after 1 conversion
ADS_COMP_QUE_2CONV|0x01|Assert ALERT/RDY after 2 conversions
ADS_COMP_QUE_4CONV|0x02|Assert ALERT/RDY after 4 conversions
**ADS_COMP_QUE_DISABLE**|**0x03**|Disable comparator.<br>Set ALERT/RDY to hi-state



## Functions


### ```__init__(int _piBus, _adsAddr=0x48, _type=1115)```
This is called when class is created. 

Parameters:
- **_piBus** *int*<br>Raspberry Pi I2C bus for python3-smbus
- **_adsAddr** *byte*<br>ADS1115 I2C address in 7-bit notation (default: 0x48)
- **_type** *int*<br>ADS device type (for future use ; default: 1115=ADS1115)


### ```ReadConfig()```
Read a word (16bit unsigned int) from ADS1115 from register 0


### ```ReadConfig2(pgaUpdate=1)```
Return config register in List format with all config bits in corresponding list items.

Parameters:
- **pgaUpdate** *int* - 0..1 <br>Set to 0 to preven updating internal copy of PGA setting,<br>Set to 1 to update internal copy of PGA by PGA setting in ADS


### ```WriteConfig(val)```
Write configuration register (register 0) with value. ```val``` is truncated to 16bit.


### ```IsReady()```
Return ADS1115 status (bit OS from Config register):
- **1** - Device is ready (no conversion is running)
- **0** - Device performing conversion


### ```SingleShot()```
Perform a single-shot conversion. This can be done if device is in power down mode.


### ```SetMux(mux)```
Set input multiplexer for specified input.
This will alter MUX bits in config register.

Parameters:
- **mux** *int* - 0x00..0x07<br>See constans ```ADS_MUX_*```


### ```SetPGA(pga)```
Set programmable gain amplifier. This routine also keep copy of PGA settings in internal class variable for providing scaled ADC conversion result.

Parameters:
- **pga** *int* - 0x00..0x07<br>PGA bits setting, see constans: ```ADS_PGA_FS*```


### ```SetMode(mode)```
Set ADS operation mode (continuous conversion or power-down).
Alter MODE bit in config register.

Parameters:
- **mode** *int* - 0..1<br>operation mode, see ```ADS_MODE_*``` constans.


### ```SetDataRate(dr)```
Set sampling speed.
Will change bits DR in config register.

Parameters:
- **dr** *int* - 0x00..0x07<br>sampling speed, see constans: ```ADS_DR_xxSPS```


### ```ComparatorDisable()```
Disable comparator (no need to use ```ComparatorSetQueue(que)```).


### ```ComparatorSetQueue(que)```
Set comparator queue or disable.
Change bits COMP_QUE in config register.

Parameters:
- **que** *int* - 0x00..0x03<br>setup comp. queue, check constans ```ADS_COMP_QUE_*```


### ```ComparatorSetMode(mode)```
Set comparator mode to traditional comparator with hysteresis, or to window comparator.
Change bit COMP_MODE in config register.

Parameters:
- **mode** *int* - 0..1<br>Comparator mode, see constans ```ADS_COMP_MODE_*```


### ```ComparatorSetPolarity(pol)```
Set comparator polarity of ALERT/RDY pin.
Change bit COMP_POL in config register.
Parameters:
- **pol** *int* - 0..1<br>Active polarity state, see constans ```ADS_COMP_POL_ACTIVE_```


### ```ComparatorSetLatching(lat)```
Set comparator output ALERT/RDY pin latch mode.
Change bit COMP_LAT in config register.

Parameters:
- **lat** *int* - Latching/non-latching mode, see constans ```ADS_COMP_LAT_*```


### ```SetThresholdLo(val)```
Set ```Lo_thresh``` register with ```val```

Parameters:
- **val** *int16* - set threshold level


### ```SetThresholdHi(val)```
Set ```Hi_thresh``` register with ```val```

Parameters:
- **val** *int16* - set threshold level

### ```GetThresholdLo()```
Read ```Lo_thresh``` register.


### ```GetThresholdHi()```
Read ```Hi_thresh``` register.


### ```GetResult()```
Return (int16) RAW result from last conversion.


### ```ConvertResultToScaled(res, pga=0xff)```
Return raw conversion result in mV according to PGA settings. For proper work it require before to set PGA using ```SetPGA``` or reading PGA setting by ```ReadConfig2```

Parameters:
- **res** *int16* -<br>RAW conversion result from e.g. ```GetResult()```
- **pga** *byte* - 0x00..0x07 / 0xff<br>PGA setting (0x00..0x07), or to use internal copy of PGA leave 0xff (any value outside 0x00..0x07 range will force to use internal copy of PGA setting).


### ```GetResultScaled(pga=0xff)```
Read last ADC conversion result from ADS and convert it to mV according to ```pga``` parameter. If ```pga``` parameter is outside of PGA setting range (0x00..0x07) then internal copy of PGA will be used.

This is basically "combo" of functions:
1. ```raw=GetResult()```
2. ```ConvertResultToScaled(raw, pga)```

Parameters:
- **pga** *byte* - 0x00..0x07 / 0xff<br>PGA setting (0x00..0x07), or to use internal copy of PGA leave 0xff (any value outside 0x00..0x07 range will force to use internal copy of PGA setting).


## Direct-access functions
Library use 2 functions that allow to access 16bit regsiters in ADS1115.
The smbus library swap bytes in word so those function correct their order before calling smbus lib routines.


### ```ADSWriteWord(reg,val)```
Write a val word (16bit int) to register. ```reg``` and ```val``` are masked to it's length (2bit for reg, and 16bit val).

Parameters:
- **reg** *int* - 0x00..0x03<br>Register address
- **val** *int16* - 0x0000..0xFFFF<br>Register content


### ```ADSReadWord(reg)```
Read a word (16bit int) from ADS register. ```reg``` is masked to it's length (2bit).
Parameters:
- **reg** *int* - 0x00..0x03<br>Register address
