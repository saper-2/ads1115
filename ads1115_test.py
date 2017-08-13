#!/usr/bin/python3

from time import sleep
import struct
from ads1x15 import ADS1X15

#bus = smbus.SMBus(1)


def byte_array_to_string(ar):
	s = ""
	for a in ar:
		s += "{:02X} ".format(a)
	return s

	
def print_config(r):
	print("ADS1x15 Config Register:")
	if (r & 0x8000):
		print("   OS[1]        =1 (NoConv)")
	else:
		print("   OS[1]        =0 (PerfConv)")
		
	mux = (r & 0x7000) >> 11
	print("   MUX[2:0]     =0b{:03b} ".format(mux), end='')
	
	if (mux == 0b000):
		print(" (A0=IN+ A1=IN-)")
	elif (mux == 0b001):
		print(" (A0=IN+ A3=IN-)")
	elif (mux == 0b010):
		print(" (A1=IN+ A3=IN-)")
	elif (mux == 0b011):
		print(" (A2=IN+ A3=IN-)")
	elif (mux == 0b100):
		print(" (A0=IN+ GND=IN-)")
	elif (mux == 0b101):
		print(" (A1=IN+ GND=IN-)")
	elif (mux == 0b110):
		print(" (A2=IN+ GND=IN-)")
	elif (mux == 0b111):
		print(" (A3=IN+ GND=IN-)")
	else:
		print(" (what?)")
	
	pga = (r & 0x0E00) >> 9
	print("   PGA[2:0]     =0b{:03b} ".format(pga), end='')
	if (pga == 0b000):
		print(" (FS=6.144V)")
	elif (pga == 0b001):
		print(" (FS=4.096V)")
	elif (pga == 0b010):
		print(" (FS=2.048V)")
	elif (pga == 0b011):
		print(" (FS=1.024V)")
	elif (pga == 0b100):
		print(" (FS=0.512V)")
	elif (pga == 0b101):
		print(" (FS=0.256V)")
	elif (pga == 0b110):
		print(" (FS=0.256V)")
	elif (pga == 0b111):
		print(" (FS=0.256V)")
	else:
		print(" (what?)")
	
	if (r & 0x0100):
		print("   MODE[1]      =1 (Power down - single shot mode)")
	else:
		print("   MODE[1]      =0 (continuous mode)")
		
	
	dr = (r & 0x00E0) >> 5
	print("   DR[2:0]      =0b{:03b} ".format(dr), end='')
	if (dr == 0b000):
		print(" (8S/s)")
	elif (dr == 0b001):
		print(" (16S/s)")
	elif (dr == 0b010):
		print(" (32S/s)")
	elif (dr == 0b011):
		print(" (64S/s)")
	elif (dr == 0b100):
		print(" (128S/s)")
	elif (dr == 0b101):
		print(" (250S/s)")
	elif (dr == 0b110):
		print(" (475S/s)")
	elif (dr == 0b111):
		print(" (860S/s)")
	else:
		print(" (what?)")
	
	if (r & 0x0010):
		print("   COMP_MODE[1] =1 (Comparator with hyst.)")
	else:
		print("   COMP_MODE[1] =0 (Window comp.)")
	
	if (r & 0x0008):
		print("   COMP_POL[1]  =1 (Compa. active out level LOW)")
	else:
		print("   COMP_POL[1]  =0 (Compa. active out level HIGH)")
	
	if (r & 0x0004):
		print("   COMP_LAT[1]  =1 (Non-latching comp.)")
	else:
		print("   COMP_LAT[1]  =0 (Latching comp.)")
	
	que = r & 0x0003
	print("   COMP_QUE[1:0]=0b{:02b} ".format(que), end='')
	
	if (que == 0b00):
		print(" (Assert after 1conv)")
	elif(que == 0b01):
		print(" (Assert after 2conv)")
	elif(que == 0b10):
		print(" (Assert after 4conv)")
	elif(que == 0b11):
		print(" (Comp. disabled)")
	else:
		print(" (what?)")
		
	return

def signed16(v):
	# get rid of everything beyond 16bit
	v &= 0xffff;
	r = 65536;
	if ((v & 0x8000) == 0x8000):
		# negative number
		r = v - (1<<16)
	else:
		r = v&0x7fff;
	
	return r

def signed16b(v,bits=15):
	# get rid of everything beyond 16bit
	v &= 0xffff;
	mask = 0xffff >> (16-bits);
	r = 65536;
	if ((v & 0x8000) == 0x8000):
		# negative number
		r = v - (1<<(bits+1))
	else:
		r = v&mask;
	
	return r

ads = ADS1X15(1) #Pi I2C Bus 1

r = ads.ReadConfig()

print("ADS1115 CONF_REG= 0x{:04X}".format(r))
print_config(r)

t1=ads.GetThresholdHi()
t2=ads.GetThresholdLo()
v1 = signed16(t1)
v2 = signed16(t2)
print("Threshold Hi: 0x{:04X} {:n}".format(t1, v1 ))
print("Threshold Lo: 0x{:04X} {:n}".format(t2, v2 ))


print("Set Threshold Hi to 0x2222")
ads.SetThresholdHi(0x2222)
print("Set Threshold Lo to 0x8444")
ads.SetThresholdLo(0x8444)

t1=ads.GetThresholdHi()
t2=ads.GetThresholdLo()
v1 = signed16(t1)
v2 = signed16(t2)
print("Threshold Hi 2: 0x{:04X} {:n}".format(t1, v1 ))
print("Threshold Lo 2: 0x{:04X} {:n}".format(t2, v2 ))

print("ReadConfigNice result: ");
cfg = ads.ReadConfigNice()
print(cfg)

print("Set up for: MUX= IN+=IN1 IN-=GND , PGA: FS=4.096V (Vcc=3,3V) , DR=64SPS , MODE=continuous")
ads.SetDataRate(ads.ADS_DR_64SPS) #data rate
ads.SetPGA(ads.ADS_PGA_FS4096) # PGA
ads.SetMux(ads.ADS_MUX_IN1P_GNDN) # mux
ads.SetMode(ads.ADS_MODE_CONTINUOUS) # mode
# re-read config
cfg = ads.ReadConfigNice()
print("New config: reg=0x{:04x} / {}".format(cfg['raw'], cfg))

while True:
	# 64 samples/sec = 15,625ms => 20ms
	sleep(0.200) # 200ms delay
	res = ads.GetResult()
	s = ads.ConvertResultToScaled(res)
	print("ADC IN1: hex={:04x} dec={:05d} Volt={}mV".format(res, res, s))



