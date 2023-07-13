from Classes import * 
import matplotlib.pyplot as plt
import numpy as np

# Generate materials
diamond = Diamond()
silicon = Silicon()
siliconCarbide = SiliconCarbide()

materials = [diamond]

e = 1.602e-19
for material in materials:
    # Generate geometry
    detector = Geometry(700,700,500,material)
    detector.CreateUniformZElectricField(500)
    detector.CreatePlanarElectrodes()
    particleGen = GenerateCarriers(detector)
    carriers = particleGen.GenerateGeant4Carrier("output_C_0.root")
    print(len(carriers)/2)
    print("charge: {0}".format((len(carriers)/2)*e))


# Plot carriers 1 positions
fig = plt.figure()
ax = fig.add_subplot(projection='3d')

for carrier in carriers:
    x = carrier.x*1e6
    y = carrier.y*1e6
    z = carrier.z*1e6
    ax.scatter(x, y, z)


plt.show()
