import numpy as np
import csv
from pydmd import DMD

tf = 5000

snapshots = []

snapshots = [
    np.genfromtxt(f'Snapshots_pressure/Time_step{i}.csv', delimiter=',', skip_header=1)
    for i in range(10, tf)
]

pts = np.genfromtxt('Snapshots_full_data/Time_step10.csv', delimiter=',', skip_header=1)[:, -5:-3]

dmd = DMD(svd_rank=0, tlsq_rank=2, exact=True, opt=True)
dmd.fit(snapshots)

print(dmd.modes.shape)
print(dmd.reconstructed_data.real.T.shape)

for c in range(10, tf):
    print(f'Writing time step {c}...')
    with open(f'Snapshots_full_data/Time_step10.csv', 'r') as read_snaps:
        csv_reader = csv.reader(read_snaps)

        with open(f'DMD_snapshots/Time_step{c}.csv', 'w') as dmd_snaps:
            csv_writer = csv.writer(dmd_snaps, delimiter=',')

            i = 0
            for line in csv_reader:
                if line[5] != 'f_26':
                    line[5] = dmd.reconstructed_data.real.T[c][i]
                    csv_writer.writerow(line)
                    i += 1
                else:
                    csv_writer.writerow(line)

for c in range(0, num_modes):
    print(f'Writing dmd mode number {c}...')
    with open(f'Snapshots_full_data/Time_step10.csv', 'r') as read_snaps:
        csv_reader = csv.reader(read_snaps)

        with open(f'DMD_modes/Dmd_mode_{c}.csv', 'w') as dmd_modes:
            csv_writer = csv.writer(dmd_modes, delimiter=',')

            i = 0
            for line in csv_reader:
                if line[5] != 'f_26':
                    line[5] = dmd.modes.real[i][c]
                    csv_writer.writerow(line)
                    i += 1
                else:
                    csv_writer.writerow(line)
