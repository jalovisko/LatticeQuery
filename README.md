# LatticeQuery - An F-rep tool for geometric modeling of lattice structures

The tool allows modeling of heterogeneous lattice structures, both beam-based and surface-based. The tool is based on the [CadQuery GUI](https://github.com/CadQuery/CQ-editor.git) editor which allows parametric modeling with [OpenCASCADE](https://www.opencascade.com/) and PyQT and supports Linux, Windows and MacOS.

For the CadQuery documentation, please address [its repository](https://github.com/CadQuery/cadquery) and [official documentation](https://cadquery.readthedocs.io/en/latest/).

## Installation
The installation of this tool requires [Anaconda](https://www.anaconda.com/) installed. Once installed, you can create a virtual conda environment as follows:
```bash
conda env create -f lqgui_env.yml -n lq
conda activate lq
```

## Usage
Most of the functionality is located in the `parfunlib` folder (stands for 'parametric function library'). Within the installed virtual environment, run the main Python script as follows:
```bash
python run.py
```

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
from parfunlib.topologies.schwartz import schwartz_p_heterogeneous_lattice
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

## Other examples
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


## Known issues
Sometimes the modeling would fail with an error like `Brep: command not done`. This is often solved by passing a float argument to the function rather than an integer one. You can also try to increase the unit cell size, let's say, 10 times, and then scale it down 10 times.

The connection between some of the TPMS based topologies seems abrupt and has gaps in some cases. This effect should be investigated further.
