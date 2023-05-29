class GenerateCarriers:
    def __init__(self, geometry):
        self.carriers = []
        self.geometry = geometry 
        

    def GenerateUniformCarrierGeometry(self):
        # Starts at (0,0,-len/2) for simplicity (Improve later)
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
                self.carriers.append(Electron(positionX, positionY, z, N)) 
                self.carriers.append(Hole(positionX, positionY, z, N))
                N += 1
        return self.carriers
   