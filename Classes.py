import numpy as np

class Carrier:
    def __init__(self, xo, yo, zo, trackID):
        self.x = xo*1e-6 #um
        self.y = yo*1e-6 #um
        self.z = zo*1e-6 #um
        self.t = [0]
        self.trackID = trackID
        self.track = [[self.x,self.y,self.z]]
        self.velocity = []
        self.charge = 0 # field movement orientation
        
    def SetNewPosition(self, x, y, z):
        self.track.append([x,y,z])
    
    def GetPosition(self):
        return (self.track)
    
    def GetVelocity(self):
        return (self.velocity)
    
    def GetTrackID(self):
        return self.trackID
    
    def GetCharge(self):
        return self.charge
        
class Electron(Carrier):
    def __init__(self, xo, yo, zo, trackID):
        super().__init__(xo, yo, zo, trackID)
        self.charge = -1.602e-19
    
class Hole(Carrier):
    def __init__(self, xo, yo, zo, trackID):
        super().__init__(xo, yo, zo, trackID)
        self.charge = 1.602e-19

class Material:
    def __init__(self, name, density, mu_e, mu_h, v_sat, av_eh_energy, elecHoleNumber_MIP):
        self.density = density # g/cm3 
        self.mu_e_300k = mu_e # cm2/Vs
        self.mu_h_300k = mu_h # cm2/Vs
        self.v_sat = v_sat*10e2 # cm/s
        self.av_eh_energy = av_eh_energy # eV
        self.elecHoleNumber_MIP = elecHoleNumber_MIP # N/um
        
    def GetMu_e_300k(self):
        return self.mu_e_300k
    
    def GetMu_h_300k(self):
        return self.mu_h_300k
    
    def GetDensity(self):
        return self.density
    
    def GetVSaturation(self):
        return self.v_sat
    
    def GetElecHoleNumber_MIP(self):
        return self.elecHoleNumber_MIP
    
class Silicon(Material):
    def __init__(self):
        self.name = "Silicon"
        self.density = 2.33 # https://doi.org/10.3389/fphy.2022.898833
        self.mu_e_300k = 1450
        self.mu_h_300k = 450
        self.v_sat = 0.8e07
        self.av_eh_energy = 3.6
        self.elecHoleNumber_MIP = 89 # DOI: 10.1109/TNS.2004.825095
        
class SiliconCarbide(Material):
    def __init__(self):
        self.name = "Silicon Carbide"
        self.density = 3.22 # https://doi.org/10.3389/fphy.2022.898833
        self.mu_e_300k = 800
        self.mu_h_300k = 115
        self.v_sat = 2e07
        self.av_eh_energy = 7.6
        self.elecHoleNumber_MIP = 55 # DOI: 10.1109/TNS.2004.825095
        
class Diamond(Material):
    def __init__(self):
        self.name = "Diamond"
        self.density = 3.51 # https://doi.org/10.3389/fphy.2022.898833
        self.mu_e_300k = 1800
        self.mu_h_300k = 1200
        self.v_sat = 2.2e07
        self.av_eh_energy = 13
        self.elecHoleNumber_MIP = 37 #26/06/2017 CERN-THESIS-2017-487
            
class Geometry:
    def __init__(self, xLen, yLen, zLen, material):
        # Start with fixed geoemtry to simplify and after making it more flexible
        self.xLen = xLen*1e-6 # um
        self.yLen = yLen*1e-6 # um
        self.zLen = zLen*1e-6# um
        self.ZLenElec = zLen/10
        self.material = material
        self.Efield = [0,0,0] 
        self.electrodes = []
    
        
    def CheckBoundary(self,carrierPosition):
        if abs(carrierPosition[0]) >= abs(self.xLen/2) or abs(carrierPosition[1]) >= abs(self.yLen/2) or abs(carrierPosition[2]) >= abs(self.zLen/2):
            return True
        else:
            return False
        
    def CreateUniformZElectricField(self, deltaV):
        # V in volts
        self.Efield = [0,0,-deltaV/(self.zLen*1e04)] # um to cm -> V/cm
        
    def CreatePlanarElectrodes(self):
        self.electrodes.append(PlanarElectrode(self.zLen/2, self.zLen/10, self.zLen, 1))
        self.electrodes.append(PlanarElectrode(-self.zLen/2, self.zLen/10, self.zLen, 2))
        
