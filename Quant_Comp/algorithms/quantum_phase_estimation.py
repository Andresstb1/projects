import numpy as np
from qiskit import QuantumCircuit, Aer, execute
from qiskit.extensions import UnitaryGate
from qiskit.circuit.library import QFT
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt

# Parameters for QPE
n_ancilla = 3           # Number of ancilla qubits (phase estimation precision)
theta = 0.625           # The phase we want to estimate: eigenvalue = exp(2*pi*i*theta)
n_qubits = n_ancilla + 1  # Total qubits: ancilla + 1 target

# Create a quantum circuit with n_qubits and n_ancilla classical bits (for ancilla measurements)
qc = QuantumCircuit(n_qubits, n_ancilla)

# Step 1: Prepare the ancilla register in superposition with Hadamard gates.
for q in range(n_ancilla):
    qc.h(q)

# Step 2: Prepare the target register in the eigenstate |1>
# (since our U operator acts as U|1> = exp(2pi i*theta)|1>)
qc.x(n_ancilla)

# Step 3: Apply the controlled-U operations.
# For each ancilla qubit j, we apply a controlled operation U^(2^(n_ancilla-1-j))
for j in range(n_ancilla):
    power = 2**(n_ancilla - 1 - j)
    # Compute U^power = diag(1, exp(2pi*i*theta*power))
    U_power = np.array([[1, 0], [0, np.exp(2*np.pi*1j*theta*power)]])
    U_gate = UnitaryGate(U_power, label=f"U^{power}")
    # Create the controlled version of U_gate.
    cU_gate = U_gate.control(1)
    # Append controlled-U: control is ancilla qubit j, target is the last qubit (n_ancilla)
    qc.append(cU_gate, [j, n_ancilla])

# Step 4: Apply the inverse Quantum Fourier Transform on the ancilla register.
qft_inv = QFT(num_qubits=n_ancilla, inverse=True, do_swaps=True).to_gate()
qft_inv.label = "QFT†"
qc.append(qft_inv, list(range(n_ancilla)))

# Step 5: Measure the ancilla qubits
qc.measure(range(n_ancilla), range(n_ancilla))

# Draw the circuit
print(qc.draw())

# Execute the circuit using a QASM simulator.
backend = Aer.get_backend('qasm_simulator')
job = execute(qc, backend, shots=1024)
result = job.result()
counts = result.get_counts(qc)

print("Measurement results:", counts)
plot_histogram(counts)
plt.show()
