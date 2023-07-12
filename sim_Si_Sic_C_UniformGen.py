from Classes import * 
import matplotlib.pyplot as plt
import numpy as np
import time
from scipy import integrate

start_time = time.time()
# Generate materials
diamond = Diamond()
diamondPC = DiamondPC()
silicon = Silicon()
siliconCarbide = SiliconCarbide()

material = diamond
#$materials = [diamond]
#plt.figure()
#plt.title("Induced corrent on electrode")
#plt.xlabel("t(s)")
#plt.ylabel("Current")
#for material in materials:
# Generate geometry
detector = Geometry(700,700,500,material)
particleGen = GenerateCarriers(detector)
#detector.CreateUniformZElectricField(800)
Vbias = 800
detector.CreateUniformZElectricField(Vbias)
detector.CreatePlanarElectrodes()
dt = 0.001e-9
drift_model = CarrierDrift(detector, dt)

carriers = particleGen.GenerateUniformCarrierGeometry()
print("carriers pair number: ", len(carriers)/2)
#carriers = [Electron(0,0,0,0), Hole(0,0,0,0)]  
    
print("###################")
print("Start drifting carriers:")
print("Infos:")
print("Material: {0}\nDensity: {1} g/cm3\nElectron Mobility: {2} cm2/Vs \nElectron Mobility: {3} cm2/Vs".format(material.name, material.density, material.mu_e_300k, material.mu_h_300k)) 
print("Electron Saturation velocity = {0} cm/s".format(material.v_sat_e))
print("Hole Saturation velocity = {0} cm/s".format(material.v_sat_e))
for carrier in carriers:
    drift_model.DriftCarrier(carrier)
#materialName = detector.material.name
data_total = np.array(detector.electrodes[0].current_total_t)
t_y,t_x = data_total.T
data_elec = np.array(detector.electrodes[0].current_e_t)
e_y, e_x = data_elec.T
e_y, e_x = list(e_y), list(e_x)
data_hole = np.array(detector.electrodes[0].current_h_t)
h_y, h_x = data_hole.T
h_y, h_x = list(h_y), list(h_x)

print("Charge collected: Q = {0} fC".format(integrate.simpson(t_y,t_x)*1e15))
filename = "output_{0}_{1}V_{2}um_{3}ns_{4}.dat".format(detector.material.name, Vbias, detector.zLen*1e6, dt*1e9, particleGen.GenCarrierName)
print("Writing output on file: {0}".format(filename))
file = open(filename,"w")
    
#Writing material Chracteristics
file.write("###################\n")
file.write(detector.material.Info())
file.write("carriers pair number: {}\n".format(len(carriers)/2))
file.write("###################\n")
#Writing header 
file.write("Itotal(A) Ie(A) Ih(A) t(s)\n")
i = 0
while(i < len(t_y)):
    if (i >= len(e_y)): e_y.append(0)
    if (i >= len(h_y)): h_y.append(0)
    file.write("{0} {1} {2} {3}\n".format(t_y[i],e_y[i],h_y[i],t_x[i]))
    i += 1
#plt.xlabel("t(s)")
#plt.ylabel("I(A)")
#plt.plot(t_x, t_y, label="{0}".format(material.name))
#plt.plot(e_x,e_y, label = "$e^-$")
#plt.plot(h_x,h_y, label = "h")
#del detector
print("###################")

#plt.legend()
#plt.savefig("current.pdf")
#plt.close()
print("--- %s seconds---" % (time.time() - start_time))
