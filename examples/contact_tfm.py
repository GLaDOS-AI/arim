#!/usr/bin/env python3
# encoding: utf-8
"""
This script shows how to perform a basic contact TFM with arim.
"""

import arim, arim.io, arim.signal, arim.im.tfm
import arim.plot as aplt

import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

from pprint import pprint as pp

#%% Figure parameters

mpl.rcParams['image.cmap'] = 'viridis'

#%% Load datafile (exported from BRAIN)

expdata_filename = r'O:\arim-datasets\Aluminium_Notch_Contact_128elts_5MHz\above_notch.mat'
frame = arim.io.load_expdata(expdata_filename)

print('Frame:')
pp(frame.metadata)
print(frame)
print()
print('Probe:')
print(frame.probe)
pp(frame.probe.metadata)

#%% Plot Bscans (unfiltered)

aplt.plot_bscan_pulse_echo(frame)
plt.draw()

#%% Filter data

filt = arim.signal.Hilbert() + \
       arim.signal.ButterworthBandpass(order=5, cutoff_min=0.5e6, cutoff_max=6e6, time=frame.time)
frame_raw = frame
frame = frame_raw.apply_filter(filt)

#%% Plot scanlines
plt.figure()
tx, rx = (19, 19)
plt.plot(frame_raw.time.samples, frame_raw.get_scanline(tx, rx), label='raw')
plt.plot(frame.time.samples, np.abs(frame.get_scanline(tx, rx)), label='filtered')
plt.gca().xaxis.set_major_formatter(aplt.micro_formatter)
plt.gca().xaxis.set_minor_formatter(aplt.micro_formatter)
plt.xlabel('time (µs)')
plt.ylabel('amplitude (1)')
plt.legend()
plt.title('Scanlines tx={} rx={}'.format(tx, rx))
plt.draw()

#%% Perform TFM:
grid = arim.geometry.Grid(xmin=-20e-3, xmax=20e-3,
                          ymin=0., ymax=0.,
                          zmin=0., zmax=50e-3,
                          pixel_size=0.15e-3)
speed = frame.examination_object.material.longitudinal_vel
tfm = arim.im.tfm.contact_tfm(frame, grid, speed)

#%% Plot TFM in linear scale

func_res = lambda x: np.real(x)
aplt.plot_tfm(tfm, func_res=func_res)
plt.title('TFM image - linear scale')
plt.axis('tight')


#%% Plot TFM in dB scale

clim = [-40, 0]
func_res = lambda x: arim.ut.decibel(x)
aplt.plot_tfm(tfm, func_res=func_res, interpolation='none', clim=clim)
plt.title('TFM image - dB scale')
plt.axis('tight')

# Block script until windows are closed.
plt.show()
