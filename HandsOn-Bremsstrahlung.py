from pyhermes import *
from pyhermes.units import TeV, GeV, kpc, pc, deg, erg, sun_mass, m_proton,cm3

import numpy as np
import healpy
import matplotlib.pyplot as plt
import astropy.units as u


filename = '../../DRAGON2-Beta_version/output/BaseModel_DRAGONxsec.fits.gz'#DRAGON output file
dragon2D_leptons = cosmicrays.Dragon2D(filename,[Electron, Positron])#load particle population

xsec = interactions.BremsstrahlungTsai74()
HI = neutralgas.RingModel(neutralgas.GasType.HI)



integrator = BremsstrahlungIntegrator(dragon2D_leptons,HI,xsec)#define the integrator


sun_pos = Vector3QLength(8.3*kpc,0*kpc,0*kpc)#Earth's position in the Galaxy
integrator.setupCacheTable(60, 60, 20)  # To be adjusted based on performance needs
integrator.setObsPosition(sun_pos)#introduce Earth's position in the integrator


nside = 128#map resolution
skymap_range = GammaSkymapRange(nside, 0.1*GeV,100*GeV,5)#define the map that we want to compute
skymap_range.setIntegrator(integrator)#introduce the integrator into the map

skymap_range.compute()

output_file = f'!HandsOn/BaseModel_brems.fits'
output = outputs.HEALPixFormat(output_file)#define the file to save the results
skymap_range.save(output)#save results
