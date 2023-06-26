from Classes import * 
import matplotlib.pyplot as plt
import numpy as np
import time
from scipy import integrate

start_time = time.time()
# Generate materials
diamond = Diamond()
silicon = Silicon()
siliconCarbide = SiliconCarbide()

#materials = [diamond, silicon, siliconCarbide]
materials = [diamond]
plt.figure()
plt.title("Induced corrent on electrode")
plt.xlabel("t(s)")
plt.ylabel("Current")
for material in materials:
    # Generate geometry
    detector = Geometry(700,700,500,material)
    particleGen = GenerateCarriers(detector)
    detector.CreateUniformZElectricField(800)
    detector.CreatePlanarElectrodes()
    drift_model = CarrierDrift(detector, 0.001e-9)

    carriers = particleGen.GenerateUniformCarrierGeometry()
    print("carriers pair number: ", len(carriers)/2)
  
    ''' VERBOSITY 
    position = []
    for carrier in carriers:
        z_pos = carrier.track[-1][2]*1e6
        if z_pos not in position:
            position.append(z_pos)
    print(position)
    '''
    for carrier in carriers:
        drift_model.DriftCarrier(carrier)
    materialName = detector.material.name
    data_total = np.array(detector.electrodes[0].current_total_t)
    t_y,t_x = data_total.T
    data_elec = np.array(detector.electrodes[0].current_e_t)
    e_y, e_x = data_elec.T
    data_hole = np.array(detector.electrodes[0].current_h_t)
    h_y, h_x = data_hole.T
    

    print("Charge collected: Q = {0} fC".format(integrate.simpson(t_y,t_x)*1e15))
    plt.xlabel("t(s)")
    plt.ylabel("I(A)")
    plt.plot(t_x, t_y, label="total current")
    plt.plot(e_x,e_y, label = "$e^-$")
    plt.plot(h_x,h_y, label = "h")
    #plt.ylim(bottom=0)
    #plt.xlim(bottom=0)
    #plt.grid()
    del detector
    #del test_electron
    #del test_hole

plt.legend()
plt.savefig("current.pdf")
plt.close()
print("--- %s seconds---" % (time.time() - start_time))
