Family Tree Data Generator
==========================


This repository contains the implementation of a tool for generating toy datasets that pose reasoning tasks about
family trees.
It has been created as part of the work for the following paper, and was used to generate a dataset for one of the
experiments reported in the same:

> Patrick Hohenecker and Thomas Lukasiewicz.  
> Deep Learning for Ontology Reasoning.  
> Preprint at [https://arxiv.org/abs/1705.10342](https://arxiv.org/abs/1705.10342), 2018.

You are very welcome to use the generator for creating data for your own research.
However, in this case, please make sure to cite the paper above.
For any questions about the paper or the code provided here, feel free to contact us via e-mail:
[patrick.hohenecker@cs.ox.ac.uk](mailto:patrick.hohenecker@cs.ox.ac.uk).

**Notice:**
Any data created by the family tree data generator are written to the disk in the *rel-data* format, which is specified
in detail [here](https://github.com/phohenecker/rel-data).


Inference Task
--------------

Every sample created by the data generator describes a knowledge graph that specifies a single family tree.
To that end, all individuals in a sample represent persons, and the only facts contained are the genders of the people
involved (specified by means of the unary predicates `male` and `female`) as well as the immediate ancestor relations
among them (identified by the binary predicate `parentOf`).
Besides this, every sample contains a multitude of inferable details, which are supposed to be derived from the facts
mentioned above.
For additional details about the inferences considered, have a look at the [ontology](/src/main/asp/ontology.asp) that
is used by the data generator, which is specified as an answer set program.
All predicates that appear in the same should be self-explanatory.


Usage
-----

Running the data generator is as easy as cloning this repository and launching the shell script
[run-data-gen.sh](/run-data-gen.sh).
Notice, however, that the application depends on numerous Python packages that need to be installed in order to run the
same.
For a complete list of dependencies, confer [setup.py](/setup.py).
While you could just install all of the required packages on your machine, a better solution is to create a virtual
[Conda](https://conda.io/docs/) environment.
To that end, the file [environment.yaml](/environment.yaml) provides a specification of such an environment that is
appropriate for running the data generator.

The following enumeration provides a step-by-step guide for running the family tree data generator in a Conda
environment:

1. Download this repository:

   ```
   $ git clone https://github.com/phohenecker/family-tree-data-gen.git
   $ cd family-tree-data-gen
   ```

2. Create and activate an appropriate Conda environment:

   ```
   $ conda env create -f environment.yaml  # create the environment
   $ source activate family-tree-data-gen  # activate it
   ```
   
   Notice that Conda environments can be reused, i.e., the one for the data generator has to be created only once.
   
3. Run the Python application:

   ```
   (family-tree-data-gen)$ ./run-data-gen.sh [ARGS]
   ```

For a detailed description of how to invoke the data generator and all options that may be provided to the same, refer
to the application's help text.
This is printed, if the application is launched with flag `--help` and `-h`, respectively:

```
(family-tree-data-gen)$ ./run-data-gen.sh --help
```

**Important:**
There are numerous options available, which allow for adjusting the generation process.
However, while all of these have default values, there is one positional arg that needs to be provided.
This is described in the next section.


The DLV System
--------------

The family tree data generator makes use of the DLV system in order to perform symbolic reasoning over family trees by
means of the ontology mentioned above.
Therefore, you have to download the DLV executable for your platform from the
[official website](http://www.dlvsystem.com/dlv/#1),
and provide the path to the same as (the only) positional arg:

```
(family-tree-data-gen)$ ./run-data-gen.sh [OPTIONS] /path/to/dlv
```

Notice that DLV is free for academic and non-commercial educational use.
However, details can be found [here](http://www.dlvsystem.com/dlv/#0).
