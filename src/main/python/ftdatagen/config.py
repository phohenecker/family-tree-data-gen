# -*- coding: utf-8 -*-


import numbers
import os
import random
import typing

import insanity

from argmagic import decorators


__author__ = "Patrick Hohenecker"
__copyright__ = (
        "Copyright (c) 2018, Patrick Hohenecker\n"
        "All rights reserved.\n"
        "\n"
        "Redistribution and use in source and binary forms, with or without\n"
        "modification, are permitted provided that the following conditions are met:\n"
        "\n"
        "1. Redistributions of source code must retain the above copyright notice, this\n"
        "   list of conditions and the following disclaimer.\n"
        "2. Redistributions in binary form must reproduce the above copyright notice,\n"
        "   this list of conditions and the following disclaimer in the documentation\n"
        "   and/or other materials provided with the distribution.\n"
        "\n"
        "THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS \"AS IS\" AND\n"
        "ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED\n"
        "WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE\n"
        "DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR\n"
        "ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES\n"
        "(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;\n"
        "LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND\n"
        "ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT\n"
        "(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS\n"
        "SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE."
)
__license__ = "BSD-2-Clause"
__version__ = "2018.1"
__date__ = "May 30, 2018"
__maintainer__ = "Patrick Hohenecker"
__email__ = "mail@paho.at"
__status__ = "Development"


class Config(object):
    """Encapsulates the user-defined configuration."""
    
    DEFAULT_MAX_BRANCHING_FACTOR = 5
    """int: Default value of :attr:`max_branching_factor`."""
    
    DEFAULT_MAX_TREE_DEPTH = 5
    """int: Default value of :attr:`max_tree_depth`."""
    
    DEFAULT_MAX_TREE_SIZE = 26
    """int: Default value of :attr:`max_tree_size`."""
    
    DEFAULT_NEGATIVE_FACTS = False
    """bool: Default value of :attr:`negative_facts`."""
    
    DEFAULT_NUM_SAMPLES = 5000
    """int: Default value of :attr:`num_samples`."""

    DEFAULT_OUTPUT_DIR = "./out"
    """str: Default value for :attr:`output_dir`."""

    DEFAULT_QUIET = False
    """bool: Default value for :attr:`quiet`."""
    
    DEFAULT_STOP_PROB = 0.0
    """float: Default value of :attr:`stop_prob`."""

    #  CONSTRUCTOR  ####################################################################################################

    def __init__(self):
        """Creates a new instance of ``Config``."""
        self._dlv = None
        self._max_branching_factor = self.DEFAULT_MAX_BRANCHING_FACTOR
        self._max_tree_depth = self.DEFAULT_MAX_TREE_DEPTH
        self._max_tree_size = self.DEFAULT_MAX_TREE_SIZE
        self._negative_facts = self.DEFAULT_NEGATIVE_FACTS
        self._num_samples = self.DEFAULT_NUM_SAMPLES
        self._output_dir = self.DEFAULT_OUTPUT_DIR
        self._quiet = self.DEFAULT_QUIET
        self._seed = random.randrange(100000)  # -> we randomly generate a default seed to ensure reproducibility
        self._stop_prob = self.DEFAULT_STOP_PROB

    #  PROPERTIES  #####################################################################################################
    
    @property
    def dlv(self) -> str:
        """str: The path to the DLV executable.

        DLV is an answer-set reasoner that is used for generating some of the datasets
        (`http://www.dlvsystem.com/dlv/`_).
        """
        return self._dlv

    @dlv.setter
    def dlv(self, dlv: str) -> None:
        dlv = str(dlv)
        if not os.path.isfile(dlv):
            raise ValueError("The provided path <dlv> does not exist: '{}'!".format(dlv))
        self._dlv = dlv

    @property
    def max_branching_factor(self) -> int:
        """int: The maximum number of children that any person in a family tree may have."""
        return self._max_branching_factor

    @max_branching_factor.setter
    def max_branching_factor(self, max_branching_factor: int) -> None:
        insanity.sanitize_type("max_branching_factor", max_branching_factor, int)
        insanity.sanitize_range("max_branching_factor", max_branching_factor, minimum=1)
        self._max_branching_factor = max_branching_factor
    
    @property
    def max_tree_depth(self) -> int:
        """int: The maximum depth that a family tree may have."""
        return self._max_tree_depth
    
    @max_tree_depth.setter
    def max_tree_depth(self, max_tree_depth: int) -> None:
        insanity.sanitize_type("max_tree_depth", max_tree_depth, int)
        insanity.sanitize_range("max_tree_depth", max_tree_depth, minimum=1)
        self._max_tree_depth = max_tree_depth
    
    @property
    def max_tree_size(self) -> int:
        """int: The maximum number of people that may appear in a family tree."""
        return self._max_tree_size
    
    @max_tree_size.setter
    def max_tree_size(self, max_tree_size: int) -> None:
        insanity.sanitize_type("max_tree_size", max_tree_size, int)
        insanity.sanitize_range("max_tree_size", max_tree_size, minimum=1)
        self._max_tree_size = max_tree_size
    
    @property
    def negative_facts(self) -> bool:
        """bool: Specifies whether to include negative parentOf relations as facts."""
        return self._negative_facts
    
    @negative_facts.setter
    def negative_facts(self, negative_facts: bool) -> None:
        self._negative_facts = bool(negative_facts)

    @property
    def num_samples(self) -> typing.Union[int, None]:
        """int: The size of the dataset to generate."""
        return self._num_samples

    @num_samples.setter
    def num_samples(self, num_samples: int) -> None:
        insanity.sanitize_type("num_samples", num_samples, int)
        insanity.sanitize_range("num_samples", num_samples, minimum=1)
        self._num_samples = num_samples

    @property
    def output_dir(self) -> str:
        """str: The directory that generated data should be written to."""
        return self._output_dir

    @output_dir.setter
    def output_dir(self, output_dir: str) -> None:
        self._output_dir = str(output_dir)

    @property
    def quiet(self) -> bool:
        """bool: Tells the application to be 'quiet'."""
        return self._quiet

    @quiet.setter
    def quiet(self, quiet: bool) -> None:
        self._quiet = bool(quiet)

    @decorators.optional
    @property
    def seed(self) -> int:
        """int: The seed that is used to initialize the used RNG."""
        return self._seed

    @seed.setter
    def seed(self, seed: int) -> None:
        insanity.sanitize_type("seed", seed, int)
        self._seed = seed
    
    @property
    def stop_prob(self) -> float:
        """float: The probability of stopping to further extend a family tree after a person has been added."""
        return self._stop_prob
    
    @stop_prob.setter
    def stop_prob(self, stop_prob: numbers.Real) -> None:
        insanity.sanitize_type("stop_prob", stop_prob, numbers.Real)
        insanity.sanitize_range("stop_prob", stop_prob, minimum=0, maximum=1, max_inclusive=False)
        self._stop_prob = float(stop_prob)
