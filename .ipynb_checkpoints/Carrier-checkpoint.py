class Carrier:
    def __init__(self, xo, yo, zo, trackID):
        self.x = xo
        self.y = yo
        self.z = zo
        self.trackID = trackID
        self.trackX = [xo]
        self.trackY = [yo]
        self.trackZ = [zo]
        self.charge = 0 # field movement orientation
        
    def Set_X(self, x):
        self.x = x
        self.trackX.append(x)
    
    def Set_Y(self, y):
        self.y = y
        self.trackY.append(y)
        
    def Set_Z(self, z):
        self.y = z
        self.trackZ.append(z) 
    
    def GetTrack(self):
        return self.trackX, self.trackY, self.trackZ
    
    def GetPos(self):
        return (self.x, self.y, self.z)
    
    def GetTrackID(self):
        return self.trackID
    
    def GetCharge(self):
        return self.charge
        
class Electron(Carrier):
    def __init__(self, xo, yo, zo, trackID):
        super().__init__(xo, yo, zo, trackID)
        self.charge = 1 
    
class Hole(Carrier):
    def __init__(self, xo, yo, zo, trackID):
        super().__init__(xo, yo, zo, trackID)
        self.charge = -1 