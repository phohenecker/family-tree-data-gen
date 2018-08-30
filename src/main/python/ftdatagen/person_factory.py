# -*- coding: utf-8 -*-


import random
import re
import typing

import insanity

from reldata.data import base_individual
from reldata.data import data_context as dc
from reldata.data import individual_factory

from ftdatagen import person


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


# ==================================================================================================================== #
#  CLASS  P E R S O N  F A C T O R Y                                                                                   #
# ==================================================================================================================== #


class PersonFactory(object):
    """A factory class for creating instances of an implementation of :class:`person.Person`."""

    _REMAINING_FEMALE_NAMES = "PersonFactory.remaining_female_names"
    """str: The key that is used for storing the remaining female names in the context."""

    _REMAINING_MALE_NAMES = "PersonFactory.remaining_male_names"
    """str: The key that is used for storing the remaining male names in the context."""
    
    FEMALE_NAMES = [
            "alina",
            "amelie",
            "anastasia",
            "angelina",
            "anna",
            "beate",
            "charlotte",
            "clara",
            "claudia",
            "elena",
            "ella",
            "emilia",
            "emily",
            "emma",
            "gertrude",
            "hannah",
            "helena",
            "helga",
            "isabella",
            "johanna",
            "julia",
            "karin",
            "katharina",
            "lara",
            "larissa",
            "laura",
            "lea",
            "lena",
            "leonie",
            "lina",
            "lisa",
            "luisa",
            "magdalena",
            "maria",
            "marie",
            "marlene",
            "mia",
            "natalie",
            "nina",
            "nora",
            "olivia",
            "paula",
            "sarah",
            "selina",
            "sofia",
            "sophie",
            "valentina",
            "valerie",
            "vanessa",
            "victoria"
    ]
    """list[str]: A list of all known female names."""
    
    MALE_NAMES = [
            "adam",
            "adrian",
            "alexander",
            "benjamin",
            "christian",
            "daniel",
            "david",
            "dominik",
            "elias",
            "emil",
            "fabian",
            "felix",
            "florian",
            "gabriel",
            "jakob",
            "jan",
            "jonas",
            "jonathan",
            "julian",
            "konstantin",
            "leo",
            "leon",
            "lorenz",
            "luca",
            "luis",
            "lukas",
            "marcel",
            "marko",
            "matthias",
            "maximilian",
            "michael",
            "moritz",
            "nico",
            "noah",
            "oliver",
            "oskar",
            "patrick",
            "paul",
            "philipp",
            "raphael",
            "rene",
            "samuel",
            "sebastian",
            "simon",
            "stefan",
            "theodor",
            "thomas",
            "tobias",
            "valentin",
            "vincent"
    ]
    """list[str]: A list of all known male names."""
    
    #  METHODS  ########################################################################################################
    
    @classmethod
    def _prepare_context(cls):
        """Prepares the current context for the ``PersonFactory`` if it is not prepared yet."""
        if dc.DataContext.get_context()[cls._REMAINING_FEMALE_NAMES] is None:
            cls.reset()
    
    @classmethod
    def create_person(cls, tree_level: int, female: bool=None) -> person.Person:
        """Constructs a new instance of :class:`person.Person`.

        Args:
            tree_level (int): The level in the family tree on which the created person is located.
            female (bool, optional): Indicates whether the created person is female. If not provided, then the gender
                is sampled randomly.
        """
        # sanitize args
        insanity.sanitize_type("tree_level", tree_level, int)
        
        # prepare context if necessary
        cls._prepare_context()
        
        # fetch current context
        ctx = dc.DataContext.get_context()
        
        # determine gender
        if female is None:
            female = random.random() > 0.5
        else:
            female = bool(female)
        
        # fetching names that may be used
        if female:
            remaining_names = ctx[cls._REMAINING_FEMALE_NAMES]
        else:
            remaining_names = ctx[cls._REMAINING_MALE_NAMES]
        
        # determine name
        name_index = random.randrange(len(remaining_names))
        name = remaining_names[name_index]
        del remaining_names[name_index]
        
        # check whether the just used list of names has to be reset (i.e., is empty now)
        # -> we just reuse known names and append a postfix to ensure uniqueness
        if not remaining_names:
            
            # determine the postfix to append to the new names
            postfix = re.search("([0-9]+)$", name)  # -> the previously used postfix
            if postfix:
                postfix = str(int(postfix.group(0)) + 1)  # increment existing postfix
            else:
                postfix = "2"  # start with postfix 2
            
            # create new names to use
            if female:
                ctx[cls._REMAINING_FEMALE_NAMES] = [n + postfix for n in cls.FEMALE_NAMES]
            else:
                ctx[cls._REMAINING_MALE_NAMES] = [n + postfix for n in cls.MALE_NAMES]
        
        # return new person
        return individual_factory.IndividualFactory.create_individual(
                name,
                target_type=_Person,
                args=[female, tree_level]
        )
    
    @classmethod
    def reset(cls) -> None:
        """Resets the ``PersonFactory`` to its initial state."""
        ctx = dc.DataContext.get_context()
        ctx[cls._REMAINING_FEMALE_NAMES] = cls.FEMALE_NAMES[:]
        ctx[cls._REMAINING_MALE_NAMES] = cls.MALE_NAMES[:]


# ==================================================================================================================== #
#  CLASS  _ P E R S O N                                                                                                #
# ==================================================================================================================== #


class _Person(person.Person):
    """A private implementation of :class:`person.Person`."""
    
    def __init__(self, index: int, name: str, female: bool, tree_level: int):
        base_individual.BaseIndividual.__init__(self)
        
        self._children = []
        self._female = female
        self._index = index
        self._married_to = None
        self._name = name
        self._parents = []
        self._tree_level = tree_level
    
    #  MAGIC FUNCTIONS  ################################################################################################
    
    def __str__(self):
        return "Person(index = {:d}, name = '{}', female = {}, married_to = {}, parents = {}, children = [{}])".format(
                self.index,
                self.name,
                str(self.female),
                str(self.married_to.index) if self.married_to else "None",
                "({})".format(", ".join([str(p.index) for p in self.parents])) if self.parents else "None",
                ", ".join([str(c.index) for c in self.children])
        )
    
    #  PROPERTIES  #####################################################################################################
    
    @property
    def children(self) -> typing.List[person.Person]:
        return self._children
    
    @property
    def female(self) -> bool:
        return self._female
    
    @property
    def married_to(self) -> typing.Union[typing.Any, None]:
        return self._married_to
    
    @married_to.setter
    def married_to(self, spouse: person.Person) -> None:
        insanity.sanitize_type("spouse", spouse, person.Person)
        self._married_to = spouse
    
    @property
    def parents(self) -> typing.List[person.Person]:
        return self._parents
    
    @property
    def tree_level(self) -> int:
        return self._tree_level
