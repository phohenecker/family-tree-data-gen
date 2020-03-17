# -*- coding: utf-8 -*-


import math
import random
import time
import typing

import aspwrapper
import networkx as nx

from reldata import data_context as dc
from reldata.data import class_membership
from reldata.data import knowledge_graph
from reldata.data import triple
from reldata.io import kg_writer
from reldata.vocab import class_type_factory as ctf
from reldata.vocab import relation_type_factory as rtf

from ftdatagen import config
from ftdatagen import person
from ftdatagen import person_factory as pf


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


class Generator(object):
    """A generator for creating family tree datasets."""
    
    BAR_CHART_STEPS = 40
    """int: The maximum width of any chart that is printed to the screen."""

    CLASSES = [
            "female",
            "male"
    ]
    """list: A list of all classes to include in a family tree dataset. List indices correspond to class indices."""

    RELATIONS = [
            "parentOf",
            "sisterOf",
            "brotherOf",
            "motherOf",
            "fatherOf",
            "grandmotherOf",
            "grandfatherOf",
            "greatGrandmotherOf",
            "greatGrandfatherOf",
            "auntOf",
            "uncleOf",
            "greatAuntOf",
            "greatUncleOf",
            "secondAuntOf",
            "secondUncleOf",
            "girlCousinOf",
            "boyCousinOf",
            "girlSecondCousinOf",
            "boySecondCousinOf",
            "girlFirstCousinOnceRemovedOf",
            "boyFirstCousinOnceRemovedOf",
            "daughterOf",
            "sonOf",
            "granddaughterOf",
            "grandsonOf",
            "greatGranddaughterOf",
            "greatGrandsonOf",
            "nieceOf",
            "nephewOf"
    ]
    """list: A list of all relations to include in a family tree dataset. List indices correspond to relation indices.
    """
    
    ONTOLOGY_PATH = "src/main/asp/ontology.asp"
    """str: The path of the answer set program that specifies the used ontology."""
    
    #  CONSTRUCTOR  ####################################################################################################
    
    def __init__(self):
        raise NotImplementedError("The class Generator cannot be instantiated!")
    
    #  METHODS  ########################################################################################################
    
    @classmethod
    def _print_distribution(cls, counts: typing.Dict[str, int]):
        """Prints a visualization of the distribution of the given counts to the screen."""
        # fetch all names from the data
        all_names = sorted(counts.keys())
    
        # get maximum count
        max_count = max(counts.values())

        # compute step size, i.e., the "width" of a bar
        step_size = max_count / cls.BAR_CHART_STEPS

        # various lengths needed for aligned printing
        index_len = len(str(len(counts)))           # length of highest index
        label_len = max(len(n) for n in all_names)  # length of longest label
        num_len = len(str(max_count))               # length of highest count

        # create pattern for printing a single line
        stats_pattern = "{{index:{}}} {{name:{}}}  {{count:{}}} {{bars:{}}}".format(
                index_len,
                label_len,
                num_len,
                cls.BAR_CHART_STEPS
        )

        # iterate over all names
        for idx, n in enumerate(all_names, start=1):

            # create the bars to print
            bars = "|" * int(math.ceil(counts[n] / step_size))
            
            # print stats line
            print(stats_pattern.format(index=idx, name=n, count=counts[n], bars=bars))
    
    @classmethod
    def _print_stats(cls, pos_counts: typing.Dict[str, int], neg_counts: typing.Dict[str, int]):
        """Prints statistics for the given counts to the screen."""
        # fetch all names from the data
        all_names = sorted(pos_counts.keys())
        
        # get maximum counts
        max_pos = max(pos_counts.values())
        max_neg = max(neg_counts.values())
        
        # compute step size, i.e., the "width" of a bar
        step_size = max(max_pos, max_neg) / cls.BAR_CHART_STEPS
        
        # various lengths needed for aligned printing
        index_len = len(str(len(pos_counts)))       # length of highest index
        label_len = max(len(n) for n in all_names)  # length of longest label
        pos_len = len(str(max_pos))                 # length of highest positive count
        neg_len = len(str(max_neg))                 # length of highest negative count
    
        # create pattern for printing a single line
        stats_pattern = "{{index:{}}} {{name:{}}}  {{num_pos:{}}} {{pos_bars:>{}}}{{neg_bars:{}}} {{num_neg:{}}}".format(
                index_len,
                label_len,
                pos_len,
                int(math.ceil(max_pos / step_size)),
                int(math.ceil(max_neg / step_size)),
                neg_len
        )
        
        # iterate over all names
        for idx, n in enumerate(all_names, start=1):
            
            # create the bars to print
            pos_bars = "+" * int(math.ceil(pos_counts[n] / step_size))
            neg_bars = "-" * int(math.ceil(neg_counts[n] / step_size))
            
            # print stats line
            print(
                    stats_pattern.format(
                            index=idx,
                            name=n,
                            pos_bars=pos_bars,
                            neg_bars=neg_bars,
                            num_pos=pos_counts[n],
                            num_neg=neg_counts[n]
                    )
            )
    
    @classmethod
    def _run_asp_solver(cls, conf: config.Config, family_tree: typing.List[person.Person]) -> aspwrapper.AnswerSet:
        """Runs the used ASP solver to compute all inferences resulting from the provided family tree.
        
        Args:
            conf (:class:`config.Config`): The configuration that specifies how to create the dataset.
            family_tree (list[:class:`person.Person`): A family tree specified as list of persons.
        
        Returns:
            aspwrapper.AnswerSet: The resulting answer set.
        """
        facts = []  # used to store all of the created facts
        
        # iterate over all persons in the provided family tree, and create all facts necessary to describe the same
        for p in family_tree:
        
            # add a fact specifying the person's gender
            if p.female:
                facts.append(aspwrapper.Literal("female", [p.name]))
            else:
                facts.append(aspwrapper.Literal("male", [p.name]))
            
            # add a fact for specifying a parent-of relation for each of the person's children
            for c in p.children:
                facts.append(aspwrapper.Literal("parentOf", [p.name, c.name]))
        
        # run the ASP solver to compute all inferences
        return aspwrapper.DlvSolver(conf.dlv).run(cls.ONTOLOGY_PATH, facts)[0]
    
    @classmethod
    def _sample_family_tree(cls, conf: config.Config) -> typing.List[person.Person]:
        """Creates a single family tree.
        
        Args:
            conf (:class:`config.Config`): The configuration that specifies how to create the dataset.
        
        Returns:
            list[:class:`person.Person`]: The created family tree specified as a list of persons appearing in the same.
                All of the according parent-of relations are specified in terms of the provided instances.
        """
        # add first person to the family tree
        fam_tree = [pf.PersonFactory.create_person(conf.max_tree_depth)]

        min_level = fam_tree[0].tree_level
        max_level = fam_tree[0].tree_level
        tree_depth = max_level - min_level
        p = 1
        total_attempts = 0  # the total number of attempts to add a person to the family tree
        while True:
    
            # randomly choose a person from the tree
            current_person = random.choice(fam_tree)
            
            # determine whether it is possible to ad parents and children of the sampled person
            can_add_parents = (
                    not current_person.parents and
                    (current_person.tree_level > min_level or tree_depth < conf.max_tree_depth)
            )
            can_add_children = (
                    len(current_person.children) < conf.max_branching_factor and
                    (current_person.tree_level < max_level or tree_depth < conf.max_tree_depth)
            )
            
            # decide what to do
            add_parents = False
            add_child = False
            if can_add_parents and can_add_children:  # -> randomly add either a child or parents
                if random.random() > 0.5:
                    add_parents = True
                else:
                    add_child = True
            elif can_add_parents:
                add_parents = True
            elif can_add_children:
                add_child = True
    
            if add_child:
        
                # check whether the chosen person is married, if not -> add a partner
                if current_person.married_to:
                    spouse = current_person.married_to
                else:
                    spouse = pf.PersonFactory.create_person(
                            current_person.tree_level + 1,
                            female=not current_person.female
                    )
                    spouse.married_to = current_person
                    current_person.married_to = spouse
                    fam_tree.append(spouse)
                    p += 1
        
                # create child
                child = pf.PersonFactory.create_person(current_person.tree_level + 1)
                child.parents.append(current_person)
                child.parents.append(spouse)
                fam_tree.append(child)
                p += 1
        
                # add child to current person and spouse
                current_person.children.append(child)
                spouse.children.append(child)
    
            elif add_parents:
        
                # create mother
                mom = pf.PersonFactory.create_person(current_person.tree_level - 1, female=True)
                mom.children.append(current_person)
                fam_tree.append(mom)
                p += 1
        
                # create father
                dad = pf.PersonFactory.create_person(current_person.tree_level - 1, female=False)
                dad.children.append(current_person)
                fam_tree.append(dad)
                p += 1
        
                # specify parents to be married
                mom.married_to = dad
                dad.married_to = mom
        
                # specify parents of chosen person
                current_person.parents.append(mom)
                current_person.parents.append(dad)
            
            # update bookkeeping variables
            total_attempts += 1
            if add_parents:
                min_level = min(min_level, current_person.tree_level - 1)
            elif add_child:
                max_level = max(max_level, current_person.tree_level + 1)
            tree_depth = max_level - min_level
    
            # stop adding people of maximum number has been reached
            if (
                    p >= conf.max_tree_size or
                    total_attempts >= conf.max_tree_size * 10 or
                    (conf.stop_prob > 0 and random.random() < conf.stop_prob)
            ):
                break

        return fam_tree

    @classmethod
    def _write_sample(
            cls,
            conf: config.Config,
            family_tree: typing.List[person.Person],
            data: aspwrapper.AnswerSet,
            base_name: str
    ) -> None:
        """Writes the provided sample as as knowledge graph to the disk.
        
        Args:
            conf (:class:`config.Config`): The configuration that specifies how to create the dataset.
            family_tree (list[:class:`person.Person`]): The specification of the family tree as list of persons.
            data (aspwrapper.AnswerSet): All facts and inferences included in the sample.
            base_name (str): The base name for the files created on the disk.
        """
        # create class and relation types
        classes = {c: ctf.ClassTypeFactory.create_class(c) for c in cls.CLASSES}
        relations = {r: rtf.RelationTypeFactory.create_relation(r) for r in cls.RELATIONS}
    
        # create dictionary that maps names to individual objects
        individuals = {i.name: i for i in family_tree}
    
        # create knowledge graph
        kg = knowledge_graph.KnowledgeGraph()
    
        # specify vocabulary
        kg.classes.add_all(classes.values())
        kg.relations.add_all(relations.values())
    
        # add individuals to knowledge graph
        kg.individuals.add_all(family_tree)
    
        # fetch facts and inferences
        facts = list(data.facts)
        inferences = list(data.inferences)
    
        # if negative facts shall be used, then move inferred ~parentOf predicates from inferences to facts
        if conf.negative_facts:
            facts += [i for i in inferences if i.predicate == "parentOf"]
            inferences = [i for i in inferences if i.predicate != "parentOf"]
    
        # sort all facts and inferences (this ensures exact reproducibility)
        facts = sorted(facts, key=lambda x: str(x))
        inferences = sorted(inferences, key=lambda x: str(x))
    
        # add all facts to the knowledge graph
        for f in facts:
            if len(f.terms) == 1:
                if f.predicate in cls.CLASSES:
                    individuals[f.terms[0]].classes.add(
                            class_membership.ClassMembership(
                                    classes[f.predicate],
                                    f.positive
                            )
                    )
            elif f.predicate in cls.RELATIONS:
                kg.triples.add(
                        triple.Triple(
                                individuals[f.terms[0]],
                                relations[f.predicate],
                                individuals[f.terms[1]],
                                f.positive
                        )
                )
    
        # add all inferences to the knowledge graph
        for i in inferences:
            if len(i.terms) == 1:
                if i.predicate in cls.CLASSES:
                    individuals[i.terms[0]].classes.add(
                            class_membership.ClassMembership(
                                    classes[i.predicate],
                                    i.positive,
                                    inferred=True
                            )
                    )
            elif i.predicate in cls.RELATIONS:
                kg.triples.add(
                        triple.Triple(
                                individuals[i.terms[0]],
                                relations[i.predicate],
                                individuals[i.terms[1]],
                                i.positive,
                                inferred=True
                        )
                )
    
        # write created knowledge graph to disk
        kg_writer.KgWriter.write(kg, conf.output_dir, base_name)
    
    @classmethod
    def generate(cls, conf: config.Config) -> None:
        """Generates a family tree dataset based on the provided configuration.
        
        Args:
            conf (:class:`config.Config`): The configuration that specifies how to create the dataset.
        """
        # a pattern that describes the base names of the created samples
        sample_name_pattern = "{:0" + str(len(str(conf.num_samples - 1))) + "d}"
        
        # numerous counters for computing data statistics
        tree_size_counts = [0] * (conf.max_tree_size + 2)  # +2 rather than +1 -> adding of spouses
        total_relations_counts = [0] * (conf.max_branching_factor ** conf.max_tree_depth)
        inferences_pos_relation_counts = {r: 0 for r in cls.RELATIONS}
        inferences_neg_relation_counts = {r: 0 for r in cls.RELATIONS}
        
        # create list for storing graph representations of all created samples (for checking isomorphism)
        sample_graphs = []
        
        for sample_idx in range(conf.num_samples):
            
            print("creating sample #{}: ".format(sample_idx), end="")
            
            # use a fresh data context
            with dc.DataContext() as data_ctx:
                
                # reset person factory
                pf.PersonFactory.reset()

                total_start = time.time()
                    
                # sample family tree
                print("sampling family tree", end="")
                start = time.time()
                done = False
                while not done:
                    
                    # randomly sample a tree
                    family_tree = cls._sample_family_tree(conf)
                    
                    # create a graph that represents the structure of the created sample for checking isomorphism
                    current_graph = nx.DiGraph()
                    for p in family_tree:
                        for parent in p.parents:
                            current_graph.add_edge(p.index, parent.index)
                        if p.married_to is not None:
                            current_graph.add_edge(p.index, p.married_to.index)
                    
                    # check whether the new sample is isomorphic to any sample created earlier
                    for existing_sample in sample_graphs:
                        if nx.is_isomorphic(existing_sample, current_graph):
                            data_ctx.clear()
                            pf.PersonFactory.reset()
                            break
                    else:
                        sample_graphs.append(current_graph)
                        done = True
                    
                print(" OK ({:.3f}s)".format(time.time() - start), end="")
        
                # run ASP solver to compute all inferences
                print(" | computing inferences", end="")
                start = time.time()
                data = cls._run_asp_solver(conf, family_tree)
                print(" OK ({:.3f}s)".format(time.time() - start), end="")
    
                # write sample to disk
                print(" | writing to disk", end="")
                start = time.time()
                cls._write_sample(conf, family_tree, data, sample_name_pattern.format(sample_idx))
                print(" OK ({:.3f}s) | ".format(time.time() - start), end="")
                
                # update statistics
                tree_size_counts[len(family_tree)] += 1
                total_relations_counts[sum((len(p.children) for p in family_tree))] += 1
                for i in data.inferences:
                    if len(i.terms) == 2 and i.predicate in cls.RELATIONS:
                        if i.positive:
                            inferences_pos_relation_counts[i.predicate] += 1
                        else:
                            inferences_neg_relation_counts[i.predicate] += 1
                
                print("finished in {:.3f}s".format(time.time() - total_start))
        
        print()  # add an empty line to the output
        
        # prepare tree-size-statistics for printing
        title_format = "size={{:0{}d}}".format(len(str(conf.max_tree_size + 1)))
        tree_size_counts = {
                title_format.format(size): counts
                for size, counts in enumerate(tree_size_counts)
                if size > 1
        }

        # prepare total-number-of-relations-statistics for printing
        max_relations = max((size for size, counts in enumerate(total_relations_counts) if counts > 0))
        title_format = "#relations={{:0{}d}}".format(len(str(max_relations)))
        total_relations_counts = {
                title_format.format(size): counts
                for size, counts in enumerate(total_relations_counts)
                if size <= max_relations
        }
        
        # print statistics
        print("DISTRIBUTION OF FAMILY TREE SIZES\n")
        cls._print_distribution(tree_size_counts)
        print("\nDISTRIBUTION OF TOTAL NUMBER OF RELATIONS PER SAMPLE\n")
        cls._print_distribution(total_relations_counts)
        print("\nINFERABLE RELATIONS\n")
        cls._print_stats(inferences_pos_relation_counts, inferences_neg_relation_counts)
        print("\nDISTRIBUTION OF POSITIVE RELATION INFERENCES\n")
        cls._print_distribution(inferences_pos_relation_counts)
        print("\nDISTRIBUTION OF NEGATIVE RELATION INFERENCES\n")
        cls._print_distribution(inferences_neg_relation_counts)
