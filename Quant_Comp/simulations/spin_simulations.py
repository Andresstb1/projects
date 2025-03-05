# -*- coding: utf-8 -*-
"""
"""

import numpy as np
import matplotlib.pyplot as plt
from qutip import *

# Simulation parameters (in arbitrary units)
D = 2.87        # Zero-field splitting (GHz) for NV centers (approximate)
A = 0.1         # Driving amplitude (arbitrary units)
omega = 2.87    # Driving frequency (resonant with D)

# Define spin-1 operators (the NV center ground state triplet)
Jx = jmat(1, 'x')
Jz = jmat(1, 'z')

# Initial state: assume the NV center is initially in the m=0 state.
# Note: In the qutip convention for a spin-1 system, basis(3, 1) often corresponds to m=0.
psi0 = basis(3, 1)

# Define the static part of the Hamiltonian:
# H0 = D * (Jz)^2. This represents the zero-field splitting.
H0 = D * (Jz**2)

# Define the time-dependent driving term:
# H1 = A * cos(omega*t) * Jx, which might represent a microwave control field.
def H1_coeff(t, args):
    return A * np.cos(omega * t)

H1 = [Jx, H1_coeff]

# Total Hamiltonian (using a list for time-dependent evolution)
H = [H0, H1]

# Time span for the simulation
tlist = np.linspace(0, 10, 200)

# Define projection operators for measuring populations in the three levels.
# (Depending on qutip's basis ordering, adjust indices if needed.)
P_m_plus  = basis(3, 0) * basis(3, 0).dag()  # Tentatively m = +1
P_m_zero  = basis(3, 1) * basis(3, 1).dag()   # m = 0
P_m_minus = basis(3, 2) * basis(3, 2).dag()   # m = -1

# Solve the dynamics (unitary evolution; no decoherence is included here)
result = mesolve(H, psi0, tlist, [], [P_m_plus, P_m_zero, P_m_minus])

# Extract the population expectation values for each state
pop_m_plus  = result.expect[0]
pop_m_zero  = result.expect[1]
pop_m_minus = result.expect[2]

# Plot the populations over time
plt.figure(figsize=(8, 5))
plt.plot(tlist, pop_m_plus,  label='Population m = +1')
plt.plot(tlist, pop_m_zero,  label='Population m = 0')
plt.plot(tlist, pop_m_minus, label='Population m = -1')
plt.xlabel('Time (arb. units)')
plt.ylabel('Population')
plt.title('Dynamics of NV Center Spin Under a Resonant Driving Field')
plt.legend()
plt.show()
