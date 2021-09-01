import head
import numpy as np
from configparser import ConfigParser
import os
import logging
config = ConfigParser()
config.read('config.ini')
savedir = config['Default']['savedir']

logging.basicConfig(level=logging.INFO, 
	format='%(asctime)s%(message)s \t')

def make_grid():
	X = np.linspace(10,30, num=int(config['Default']['num_grid_perdim'])) 
	Y = np.linspace(1e-3,1, num=int(config['Default']['num_grid_perdim']))
	grid = head.Grid(X,Y)
	np.savetxt(savedir+'grid.txt', grid, delimiter=',')
	
def make_target():
	sim = head.Emulator(n_structures=int(config['Modelling']['n_structures']))
	sim.make_structure(r_mu=float(config['Default']['r_mu']),
		r_sigma=float(config['Default']['r_sigma']))
	q, st = sim.get_saxs(n_samples=int(config['Modelling']['n_sas_samples']))
	wl, It = sim.get_spectrum(n_samples=int(config['Modelling']['n_uvvis_samples']))
	np.savetxt(savedir+'target_saxs.txt', st, delimiter=',')
	np.savetxt(savedir+'target_uvvis.txt', It, delimiter=',')
	np.savetxt(savedir+'q.txt', q, delimiter=',')
	np.savetxt(savedir+'wl.txt', wl, delimiter=',')
	
if __name__=='__main__':
	
	if  os.path.exists(savedir):
		logging.error('Required directory already exists...\n'
			'Confirm that this is not a duplicate run, manually delete the directory and re-run again')
	else:
		os.makedirs(savedir)
		logging.info('Made the directory for this experiment %s'%savedir)
		logging.info('Making the grid using')
		make_grid()
		logging.info('Making the target responses using the Emulator')
		make_target()
		config.set('BO', 'iteration', '0')
		with open('config.ini', 'w') as configfile:
			config.write(configfile)