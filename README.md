# An F-rep tool for geometric modeling of lattice structures

The tool is based on the [CadQuery GUI](https://github.com/CadQuery/CQ-editor.git) editor which in turn is based on PyQT and OpenCASCADE and supports Linux, Windows and Mac.

<img src="https://github.com/CadQuery/CQ-editor/raw/master/screenshots/screenshot2.png" alt="Screenshot" width="70%" >
<img src="https://github.com/CadQuery/CQ-editor/raw/master/screenshots/screenshot3.png" alt="Screenshot" width="70%" >
<img src="https://github.com/CadQuery/CQ-editor/raw/master/screenshots/screenshot4.png" alt="Screenshot" width="70%" >

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

The `lattce_scripts` directory includes a few more examples.

## Known issues
Sometimes the modeling would fail with an error like `Brep: command not done`. This is often solved by passing a float argument to the function rather than an integer one. You can also try to increase the unit cell size, let's say, 10 times, and then scale it down 10 times.

# CadQuery

This section is an intoduction to CadQuery - the library we used to implement our tool. This is relevant only if you intend to contribute to this repository.

## Notable features

* OCCT based
* Graphical debugger for CadQuery scripts
  * Step through script and watch how your model changes
* CadQuery object stack inspector
  * Visual inspection of current workplane and selected items
  * Insight into evolution of the model
* Export to various formats
  * STL
  * STEP

## Installation (Anaconda)

Use conda to install:
```
conda install -c cadquery -c conda-forge cq-editor=master
```
and then simply type `cq-editor` to run it. This installs the latest version built directly from the HEAD of this repository.

Alternatively clone this git repository and set up the following conda environment:
```
conda env create -f cqgui_env.yml -n cqgui
conda activate cqgui
python run.py
```

On some linux distributions (e.g. `Ubuntu 18.04`) it might be necessary to install additonal packages:
```
sudo apt install libglu1-mesa libgl1-mesa-dri mesa-common-dev libglu1-mesa-dev
```
On Fedora 29 the packages can be installed as follows:
```
dnf install -y mesa-libGLU mesa-libGL mesa-libGLU-devel
```

## Installation (Binary Builds)

Development builds are now available that should work stand-alone without Anaconda. Click on the newest build with a green checkmark [here](https://github.com/jmwright/CQ-editor/actions?query=workflow%3Abuild), wait for the _Artifacts_ section at the bottom of the page to load, and then click on the appropriate download for your operating system. Extract the archive file and run the shell (*nix) or batch (Windows) script in the root CQ-editor directory. The CQ-editor window should launch.

A stable version of these builds will be provided in the future, but are not available currently.

## Usage

### Showing Objects

By default, CQ-editor will display a 3D representation of all `Workplane` objects in a script with a default color and alpha (transparency). To have more control over what is shown, and what the color and alpha settings are, the `show_object` method can be used. `show_object` tells CQ-editor to explicity display an object, and accepts the `options` parameter. The `options` parameter is a dictionary of rendering options named `alpha` and `color`. `alpha` is scaled between 0.0 and 1.0, with 0.0 being completely opaque and 1.0 being completely transparent. The color is set using R (red), G (green) and B (blue) values, and each one is scaled from 0 to 255. Either option or both can be omitted.

```python
show_object(result, options={"alpha":0.5, "color": (64, 164, 223)})
```

Note that `show_object` works for `Shape` and `TopoDS_Shape` objects too. In order to display objects from the embedded Python console use `show`.
