from pyhermes import *
from pyhermes.units import MHz, kpc

import numpy as np
import healpy
import matplotlib.pyplot as plt
import astropy.units as u


filename = '../../DRAGON2-Beta_version/output/BaseModel_DRAGONxsec.fits.gz'#DRAGON output file
dragon2D_leptons = cosmicrays.Dragon2D(filename,[Electron, Positron])#load particle population

bfield = magneticfields.PT11()

nside = 64#map resolution
sun_pos = Vector3QLength(8.3*kpc,0*kpc,0*kpc)#Earth's position in the Galaxy

integrator = SynchroIntegrator(bfield,dragon2D_leptons)#define the integrator
integrator.setupCacheTable(60, 60, 20)  # To be adjusted based on performance needs
integrator.setObsPosition(sun_pos)#introduce Earth's position in the integrator

skymap = RadioSkymap(nside,418*MHz)

skymap.setIntegrator(integrator)
skymap.compute()
	
output_file = f'!HandsOn/BaseModel_Synchro.fits'
output = outputs.HEALPixFormat(output_file)#define the file to save the results
skymap.save(output)#save results
