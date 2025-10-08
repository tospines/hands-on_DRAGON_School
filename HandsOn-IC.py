from pyhermes import *
from pyhermes.units import TeV, GeV, kpc, pc, deg, erg, sun_mass, m_proton,cm3

import numpy as np
import healpy
import matplotlib.pyplot as plt
import astropy.units as u


filename = '../../DRAGON2-Beta_version/output/3D_run.fits.gz'#DRAGON output file
dragon2D_leptons = cosmicrays.Dragon3D(filename,[Electron, Positron])#load particle population

kn_xsec = interactions.KleinNishina()#choose cross-sections for gamma-ray production
ISRF = photonfields.ISRF(0)


nside = 64#map resolution
sun_pos = Vector3QLength(8.3*kpc,0*kpc,0*kpc)#Earth's position in the Galaxy

integrator = InverseComptonIntegrator(dragon2D_leptons,ISRF,kn_xsec)#define the integrator
integrator.setupCacheTable(30, 30, 12)  # To be adjusted based on performance needs
integrator.setObsPosition(sun_pos)#introduce Earth's position in the integrator

skymap = GammaSkymap(nside, 10*GeV)#define the map that we want to compute
skymap.setIntegrator(integrator)#introduce the integrator into the map

mask = RectangularWindow(latitude=[5*deg, -5*deg],longitude=[15*deg, 125*deg])#if we want to calculate a portion of the sky to save time
skymap.setMask(mask)

skymap.compute()
	
output_file = f'!HandsOn/3D_run_IC.fits'
output = outputs.HEALPixFormat(output_file)#define the file to save the results
skymap.save(output)#save results
