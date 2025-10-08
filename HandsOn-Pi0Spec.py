from pyhermes import *
from pyhermes.units import TeV, GeV, kpc, pc, deg, erg, sun_mass, m_proton,cm3

import numpy as np
import healpy
import matplotlib.pyplot as plt
import astropy.units as u


filename = '../../DRAGON2-Beta_version/output/BaseModel_DRAGONxsec.fits.gz'#DRAGON output file
dragon2D_nuclei = cosmicrays.Dragon2D(filename,[Proton, Helium])#load particle population

xsecs = interactions.Kamae06Gamma()#choose cross-sections for gamma-ray production

gas_models = {#   target fields
	'HI': neutralgas.RingModel(neutralgas.GasType.HI),
	'H2': neutralgas.RingModel(neutralgas.GasType.H2)
}


nside = 64#map resolution
sun_pos = Vector3QLength(8.3*kpc,0*kpc,0*kpc)#Earth's position in the Galaxy


for name, gas_model in gas_models.items():

	integrator = PiZeroIntegrator(dragon2D_nuclei,gas_model,xsecs)#define the integrator
	integrator.setupCacheTable(60, 60, 20)  # To be adjusted based on performance needs
	integrator.setObsPosition(sun_pos)#introduce Earth's position in the integrator

	skymap_range = GammaSkymapRange(nside, 1*GeV,100*GeV,11)#define the map that we want to compute
	skymap_range.setIntegrator(integrator)#introduce the integrator into the map

	skymap_range.compute()
	
	output_file = f'!HandsOn/BaseModel_pi0spec_{name}.fits'
	output = outputs.HEALPixFormat(output_file)#define the file to save the results
	skymap_range.save(output)#save results
