# LatticeQuery - An F-rep tool for geometric modeling of lattice structures

The tool allows modeling of heterogeneous lattice structures, both beam-based and surface-based. The tool is based on the [CadQuery GUI](https://github.com/CadQuery/CQ-editor.git) editor which allows parametric modeling with [OpenCASCADE](https://www.opencascade.com/) and PyQT and supports Linux, Windows and MacOS.

For the CadQuery documentation, please address [its repository](https://github.com/CadQuery/cadquery) and [official documentation](https://cadquery.readthedocs.io/en/latest/).

## Usage
Most of the functionality is located in the `parfunlib` folder (stands for 'parametric function library').

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
This and many more examples of the implementation are located in the `lattce_scripts` directory.

## Known issues
Sometimes the modeling would fail with an error like `Brep: command not done`. This is often solved by passing a float argument to the function rather than an integer one. You can also try to increase the unit cell size, let's say, 10 times, and then scale it down 10 times.

The connection between some of the TPMS based topologies seems abrupt and has gaps in some cases. This effect should be investigated further.
