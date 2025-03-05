import numpy as np
from qiskit import QuantumCircuit, Aer, execute
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt

def shor_encode(qc, qubits):
    """
    Función para codificar un qubit lógico en 9 qubits usando el código de Shor.
    Se utiliza primero una codificación de 3-qubits (repetición) para corregir
    errores de bit-flip, y luego para cada uno se implementa una codificación en
    la base Hadamard para proteger contra errores de fase.
    
    Se asume que:
      - Los qubits [0,1,2] contienen inicialmente la codificación bit-flip:
            α|000> + β|111>
      - Cada uno se codificará en un bloque de 3 qubits:
            Bloque 1: qubits[0], qubits[3], qubits[6]
            Bloque 2: qubits[1], qubits[4], qubits[7]
            Bloque 3: qubits[2], qubits[5], qubits[8]
    """
    # Paso 1: Codificación de 3-qubits (bit-flip code)
    qc.cx(qubits[0], qubits[1])
    qc.cx(qubits[0], qubits[2])
    qc.barrier()
    
    # Paso 2: Codificación para cada bloque (protección contra errores de fase)
    # La idea es realizar una repetición en la base Hadamard:
    # se aplican H en los 3 qubits del bloque, se "copian" mediante CNOTs y luego se vuelve a aplicar H.
    
    # Bloque 1: qubits 0, 3, 6
    qc.h(qubits[0])
    qc.h(qubits[3])
    qc.h(qubits[6])
    qc.cx(qubits[0], qubits[3])
    qc.cx(qubits[0], qubits[6])
    qc.h(qubits[0])
    qc.h(qubits[3])
    qc.h(qubits[6])
    qc.barrier()
    
    # Bloque 2: qubits 1, 4, 7
    qc.h(qubits[1])
    qc.h(qubits[4])
    qc.h(qubits[7])
    qc.cx(qubits[1], qubits[4])
    qc.cx(qubits[1], qubits[7])
    qc.h(qubits[1])
    qc.h(qubits[4])
    qc.h(qubits[7])
    qc.barrier()
    
    # Bloque 3: qubits 2, 5, 8
    qc.h(qubits[2])
    qc.h(qubits[5])
    qc.h(qubits[8])
    qc.cx(qubits[2], qubits[5])
    qc.cx(qubits[2], qubits[8])
    qc.h(qubits[2])
    qc.h(qubits[5])
    qc.h(qubits[8])
    qc.barrier()

def shor_decode(qc, qubits):
    """
    Función de decodificación (inversa de la codificación).
    Se invierte el proceso aplicado en shor_encode.
    """
    # Inverso de la codificación en cada bloque.
    # Bloque 3: qubits 2, 5, 8
    qc.h(qubits[2])
    qc.h(qubits[5])
    qc.h(qubits[8])
    qc.cx(qubits[2], qubits[5])
    qc.cx(qubits[2], qubits[8])
    qc.h(qubits[2])
    qc.h(qubits[5])
    qc.h(qubits[8])
    qc.barrier()
    
    # Bloque 2: qubits 1, 4, 7
    qc.h(qubits[1])
    qc.h(qubits[4])
    qc.h(qubits[7])
    qc.cx(qubits[1], qubits[4])
    qc.cx(qubits[1], qubits[7])
    qc.h(qubits[1])
    qc.h(qubits[4])
    qc.h(qubits[7])
    qc.barrier()
    
    # Bloque 1: qubits 0, 3, 6
    qc.h(qubits[0])
    qc.h(qubits[3])
    qc.h(qubits[6])
    qc.cx(qubits[0], qubits[3])
    qc.cx(qubits[0], qubits[6])
    qc.h(qubits[0])
    qc.h(qubits[3])
    qc.h(qubits[6])
    qc.barrier()
    
    # Inverso de la codificación bit-flip (mayoría simple)
    qc.cx(qubits[0], qubits[1])
    qc.cx(qubits[0], qubits[2])
    qc.barrier()

# Crear un circuito cuántico con 9 qubits y 1 bit clásico para la medición final
qc = QuantumCircuit(9, 1)

# Preparar el estado inicial en el qubit lógico (por ejemplo, el estado |+>)
qc.h(0)
qc.barrier()

# Codificar el qubit lógico en 9 qubits con el código de Shor
shor_encode(qc, list(range(9)))

# Se introduce un error: por ejemplo, un error de flip de bit en el qubit 4
qc.x(4)
qc.barrier()

# Se aplica la decodificación (inversa de la codificación)
shor_decode(qc, list(range(9)))

# Medición del qubit 0, que se espera recupere el estado original (en ausencia de otros errores)
qc.measure(0, 0)

# Ejecutar el circuito en el simulador QASM
backend = Aer.get_backend('qasm_simulator')
job = execute(qc, backend, shots=1024)
result = job.result()
counts = result.get_counts(qc)

print("Resultados de la medición:", counts)
plot_histogram(counts)
plt.show()
