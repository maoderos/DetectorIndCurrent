from Classes import * 
import matplotlib.pyplot as plt
import numpy as np
import time
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
    #particleGen = GenerateCarriers(detector)
    detector.CreateUniformZElectricField(500)
    detector.CreatePlanarElectrodes()
    drift_model = CarrierDrift(detector, 0.001e-9)

    #carriers = particleGen.GenerateUniformCarrierGeometry()
    carriers = []
    dz = 0.1 #um
    z = (detector.zLen*1e6)/2
    ID = 0
    while z > (-detector.zLen*1e6/2):
        z -= dz 
        #print(z)
        carriers.append(Electron(0,0,z,ID))
        carriers.append(Hole(0,0,z,ID))
        ID += 1
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

    plt.plot(t_x, t_y, label="{0}".format(materialName))
    plt.plot(e_x,e_y)
    plt.plot(h_x,h_y)
    del detector
    #del test_electron
    #del test_hole

plt.legend()
plt.savefig("current.pdf")
plt.close()
print("--- %s seconds---" % (time.time() - start_time))
