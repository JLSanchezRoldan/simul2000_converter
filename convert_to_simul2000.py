import os
import numpy as np
from tqdm import tqdm

# Configuration
RATIO_VP_VS = 1.73
input_folder = "dat"
output_file = "velocity_model.mod"

def parse_depth_from_filename(fname):
    base = os.path.splitext(fname)[0]
    depth_str = base[1:]
    return float(depth_str.replace('-', '.').replace('0.', '-').replace('-', '')) if '0-' in base else float(depth_str)

def main():
    files = [f for f in os.listdir(input_folder) if f.startswith('z') and f.endswith('.dat')]
    if not files:
        raise FileNotFoundError(f"No depth slice files found in {input_folder} folder.")

    depths_files = []
    for f in files:
        if '0-' in f:
            depth = -float(f.split('0-')[1].split('.')[0])
        else:
            depth = float(f[1:4])
        depths_files.append((depth, os.path.join(input_folder, f)))

    depths_files.sort(key=lambda x: x[0])

    X_coords, Y_coords, Vp_data = None, None, []

    print("Reading input files...")
    for depth, filepath in tqdm(depths_files, desc="Depth layers"):
        data = np.loadtxt(filepath, delimiter=',')
        if X_coords is None:
            X_coords = np.unique(data[:,0])
            Y_coords = np.unique(data[:,1])
        Vp_data.append(data[:,3].reshape(len(Y_coords), len(X_coords)))

    Z_coords = [d for d, _ in depths_files]

    with open(output_file, 'w') as f:
        f.write(f"1.0 {len(X_coords)} {len(Y_coords)} {len(Z_coords)}\n")
        f.write(" ".join(map(str, X_coords)) + "\n")
        f.write(" ".join(map(str, Y_coords)) + "\n")
        f.write(" ".join(map(str, Z_coords)) + "\n")
        f.write(" 0 0 0\n 0 0 0\n")

        #for vp_slice in Vp_data:
        for vp_slice in tqdm(Vp_data, desc="Depth slices (Vp)"):
            for row in vp_slice:
                f.write(" ".join(map(str, row)) + "\n")

        #for _ in Vp_data:
        for vp_slice in tqdm(Vp_data, desc="Depth slices (Vp/Vs ratio)"):
            for _ in Y_coords:
                f.write(" ".join([str(RATIO_VP_VS)] * len(X_coords)) + "\n")

if __name__ == "__main__":
    main()
