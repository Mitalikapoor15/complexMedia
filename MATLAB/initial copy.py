import numpy as np
import matplotlib
import matplotlib.pyplot as plt

#1. Generating a matrix similar to the resolution of the SLM device - we are using HAMAMATSU LSH0805097
#Resolution: 600 x 800
H = 600 #horizontal pixels
V = 800 #vertical pixels

x = np.arange(-H/2,H/2-1,1)
y = np.arange(-V/2,V/2-1,1)

xv,yv = np.meshgrid(x,y) #surface area for the hologram - should be similar to that of SLMs resolution

phi = np.angle(xv + 1j * yv, deg=False) #azimuthal angle 
l = 1 #topological charge
# print(phi)
nx = 100 #number of horizontal and vertical grooves
ny = 100

gx = nx/H
gy = nx/V

plt.plot(xv,yv, marker='o', color='r', linestyle='none')
plt.show()

# plt.imshow(x,y)
#2. Now that we have made a mesh similar to the size of the SLM screen, we encode a hologram on to it.
#1. Vortex Beam
Hol_vortex = np.mod(-l*phi+2*np.pi*(gy*yv + gx*xv),2*np.pi)

SLM_vortex = Hol_vortex/np.max(Hol_vortex) * 255 #grayscale normalisation

print(SLM_vortex[:5])
plt.imshow(SLM_vortex)
plt.show()
print(matplotlib.get_backend())
#3. Plotting the hologram on the second screen (the SLM)
fig = plt.figure(1)

# Get the figure manager
manager = plt.get_current_fig_manager()

# Set window position if supported by the backend
if hasattr(manager, "window"):
    window = manager.window
    if hasattr(window, "wm_geometry"):  # Tkinter
        window.wm_geometry("+1200+0")
    elif hasattr(window, "setGeometry"):  # Qt
        window.setGeometry(1200, 0, 600, 800)

# Remove axes margins and display the SLM
ax = fig.add_axes([0, 0, 1, 1])
ax.imshow(SLM_vortex, cmap="gray", interpolation="nearest", aspect="auto")
ax.axis("off")

plt.show()
