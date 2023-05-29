import numpy as np

class CarrierDrift:
    def __init__(self, geometry, dt):
        self.geometry = geometry 
        self.dt = dt
        
    def DriftCarrier(self, carrier):
        # carrier
        isParticleInBoundary = self.geometry.CheckBoundary(carrier.track[-1])
        while(isParticleInBoundary == False):
            E = self.geometry.Efield
            v_sat = self.geometry.material.v_sat
            if carrier.charge == -1:
                mu = self.geometry.material.mu_e_300k
                v = [(mu*E[0]/(np.sqrt(1 + (mu*E[0]/v_sat)**2))),(mu*E[1]/(np.sqrt(1 + (mu*E[1]/v_sat)**2))),(mu*E[2]/(np.sqrt(1 + (mu*E[2]/v_sat)**2)))]
            elif carrier.charge == 1:
                mu = self.geometry.material.mu_h_300k
                v = [(mu*E[0]/((1 + (mu*E[0]/v_sat)**2))),(mu*E[1]/((1 + (mu*E[1]/v_sat)**2))),(mu*E[2]/((1 + (mu*E[2]/v_sat)**2)))]
        
            newPosition = [(carrier.track[-1][0] + carrier.charge*v[0]*self.dt), (carrier.track[-1][1] + carrier.charge*v[1]*self.dt), (carrier.track[-1][2] + carrier.charge*v[2]*self.dt)]
            isParticleInBoundary = self.geometry.CheckBoundary(newPosition)
            if(isParticleInBoundary == False):
                carrier.track.append(newPosition)
            else:
                print("Done drifting")