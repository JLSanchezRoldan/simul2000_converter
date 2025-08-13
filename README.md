# Simul2000 Velocity Model Converter

A Python utility to convert multiple depth slices of **P-wave velocity** into a single **3D velocity model** in [Simul2000]([https://www.ita.uni-heidelberg.de/~simul2000](http://www.geology.wisc.edu/~thurber/simul2000/)) format.

## 📋 Features
- Reads multiple ASCII files containing P-wave velocity values at different depths.
- Supports **negative depths** (above the surface) and **positive depths** (below the surface).
- Automatically sorts slices in correct vertical order.
- Generates a `.mod` file ready for Simul2000.
- Configurable **Vp/Vs ratio**.

---

## 📂 Input File Naming

Depth slices must be placed inside the `mTAB3D` folder.  
The script recognizes two naming patterns:

| Example Filename | Depth Interpretation |
|------------------|----------------------|
| `z000.dat`       | 0 km (surface)        |
| `z001.dat`       | +1 km (below surface) |
| `z010.dat`       | +10 km (below surface)|
| `z0-1.dat`       | -1 km (above surface) |
| `z0-5.dat`       | -5 km (above surface) |

---

## 📑 Input File Format

Each `.dat` file must have **4 columns** (space-separated):

```
X_node   Y_node   Z_node   Vp_value
```

- **X_node**: X coordinate (km) of grid node
- **Y_node**: Y coordinate (km) of grid node
- **Z_node**: Depth coordinate (km) of grid node (can be negative)
- **Vp_value**: P-wave velocity (km/s)

The horizontal grid should be consistent across all depth files.

---

## 🖥 Output

The script writes a `.mod` file in **Simul2000** format:

```
BLD NX NY NZ
XN(1) XN(2) ... XN(NX)
YN(1) YN(2) ... YN(NY)
ZN(1) ZN(2) ... ZN(NZ)
0 0 0
0 0 0
VP(1,1,1) VP(2,1,1) ... VP(NX,1,1)
...
RAT(1,1,1) RAT(2,1,1) ... RAT(NX,1,1)
...
```

Where:
- **BLD** is always `1.0`
- **RAT** = Vp/Vs ratio (constant, configurable in the script)

---

## ⚙️ Configuration

Inside the script, you can set:

```python
RATIO_VP_VS = 1.73  # Default Vp/Vs ratio
input_folder = "mTAB3D"
output_file = "velocity_model.mod"
```

---

## 🚀 Usage

```bash
python convert_to_simul2000.py
```

The script will:
1. Read all `z*.dat` files from the `mTAB3D` folder.
2. Sort them in vertical order.
3. Generate a `.mod` file for Simul2000.

---

## 📌 Example

If `mTAB3D` contains:

```
z0-2.dat   → -2 km depth
z0-1.dat   → -1 km depth
z000.dat   →  0 km depth
z001.dat   → +1 km depth
```

The ZN coordinate list in the `.mod` file will be:

```
-2.0 -1.0 0.0 1.0
```

---

## 🛠 Requirements
- Python 3.7+
- NumPy

Install dependencies:
```bash
pip install numpy
```

---

## 📄 License
MIT License.  
You are free to use, modify, and distribute this script.
