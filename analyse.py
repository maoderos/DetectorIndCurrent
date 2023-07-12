import matplotlib.pyplot as plt
import numpy as np
from scipy import integrate

filename = 'output_Diamond SC_800V_500.0um_0.001ns_UniformMIP.dat'
I,Ie,Ih,t = np.loadtxt(filename, skiprows=12,unpack=True)

Qo = integrate.simpson(I,t) 

tauOverTr = [0.1,0.3,0.5,1]
tr = t[-1]

plt.figure()
plt.title("pc Diamond")
plt.xlabel("t (ns)")
plt.ylabel("A($\mu$A)")
for i in tauOverTr:
    I_pcvd = []
    j = 0
    tau = tr*i
    while (j < len(t)):
        newI = I[j]*np.exp(-t[j]/tau)
        I_pcvd.append(newI)
        j+= 1
    plt.plot(t,I_pcvd,label=r"$\tau$/Tr = {0}".format(i))


tauOverTr = np.arange(0.1,5,0.2)
#plt.plot(t,Ie,label="e$^-$ current")
#plt.plot(t,Ih,label="h current")
plt.legend()
plt.savefig("current_pcCVD.pdf")    
plt.close()

plt.figure()
plt.title("pc Diamond")
plt.xlabel(r"$\tau$/Tr")
plt.ylabel("Charge Collection Efficiency")
eff = []
for i in tauOverTr:
    I_pcvd = []
    j = 0
    tau = tr*i
    while (j < len(t)):
        newI = I[j]*np.exp(-t[j]/tau)
        I_pcvd.append(newI)
        j+= 1
    Qf = integrate.simpson(I_pcvd,t)
    eff.append(Qf/Qo)
    #plt.plot(t,I_pcvd,label=r"$\tau$/Tr = {0}".format(i))



#plt.plot(t,Ie,label="e$^-$ current")
plt.scatter(tauOverTr,eff)
plt.legend()
plt.savefig("cce.pdf")    
plt.close()

tau = 200
I_pcvd = []
j = 0
plt.figure()
plt.title("sc Diamond")
plt.xlabel("t (ns)")
plt.ylabel("A($\mu$A)")
while (j < len(t)):
    newI = I[j]*np.exp(-t[j]/tau)
    I_pcvd.append(newI)
    j+= 1
plt.plot(t,I_pcvd,label=r"scCVD - 200s Tau eff".format(i))
plt.savefig("scCVDwithexp.pdf")
plt.close()