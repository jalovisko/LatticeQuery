# LatticeQuery - An open-source software for modeling of lattice structures

[![DOI](https://zenodo.org/badge/291864023.svg)](https://zenodo.org/badge/latestdoi/291864023)

The tool allows modeling of heterogeneous lattice structures, both beam-based and surface-based. The tool is based on the [CadQuery GUI](https://github.com/CadQuery/CQ-editor.git) editor which allows parametric modeling with [OpenCASCADE](https://www.opencascade.com/) and PyQT and supports Linux, Windows and MacOS.

For the CadQuery documentation, please address [its repository](https://github.com/CadQuery/cadquery) and [official documentation](https://cadquery.readthedocs.io/en/latest/).

For the description of the methodology, the [corresponding research paper](https://doi.org/10.1093/jcde/qwac076) is suggested.

## 1. Installation

### 1.1. Requirements

- Python 3.10–3.12 (Python 3.13+ is not yet supported by the `cadquery` dependency)
- pip

### 1.2. Linux (Debian / Ubuntu)

Install system libraries required by Qt and Python:

```bash
sudo apt update && sudo apt install -y \
  python3 python3-pip python3-venv \
  libgl1 libglu1-mesa \
  libx11-xcb1 libxcb-icccm4 libxcb-image0 libxcb-keysyms1 \
  libxcb-randr0 libxcb-render-util0 libxcb-xinerama0 \
  libxkbcommon-x11-0
```

Then install LatticeQuery:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -e .
python run.py
```

### 1.3. Linux (Arch Linux)

```bash
sudo pacman -S --needed python python-pip mesa glu libx11 libxcb \
  xcb-util-wm xcb-util-image xcb-util-keysyms xcb-util-renderutil libxkbcommon
```

```bash
python -m venv venv
source venv/bin/activate
pip install -e .
python run.py
```

### 1.4. macOS

```bash
python3 -m venv venv
source venv/bin/activate
pip install -e .
python run.py
```

### 1.5. Windows

```bat
python -m venv venv
venv\Scripts\activate
pip install -e .
python run.py
```

You can also use the binary versions in the [latest release](https://github.com/jalovisko/LatticeQuery/releases/latest).

## 2. Usage

Most of the functionality is located in the `lq` folder (stands for 'LatticeQuery'). Within the installed virtual environment, run the main Python script as follows:

```bash
python run.py
```

Linux (Wayland): if you are running a Wayland compositor, Qt may need to be forced to use the XCB (X11) backend:

```bash
QT_QPA_PLATFORM=xcb python run.py
```

This is set automatically when launching via `run.py`, so you only need the explicit override if you experience display issues.

The topologies that are implemented include:
* Beam-based
  * Simple cubic
  * BCC
  * FCC
  * S-FCC
  * BCCz
  * FCCz
  * S-FCCz
  * FBCC
  * S-FBCC
  * S-FBCCz
  * Diamond
  * Rhombicuboctahedron
  * Truncated cube
* TPMS
  * Gyroid
  * Schwarz 'Primitive' (P)
  * Schwarz 'Diamond' (D)

For example, modeling of a heterogeneous Schwarz P lattice with the thickness linearly changing from 0.1 to 7 is possible as follows
```python
# Python
import cadquery as cq
from lq.topologies.schwartz import schwartz_p_heterogeneous_lattice
cq.Workplane.schwartz_p_heterogeneous_lattice = schwartz_p_heterogeneous_lattice

# BEGIN USER INPUT
unit_cell_size = 4
Nx = 10
Ny = 10
Nz = 10
min_thickness = 0.1
max_thickness = 7
# END USER INPUT

schwartz = schwartz_p_heterogeneous_lattice(unit_cell_size, min_thickness, max_thickness,
                                      Nx, Ny, Nz
                                      )
```
As you can see, a single function handles requires geometric arguments and handles all the modeling. The result is the following:
![Heterogeneous Schwartz P lattice](/screenshots/hetero-schwartz.png)

## 3. Other examples
This and many more examples of the implementation are located in the `lattce_scripts` directory.
An example is a Python script that can be imported from within the editor (the window you see when running `run.py`).
These examples include the geometric modeling of:
* A homogeneous gyroid lattice (`gyroid.py`)
* A conformal heterogeneous lattice filling a cylindrical tube (`tire.py`)
* A heterogeneous FCC lattice with the linearly changing beam thickness (`FCC_heterogeneous_lattice.py`)
* A heterogeneous BCC lattice with the beam thickness changing according to the parabolic distribution (`BCC_heterogeneous_lattice.py`)
* A heterogeneous FCC lattice with the beam cross-section gradually changing from square to circle (`changing_cross_section.py`)
* A heterogeneous diamond lattice with the linearly changing beam thickness (`diamond.py`)
* A heterogeneous FBCC lattice with the linearly changing beam thickness (`FBCC_heterogeneous_lattice.py`)
* A heterogeneous gyroid lattice with the linearly changing thickness (`heterogeneous_gyroid.py`)
* A heterogeneous Schwarz D and P lattices with the linearly changing thickness (`heterogeneous_schwartz.py`)
* A heterogeneous Schwarz D lattice with the thickness changing according to the periodic sine distribution (`schwartz-d.py`)


## 4. Known issues
Sometimes the modeling would fail with an error like `Brep: command not done`. This is often solved by passing a float argument to the function rather than an integer one. You can also try to increase the unit cell size, let's say, 10 times, and then scale it down 10 times, or increasing the mesh density.

The connection between some of the TPMS based topologies seems abrupt and has gaps in some cases. This effect should be investigated further.