class CarrierDrift:
    def __init__(self, geometry, dt):
        self.geometry = geometry 
        self.dt = dt
        
    def ElectrodeIndCurrent(self, carrier):
        # Calculate induced current with Shockley-Ramo Theorem in each electrode.
        for electrode in self.geometry.electrodes:
            v = carrier.velocity[-1]
            Wfield = electrode.WeightingField(electrode)
            Wfield_v = 0
            j = 0
            while(j < 3):
                Wfield_v += v[j]*Wfield[j]
                j += 1
            i = abs(carrier.charge)*Wfield_v
            if (carrier.charge < 0):
                if (len(carrier.velocity) > len(electrode.current_e_t)):
                    electrode.current_e_t.append([i,len(carrier.velocity)*self.dt])
                    
                else:
                    electrode.current_e_t[len(carrier.velocity) - 1][0] += i
            else:
                if (len(carrier.velocity) > len(electrode.current_h_t)):
                    electrode.current_h_t.append([i,len(carrier.velocity)*self.dt])
                    
                else:
                    electrode.current_h_t[len(carrier.velocity) - 1][0] += i
                    
            if (len(carrier.velocity) > len(electrode.current_total_t)):
                electrode.current_total_t.append([i,len(carrier.velocity)*self.dt])
            else:
                electrode.current_total_t[len(carrier.velocity) - 1][0] += i
                
                    
    def DriftCarrier(self, carrier):
        # carrier
        isParticleInBoundary = self.geometry.CheckBoundary(carrier.track[-1])
        n = 0
        while(isParticleInBoundary == False):
            E = self.geometry.Efield
            v_sat = self.geometry.material.v_sat
            if carrier.charge < 0:
                signal = -1
                mu = self.geometry.material.mu_e_300k
                v = [(mu*E[0]/(np.sqrt(1 + (mu*E[0]/v_sat)**2))),(mu*E[1]/(np.sqrt(1 + (mu*E[1]/v_sat)**2))),(mu*E[2]/(np.sqrt(1 + (mu*E[2]/v_sat)**2)))]
            elif carrier.charge > 0:
                signal = 1
                mu = self.geometry.material.mu_h_300k
                v = [(mu*E[0]/((1 + (mu*E[0]/v_sat)**2))),(mu*E[1]/((1 + (mu*E[1]/v_sat)**2))),(mu*E[2]/((1 + (mu*E[2]/v_sat)**2)))]
        
            newPosition = [(carrier.track[-1][0] + signal*v[0]*self.dt), (carrier.track[-1][1] + signal*v[1]*self.dt), (carrier.track[-1][2] + signal*v[2]*self.dt)]
            isParticleInBoundary = self.geometry.CheckBoundary(newPosition)
            if(isParticleInBoundary == False):
                carrier.track.append(newPosition)
                carrier.velocity.append(v)
                self.ElectrodeIndCurrent(carrier)
                n += 1
                #print(newPosition[2])
            else:
                print("Done drifting")
                print(n)
    
                      
class GenerateCarriers:
    def __init__(self, geometry):
        self.carriers = []
        self.geometry = geometry 
        
    def GenerateUniformCarrierGeometry(self):
        # Starts at (0,0,-len/2) for simplicity (Improve later)
        ## NEED REVIEW
        positionY = 0
        positionX = 0
        initialPosZ = self.geometry.zLen/2
        finalPosZ = -self.geometry.zLen/2
        dz = (self.geometry.zLen/10)
        N_eh = int(self.geometry.material.elecHoleNumber_MIP*dz*1e06)
        z = initialPosZ
        while(z > finalPosZ):
            N = 1
            z -= dz
            while N < N_eh: #generate N_eh carrier at the point
                self.carriers.append(Electron(positionX*1e6, positionY*1e6, z*1e6, N)) 
                self.carriers.append(Hole(positionX*1e6, positionY*1e6, z*1e6, N))
                N += 1
        return self.carriers
   

class PlanarElectrode:
    def __init__(self, z, width, d, electrodeId):
        self.width = width
        self.d = d*1e04 # um to cm
        self.electrodeId = electrodeId
        self.current_e_t = [] # C/s = A
        self.current_h_t = [] #C/s = A
        self.current_total_t = []
        
    # Need improvements
    def WeightingField(self, electrode, x=0,y=0,z=0,):
        # MELHORAR
        if (self.electrodeId == 1):
            return [0,0,-1/(self.d)]
        else:
            return [0,0,1/(self.d)]
        

    


    
