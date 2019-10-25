# rrps.dt.integrator

## Development / testing
```shell
# Assuming rrps/python/build_deps.sh has been run
pip install -f ../../../deps -f ../dist -e .
```
The above step is not required if the requirement packages are installed in development mode already. In this case the following is enough:
```shell
pip install -e .
```

## Environment setup

### Python

Download and install Python 3.6.7 for Windows.

### Visual Studio compilers

Download and install the Microsoft Visual Studio build tools from https://visualstudio.microsoft.com/downloads/#build-tools-for-visual-studio-2017 .

Execute the following from the folder where you downloaded the build tools to install them in `C:\Buildtools`:

```
vs_buildtools.exe --norestart --nocache --installPath C:\BuildTools --add Microsoft.VisualStudio.Workload.VCTools;includeRecommended --add Microsoft.VisualStudio.Component.Windows81SDK --add Microsoft.VisualStudio.ComponentGroup.NativeDesktop.Win81
```

The Visual Studio tools are required to build C extensions; if a `pip` execution fails to compile something, execute the following to ensure that the compilers are in the user path:

```
C:\BuildTools\VC\Auxiliary\Build\vcvarsall.bat x64 8.1
```

### Virtual environment

In order to avoid polluting the system python interpreter, it is necessary to create a virtual environment for development.

Such environment can be created by running the following:

```
mkdir %HOME%\envs
C:\Python36\python -mvenv %HOME%\envs\rrpsdev
```

The environment can be activated in the current command prompt by running:

```
%HOME%\envs\rrpsdev\Scripts\activate
```

When the environment is active, you'll see its name in the command prompt, e.g.:

```
(rrpsdev) C:\Users\foo\>
```

To link common dependencies and integrator packages to the virtual environment, activate the virtual environment, then go to the `rrps\python` directory and execute:

```
setup_venv.cmd
```

### Editing

To edit the sources in Pycharm, create a new project pointing to the GIT clone.

Click on `File` > `Settings...` and then click on `Project: <project name>`.

Click on `Python interpreter`.

Click on the cog next to the interpreter dropdown and then on `Add...`

Select "Existing environment".

Click on `...` next to `Interpreter` and put `~\envs\rrpsdev\Scripts\python.exe` as the interpreter (adjust if your virtual environment is in a different location).

Click OK and make sure that the selected interpreter is the one you just created.

Click OK and wait for indexing to complete (see bottom of the editor for progress).

To verify that Pycharm is working properly, open `rrps\python\rrps.dt.integrator.sapequipmenthistory\rrps\dt\integrator\sapequipmenthistory\impl.py` and expand the imports.

Go over the NestedConfig symbol in the imports and press `CTRL+Q`; you should see the docstring for the module.

Ctrl + Click on the symbol and you should jump to its source code.