from Classes import * 
import matplotlib.pyplot as plt
import numpy as np

# Generate materials
diamond = Diamond()
silicon = Silicon()
siliconCarbide = SiliconCarbide()

materials = [diamond, silicon, siliconCarbide]

plt.figure()
plt.title("Induced corrent on electrode")
plt.xlabel("t(s)")
plt.ylabel("Current")
for material in materials:
    # Generate geometry
    detector = Geometry(700,700,500,material)
    detector.CreateUniformZElectricField(500)
    detector.CreatePlanarElectrodes()
    drift_model = CarrierDrift(detector, 0.001e-9)

    test_electron = Electron(0,0,0,0)
    test_hole = Hole(0,0,0,0)
    
    drift_model.DriftCarrier(test_electron)
    drift_model.DriftCarrier(test_hole)
    
    materialName = detector.material.name
    data_total = np.array(detector.electrodes[0].current_total_t)
    t_y,t_x = data_total.T

    plt.plot(t_x, t_y, label="{0}".format(materialName))
    del detector
    del test_electron
    del test_hole

plt.legend()
plt.savefig("current.pdf")
plt.close()
# Generate Particles
#genParticles = GenerateCarriers(detector)
#genParticles.GenerateUniformCarrierGeometry()
#print(len(genParticles.carriers))
