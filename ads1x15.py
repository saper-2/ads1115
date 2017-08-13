#!/usr/bin/python3

# -*- coding: utf-8 -*-
"""ADS1x15 control class

ADS1X15 class is a helper to interface with ADS1015/ADS1115 ADCs on I2C bus.
Class using generic SMBus library ( python3-smbus ) so it must be installed beforehand.

Check the code of ads1115_test.py for reference.

Todo:
	* ?

Credists:
	Me - saper_2 / 2017-08-13 :D

License:
	MIT

"""

import time
import smbus

class ADS1X15:
	def __init__(self, _piBus, _adsAddr=0x48, _type=1115):
		"""Initialize ADS1X15 interface class.
		
		Args:
			_piBus: Raspberry Pi I2C bus number
			_adsAddr: ADS1x15 I2C address (0x48 default for GY-ADS1115)
			_type: ADS1115 (1115) or ADS1015 (1015)
		
		Returns:
			none
		"""
		self.i2c = smbus.SMBus(int(_piBus))
		self.adsAddr = int(_adsAddr)
		self.adsType = int(_type)
		# init internal variables
		self.pgaVal = self.ADS_PGA_FS2048
		# self.pio = pigpio.pi()		
	
	#def __del__(self):
		#self.pio.stop()	
	
	# ***************************************************************************
	# ***************************************************************************
	# ***************************** CONSTANS ************************************
	# MUX setting
	ADS_MUX_IN0P_IN1N=0x00 # IN0=AIN+ , IN1=AIN-
	ADS_MUX_IN0P_IN3N=0x01 # IN0=AIN+ , IN3=AIN-
	ADS_MUX_IN1P_IN3N=0x02 # IN1=AIN+ , IN3=AIN-
	ADS_MUX_IN2P_IN3N=0x03 # IN2=AIN+ , IN3=AIN-
	ADS_MUX_IN0P_GNDN=0x04 # IN0=AIN+ , GND=AIN- (can only measure positive voltage on input)
	ADS_MUX_IN1P_GNDN=0x05 # IN1=AIN+ , GND=AIN- (can only measure positive voltage on input)
	ADS_MUX_IN2P_GNDN=0x06 # IN2=AIN+ , GND=AIN- (can only measure positive voltage on input)
	ADS_MUX_IN3P_GNDN=0x07 # IN3=AIN+ , GND=AIN- (can only measure positive voltage on input)
	# PGA setting
	ADS_PGA_FS6144=0x00 #6.144V
	ADS_PGA_FS4096=0x01 #4.096V
	ADS_PGA_FS2048=0x02 #2.048V
	ADS_PGA_FS1024=0x03 #1.024V
	ADS_PGA_FS0512=0x04 #0.512V
	ADS_PGA_FS0256=0x05 #0.256V
	ADS_PGA_FS0256_2=0x06 #0.256V (alternative option, no different from 0256 (0x05) )
	ADS_PGA_FS0256_3=0x07 #0.256V (alternative option, no different from 0256 (0x05) )
	# sampling mode (single/manual, continuous)
	ADS_MODE_CONTINUOUS=0x00 # continuous conversion mode
	ADS_MODE_POWER_DOWN_SINGLE_SHOT=0x01 # single-conversion mode (each conversion is started by SingleShot() (or writting 1 to bit OS)
	# data sampling rate
	ADS_DR_8SPS=0x00   # sampling data rate: 8 samples-per-sec
	ADS_DR_16SPS=0x01  # sampling data rate: 16 samples-per-sec
	ADS_DR_32SPS=0x02  # sampling data rate: 32 samples-per-sec
	ADS_DR_64SPS=0x03  # sampling data rate: 64 samples-per-sec
	ADS_DR_128SPS=0x04 # sampling data rate: 128 samples-per-sec
	ADS_DR_250SPS=0x05 # sampling data rate: 250 samples-per-sec
	ADS_DR_475SPS=0x06 # sampling data rate: 475 samples-per-sec
	ADS_DR_860SPS=0x07 # sampling data rate: 860 samples-per-sec
	# comparator queue
	ADS_COMP_QUE_1CONV=0x00   # Assert ALERT/RDY after 1 conversion
	ADS_COMP_QUE_2CONV=0x01   # Assert ALERT/RDY after 2 conversions
	ADS_COMP_QUE_4CONV=0x02   # Assert ALERT/RDY after 4 conversions
	ADS_COMP_QUE_DISABLE=0x03 # Disable comparator, and set ALERT/RDY to hi-state
	# comparator mode (hysteresis/Window)
	ADS_COMP_MODE_HYST=0   # Traditional comparator with hysteresis
	ADS_COMP_MODE_WINDOW=1 # Window comparator
	# comparator polarity
	ADS_COMP_POL_ACTIVE_LOW=0x00
	ADS_COMP_POL_ACTIVE_HIGH=0x01
	# Comparator latching mode	
	ADS_COMP_LAT_NON_LATCHING=0 # non-latching comparator mode
	ADS_COMP_LAT_LATCHING=1     # latchinng comparator mode (ALERT/RDY state is keep until Host will read conversion results from ADS)
	
	
	def ADSWriteWord(self, reg, val):
		"""Write 16bit value to ADS register
		
		Args:
			reg (int) - register number (0..3)
			val (word) - 2 byte (word) value of register in 
			
		Returns:
			none
		"""
		# swap byte order 
		v2 = ((val&0xff00)>>8) | ((val&0x00ff)<<8)
		reg = reg&0x03
		#print(":WORD_WR(reg={:02x},val={:04x}->{:04x})".format(reg, val,v2))
		self.i2c.write_word_data(self.adsAddr, reg, v2)
		return
		
	def ADSReadWord(self, reg):
		"""Read 16bit value from ADS register
		
		Args:
			reg (int) - register number (0..3)
			
		Returns:
			val (word) - 2 byte (word) value of register
		"""
		reg = reg & 0x03
		r = self.i2c.read_word_data(self.adsAddr, reg)
		# swap byte order 
		v = ((r&0xff00)>>8) | ((r&0x00ff)<<8)
		return v
	
	
	def ReadConfig(self):
		"""Read config reg.
		?.

		Args:


		Returns:
			
		"""
		r = self.ADSReadWord(0x01)
		return r
	
	def WriteConfig(self, val):
		self.ADSWriteWord(0x01, val)
		return
	
	def IsReady(self):
		"""Return if device not busy (OS bit)
		
		Args:
			none
		
		Returns:
			int: 1-Not busy , 0-busy
		"""
		r = self.ReadConfig()
		if (r & 0x8000):
			return 1
		
		return 0
	
	def SingleShot(self):
		"""Start single-shot conversion
		
		Args:
			none
			
		Returns:
			none
		"""
		r = self.ReadConfig()
		r |= 0x8000 # set bit OT
		self.WriteConfig(r)
		return
	
	def SetMux(self, mux):
		"""Select input and input mode for conversion.
		See constants ADS_MUX_INxP_xxxx
		
		Args:
			mux (int) - input and/or input mode (0x00..0x07)
		
		Returns:
			none
		"""
		mux = mux & 0x07
		
		r = self.ReadConfig()
		r &= 0x8FFF
		r |= ((mux<<12)&0x7000)
		self.WriteConfig(r)
		return
	
	def SetPGA(self, pga):
		"""Set Programmable gain amplifier (+/-6.144V .. +/-0.256V).
		Check constants ADS_PGA_FSxxxx
		Use this rutine to setup PGA because it'll also update internal (ads1x15 class) variable
		which hold the PGA setting for reading result value in mV by GetResultScaled
		
		Args:
			pga (int) - PGA scale (0x00..0x07)
		
		Returns:
			none
		"""
		pga &= 0x07
		self.pgaVal = pga # store PGA config
		r = self.ReadConfig()
		r &= 0xF1FF
		r |= ((pga<<9)&0x0E00)
		self.WriteConfig(r)
		return
	
	def SetMode(self, mode):
		"""Set mode of ADC converter. 
		Check constants ADS_MODE_xxxxx
		Continuous: mean that once conversion end, it is started again right on
		Single-shot: mean that each conversion must be started manually, and once is done, ADS11x5 goes into low power mode
		
		Args:
			mode (int) - conversion mode (0/1)
		
		Returns:
			none
		"""
		mode &= 0x01
		r = self.ReadConfig()
		if (mode == 0):
			# clear 8th bit
			r &= 0xFEFF
		else:
			# set 8th bit
			r |= 0x0100
		self.WriteConfig(r)
		return
	
	def SetDataRate(self, dr):
		"""Set how many samples are collected for each conversion. 
		Check constants ADS_DR_xxxxx
		
		Args:
			dr (int) - data rate (0x00..0x07)
		
		Returns:
			none
		"""
		dr &= 0x07
		r = self.ReadConfig()
		r &= 0xFF1F
		r |= ((dr<<5)&0x00E0)
		self.WriteConfig(r)
		return
	
	def ComparatorDisable(self):
		"""Disable comparator. 
		
		Args:
			none
		
		Returns:
			none
		"""
		r = self.ReadConfig()
		r |= 0x0003
		self.WriteConfig(r)
		return
	
	def ComparatorSetQueue(self, que):
		"""Set comparator queue or disable comparator. 
		Check constants ADS_COMP_QUE_xxxxx
		
		Args:
			que (int) - comp. queue (0x00..0x03)
		
		Returns:
			none
		"""
		que &= 0x03
		r = self.ReadConfig()
		r &= 0xFFFC
		r |= que
		self.WriteConfig(r)
		return
	
	def ComparatorSetMode(self, mode):
		"""Set comparator mode (to window or hyst. comparator). 
		Check constants ADS_COMP_MODE_xxxxx
		
		Args:
			mode (int) - comp. mode (0/1)
		
		Returns:
			none
		"""
		mode &= 0x01
		r = self.ReadConfig()
		if (mode == 0):
			# clear 4th bit
			r &= 0xFFEF
		else:
			# set 4th bit
			r |= 0x0010
		self.WriteConfig(r)
		return
	
	def ComparatorSetPolarity(self, pol):
		"""Set comparator output (ALERT/RDY) active state. 
		Check constants ADS_COMP_POL_ACTIVE_xxxxx
		
		Args:
			pol (int) - comp. out polarity (0/1)
		
		Returns:
			none
		"""
		pol &= 0x01
		r = self.ReadConfig()
		if (pol == 0):
			# clear 3rd bit
			r &= 0xFFF7
		else:
			# set 3rd bit
			r |= 0x0008
		self.WriteConfig(r)
		return
		
	def ComparatorSetLatching(self, lat):
		"""Set comparator latching mode. 
		Check constants ADS_COMP_LAT_xxxxx
		
		Args:
			lat (int) - comp. out polarity (0/1)
		
		Returns:
			none
		"""
		lat &= 0x01
		r = self.ReadConfig()
		if (lat == 0):
			# clear 2nd bit
			r &= 0xFFFB
		else:
			# set 2nd bit
			r |= 0x0004
		self.WriteConfig(r)
		return
	
	def SetThresholdLo(self,val):
		"""Set low threshold register value. 
		
		Args:
			val (word) - 16bit int value
		
		Returns:
			none
		"""
		val &= 0xffff
		self.ADSWriteWord(0x02, val)
		return
		
	def SetThresholdHi(self,val):
		"""Set high threshold register value. 
		
		Args:
			val (word) - 16bit int value
		
		Returns:
			none
		"""
		val &= 0xffff
		self.ADSWriteWord(0x03, val)
		return
		
	def GetThresholdLo(self):
		"""Read low threshold register value. 
		
		Args:
			none
		
		Returns:
			word - 16bit signed int
		"""
		r = self.ADSReadWord(0x02)
		return r
		
	def GetThresholdHi(self):
		"""Read high threshold register value. 
		
		Args:
			none
		
		Returns:
			word - 16bit signed int
		"""
		r = self.ADSReadWord(0x03)
		return r
		
	def GetResult(self):
		"""Read last conversion result. 
		
		Args:
			none
		
		Returns:
			word - 16bit signed int
		"""
		r = self.ADSReadWord(0x00);
		return r
		
	def ReadConfig2(self, pgaUpdate=1):
		"""Read config register and return it in list format.
		By default this also update class internal pga value for reading conversion 
		result in mV (GetResultScaled, ConvertResultToScaled)
		
		Args:
			pgaUpdate (int) - 1 = update internal PGA from ADS1115 (default)
							  0 = do not update PGA from ADS1115
		
		Returns:
			List of elements from config register
		"""
		r = self.ReadConfig()
		os = 1
		if (r & 0x8000):
			os=1
		else:
			os=0
			
		mux = (r & 0x7000) >> 11
		pga = (r & 0x0E00) >> 9
		mode = 1
		if (r & 0x0100):
			mode=1
		else:
			mode=0
			
		
		dr = (r & 0x00E0) >> 5
		
		comp_mode = 0
		if (r & 0x0010):
			comp_mode=1
		
		comp_pol=0
		if (r & 0x0008):
			comp_pol=1
		
		comp_lat=0
		if (r & 0x0004):
			comp_lat=1
		
		que = r & 0x0003
		# pack
		ar = {
			'os': os,
			'mux': mux,
			'pga': pga,
			'mode': mode,
			'dr':dr,
			'comp_mode': comp_mode,
			'comp_pol': comp_pol,
			'comp_lat': comp_lat,
			'comp_que': que,
			'raw': r
		}
		# update self.pgaVal
		if (pgaUpdate != 0):
			self.pgaVal = pga
			
		return ar

	def ConvertResultToScaled(self, res, pga=0xff):
		"""Read last conversion result, applay PGA setting, and return measured voltage in mV
		
		Args:
			res (word) - RAW result value of conversion (from GetResult)
			pga (byte) - PGA setting (0..7). If greater than 0x07 then pga setting will be used 
						 from internal variable which keep copy of pga value 
						 from SetPGA .
						 
		
		Returns:
			Measured voltage in mV (float) on selected input (MUX)
		"""
		r = res
		if (pga > 0x07): 
			pga = self.pgaVal
			
		if (pga == self.ADS_PGA_FS6144):
			fs = 6144
		elif (pga == self.ADS_PGA_FS4096 ):
			fs = 4096
		elif (pga == self.ADS_PGA_FS2048 ):
			fs = 2048
		elif (pga == self.ADS_PGA_FS1024 ):
			fs = 1024
		elif (pga == self.ADS_PGA_FS0512 ):
			fs = 512
		elif (pga == self.ADS_PGA_FS0256 ):
			fs = 256
		elif (pga == self.ADS_PGA_FS0256_2 ):
			fs = 256
		elif (pga == self.ADS_PGA_FS0256_3 ):
			fs = 256
		else:
			fs = 2048
			
		# 1LSB voltage from FS
		val = (fs/(2**15)) * r
		
		return val
	
	def GetResultScaled(self, pga=0xff):
		"""Read last conversion result, applay PGA setting, and return measured voltage in mV
		
		Args:
			pga (byte) - if greater than 0x07 then pga value will be used 
						 from internal variable which keep copy of pga value 
						 from SetPGA routine.
						 
		
		Returns:
			Measured voltage in mV(float) on selected input (MUX)
		"""
		r = self.GetResult()
		val = self.ConvertResultToScaled(r, pga)
		
		return val

