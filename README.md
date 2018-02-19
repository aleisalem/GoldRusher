# GoldRusher: A Miner for Rapid Identification of Hidden Code

GoldRusher is a dynamic analysis tool primarily meant to aid reverse engineers with analyzing (malicious) binaries. Based on the fact that hidden code segments rarely execute, the tool is able to rapidly highlight functions and basic blocks that are potentially hidden, and identify the trigger conditions that control their executions.

## Overview
The miner is implemented as a set of modules organized into separate directories:
* ``bin``: Contains the codeCoverage binaries, which can also be downloaded [here](http://www.paradyn.org/html/tools/codecoverage.html).
* ``conf``: Contains a configuration file that primarily specifies paths to different directories used during the execution of GoldRusher.
* ``db``: A directory in which the ``goldrusher.db`` database is stored.
* ``demo``: A video demonstration of how the initial version of the tool works. More videos/tutorials about the tool will be uploaded to this directory.
* ``docs``: Documents related to the tool's operation. Currently contains a SQL script used to generate the ``goldrusher.db``, if it doesn't exist under ``db``.
* ``out``: The default output directory of GoldRusher.
* ``samples``: Contains sample C/C++ programs that can be used to get acquainted to GoldRusher and its operation.
* ``tools``: Contains tools that utilize the GoldRusher modules to extract hidden code segments from binaries.
* ``utils``: Different utilities used by the tool.
  * ``db``: Handles all CRUD operations between the tools and the ``goldrusher.db`` database.
  * ``graphics``: Used for colored display of output, warning, error, and debug messages.
  * ``misc``: Miscellaneous tools e.g. generate timestamps and random values.
  * ``parser``: Parses the output from ``codeCoverage`` and ``ltrace`` to retrieve number of executions and function names.


## Dependencies
The tool depends on the existence of the following tools:
* ``codeCoverage``: Used to instrument target binaries to keep track of functions and blocks covered during run time.
* ``ltrace``: A *-nix tool that keeps track of library calls made during runtime.
* ``Tigress``: Used by the tool ``generatePrograms.py`` to generate random/obfuscated programs.

## Tools
Currently, there are two tools that utilize the GoldRusher modules viz., ``generatePrograms.py`` and ``goldRusher.py``.

### generatePrograms.py
Uses [Tigress](tigress.cs.arizona.edu) to generate random programs used to evaluate/test GoldRusher's approach.

```
usage: generatePrograms.py [-h] -n NUM [-o OUTDIR] [-f {yes,no}]

Generates obfuscated and hidden code versions of programs.

optional arguments:
  -h, --help            show this help message and exit
  -n NUM, --num NUM     The number of random programs to generate.
  -o OUTDIR, --outdir OUTDIR
                        The directory to write generated programs to
  -f {yes,no}, --obfuscate {yes,no}
                        Whether to obfuscate generated programs
```

###
Depicts the main operation of GoldRusher i.e. 

```
usage: goldRusher.py [-h] -t TARGET [-c CODECOVERAGE] [-x HIDDENTHRESHOLD]
                     [-p OPT] [-e CONNECTOR] [-a ARG] [-i STDINPUT]
                     [-n NUMRUNS] [-o OUTDIR]

Extracts hidden code segments from binaries and identifies their trigger
conditions.

optional arguments:
  -h, --help            show this help message and exit
  -t TARGET, --target TARGET
                        The binaries file to examine.
  -c CODECOVERAGE, --codecoverage CODECOVERAGE
                        The directory under which codeCoverage resides.
  -x HIDDENTHRESHOLD, --hiddenthreshold HIDDENTHRESHOLD
                        The percentage of coverage under which a method/line
                        is considered hidden
  -p OPT, --opt OPT     The options to invoke the binary with, if applicable
  -e CONNECTOR, --connector CONNECTOR
                        The operator that connects options and actions (e.g.,
                        '=')
  -a ARG, --arg ARG     The type/value of arguments to invoke the program
                        with. Supported types are "int", "float", "str",
                        "char", "hash", or "none"
  -i STDINPUT, --stdinput STDINPUT
                        Whether the program needs inputs via stdin
  -n NUMRUNS, --numruns NUMRUNS
                        The number of times random inputs is fed to the target
                        program.
  -o OUTDIR, --outdir OUTDIR
                        The path to the output directory. Defaults to entry in
                        config file. Files generated if logging is on


```
## Demonstration

A video demonstration of the ``goldrusher.py`` tool is available under [demo/goldrusher_demo.m4v](https://github.com/aleisalem/goldrusher/demo/goldrusher_demo.m4v).

## Citation and Contact

For more information about the design and implementation of the tool, please refer to the **To appear** paper. Kindly cite GoldRusher paper, if you mention the tool in your paper. :)

```
Citation coming soon.
```

Please contact me via [salem@in.tum.de](mailto:salem@in.tum.de) if you have any questions with regard to that tool and its operation.
