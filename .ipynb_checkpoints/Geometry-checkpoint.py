class Geometry:
    def __init__(self, xLen, yLen, zLen, material):
        # Start with fixed geoemtry to simplify and after making it more flexible
        self.xLen = xLen*1e-6 # um
        self.yLen = yLen*1e-6 # um
        self.zLen = zLen*1e-6# um
        self.ZLenElec = zLen/10
        self.material = material
        self.Efield = [0,0,0] 
    
        
    def CheckBoundary(self,carrierPosition):
        if abs(carrierPosition[0]) >= abs(self.xLen/2) or abs(carrierPosition[1]) >= abs(self.yLen/2) or abs(carrierPosition[2]) >= abs(self.zLen/2):
            return True
        else:
            return False
        
    def CreateUniformZElectricField(self, deltaV):
        # V in volts
        self.Efield = [0,0,-deltaV/(self.zLen*1e04)] # um to cm -> V/cm