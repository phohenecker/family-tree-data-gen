% 2-Clause BSD License
%
% Copyright (c) 2018, Patrick Hohenecker
% All rights reserved.
%
% Redistribution and use in source and binary forms, with or without
% modification, are permitted provided that the following conditions are met:
%
% 1. Redistributions of source code must retain the above copyright notice, this
%    list of conditions and the following disclaimer.
% 2. Redistributions in binary form must reproduce the above copyright notice,
%    this list of conditions and the following disclaimer in the documentation
%    and/or other materials provided with the distribution.
%
% THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
% ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
% WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
% DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
% ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
% (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
% LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
% ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
% (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
% SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

% author:   Patrick Hohenecker (mail@paho.at)
% version:  2018.1
% date:     May 30, 2018


% The predicate person is needed in order to allow for the use of the default negation rules that are specified at the
% end. However, as we only consider individuals representing persons, this predicate does not provide any insights.

person(X) :- male(X)        .
person(X) :- female(X)      .
person(X) :- parentOf(X, Y) .
person(Y) :- parentOf(X, Y) .


%%%%%%%% SAFETY RULES %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

:- ~person(X)                     .
:- male(X), female(X)             .
:- ~male(X), ~female(X)           .
:- parentOf(X, Y), parentOf(Y, X) .


%%%%%%%% GENDERS %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

~female(X) :- male(X)   .
~male(X)   :- female(X) .


%%%%%%%% FAMILY RELATIONSHIPS %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%%%% Top-down Relationships --------------------------------------------------------------------------------------------

grandparentOf(X, Y)      :- parentOf(X, Z), parentOf(Z, Y)         .
greatGrandparentOf(X, Y) :- parentOf(X, Z), grandparentOf(Z, Y)    .

auntUncleOf(X, Y)        :- siblingOf(X, Z), parentOf(Z, Y)        .
greatAuntUncleOf(X, Y)   :- siblingOf(X, Z), grandparentOf(Z, Y)   .
secondAuntUncleOf(X, Y)  :- parentOf(Z, X), greatAuntUncleOf(Z, Y) .

%%%% Bottom-up Relationships -------------------------------------------------------------------------------------------

childOf(X, Y)           :- parentOf(Y, X)           .
grandchildOf(X, Y)      :- grandparentOf(Y, X)      .
greatGrandchildOf(X, Y) :- greatGrandparentOf(Y, X) .
nieceNephewOf(X, Y)     :- auntUncleOf(Y, X)        .

%%%% Other/Sideways Relationships --------------------------------------------------------------------------------------

siblingOf(X, Y)                :- siblingOf(Y, X)                         .
siblingOf(X, Y)                :- parentOf(Z, X), parentOf(Z, Y), X<>Y    .

cousinOf(X, Y)                 :- cousinOf(Y, X)                          .
cousinOf(X, Y)                 :- parentOf(Z, X), auntUncleOf(Z, Y)       .
secondCousinOf(X, Y)           :- secondCousinOf(Y, X)                    .
secondCousinOf(X, Y)           :- parentOf(Z, X), secondAuntUncleOf(Z, Y) .
firstCousinOnceRemovedOf(X, Y) :- cousinOf(Y, Z), parentOf(Z, X)          .  % german: Nichte/Neffe 2. Grades


%%%%%%%% GENDERED RELATIONSHIPS %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

sisterOf(X, Y)                     :- siblingOf(X, Y), female(X)                .
brotherOf(X, Y)                    :- siblingOf(X, Y), male(X)                  .
motherOf(X, Y)                     :- parentOf(X, Y), female(X)                 .
fatherOf(X, Y)                     :- parentOf(X, Y), male(X)                   .
grandmotherOf(X, Y)                :- grandparentOf(X, Y), female(X)            .
grandfatherOf(X, Y)                :- grandparentOf(X, Y), male(X)              .
greatGrandmotherOf(X, Y)           :- greatGrandparentOf(X, Y), female(X)       .
greatGrandfatherOf(X, Y)           :- greatGrandparentOf(X, Y), male(X)         .

auntOf(X, Y)                       :- auntUncleOf(X, Y), female(X)              .
uncleOf(X, Y)                      :- auntUncleOf(X, Y), male(X)                .
greatAuntOf(X, Y)                  :- greatAuntUncleOf(X, Y), female(X)         .
greatUncleOf(X, Y)                 :- greatAuntUncleOf(X, Y), male(X)           .
secondAuntOf(X, Y)                 :- secondAuntUncleOf(X, Y), female(X)        .
secondUncleOf(X, Y)                :- secondAuntUncleOf(X, Y), male(X)          .

girlCousinOf(X, Y)                 :- cousinOf(X, Y), female(X)                 .
boyCousinOf(X, Y)                  :- cousinOf(X, Y), male(X)                   .
girlSecondCousinOf(X, Y)           :- secondCousinOf(X, Y), female(X)           .
boySecondCousinOf(X, Y)            :- secondCousinOf(X, Y), male(X)             .
girlFirstCousinOnceRemovedOf(X, Y) :- firstCousinOnceRemovedOf(X, Y), female(X) .
boyFirstCousinOnceRemovedOf(X, Y)  :- firstCousinOnceRemovedOf(X, Y), male(X)   .

daughterOf(X, Y)                   :- childOf(X, Y), female(X)                  .
sonOf(X, Y)                        :- childOf(X, Y), male(X)                    .
granddaughterOf(X, Y)              :- grandchildOf(X, Y), female(X)             .
grandsonOf(X, Y)                   :- grandchildOf(X, Y), male(X)               .
greatGranddaughterOf(X, Y)         :- greatGrandchildOf(X, Y), female(X)        .
greatGrandsonOf(X, Y)              :- greatGrandchildOf(X, Y), male(X)          .
nieceOf(X, Y)                      :- nieceNephewOf(X, Y), female(X)            .
nephewOf(X, Y)                     :- nieceNephewOf(X, Y), male(X)              .


%%%%%%%% DEFAULT NEGATION %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

~parentOf(X, Y)                     :- not parentOf(X, Y)                     , person(X), person(Y) .
~grandparentOf(X, Y)                :- not grandparentOf(X, Y)                , person(X), person(Y) .
~greatGrandparentOf(X, Y)           :- not greatGrandparentOf(X, Y)           , person(X), person(Y) .
~auntUncleOf(X, Y)                  :- not auntUncleOf(X, Y)                  , person(X), person(Y) .
~greatAuntUncleOf(X, Y)             :- not greatAuntUncleOf(X, Y)             , person(X), person(Y) .
~secondAuntUncleOf(X, Y)            :- not secondAuntUncleOf(X, Y)            , person(X), person(Y) .
~childOf(X, Y)                      :- not childOf(X, Y)                      , person(X), person(Y) .
~grandchildOf(X, Y)                 :- not grandchildOf(X, Y)                 , person(X), person(Y) .
~greatGrandchildOf(X, Y)            :- not greatGrandchildOf(X, Y)            , person(X), person(Y) .
~nieceNephewOf(X, Y)                :- not nieceNephewOf(X, Y)                , person(X), person(Y) .
~siblingOf(X, Y)                    :- not siblingOf(X, Y)                    , person(X), person(Y) .
~cousinOf(X, Y)                     :- not cousinOf(X, Y)                     , person(X), person(Y) .
~secondCousinOf(X, Y)               :- not secondCousinOf(X, Y)               , person(X), person(Y) .
~firstCousinOnceRemovedOf(X, Y)     :- not firstCousinOnceRemovedOf(X, Y)     , person(X), person(Y) .
~sisterOf(X, Y)                     :- not sisterOf(X, Y)                     , person(X), person(Y) .
~brotherOf(X, Y)                    :- not brotherOf(X, Y)                    , person(X), person(Y) .
~motherOf(X, Y)                     :- not motherOf(X, Y)                     , person(X), person(Y) .
~fatherOf(X, Y)                     :- not fatherOf(X, Y)                     , person(X), person(Y) .
~grandmotherOf(X, Y)                :- not grandmotherOf(X, Y)                , person(X), person(Y) .
~grandfatherOf(X, Y)                :- not grandfatherOf(X, Y)                , person(X), person(Y) .
~greatGrandmotherOf(X, Y)           :- not greatGrandmotherOf(X, Y)           , person(X), person(Y) .
~greatGrandfatherOf(X, Y)           :- not greatGrandfatherOf(X, Y)           , person(X), person(Y) .
~auntOf(X, Y)                       :- not auntOf(X, Y)                       , person(X), person(Y) .
~uncleOf(X, Y)                      :- not uncleOf(X, Y)                      , person(X), person(Y) .
~greatAuntOf(X, Y)                  :- not greatAuntOf(X, Y)                  , person(X), person(Y) .
~greatUncleOf(X, Y)                 :- not greatUncleOf(X, Y)                 , person(X), person(Y) .
~secondAuntOf(X, Y)                 :- not secondAuntOf(X, Y)                 , person(X), person(Y) .
~secondUncleOf(X, Y)                :- not secondUncleOf(X, Y)                , person(X), person(Y) .
~girlCousinOf(X, Y)                 :- not girlCousinOf(X, Y)                 , person(X), person(Y) .
~boyCousinOf(X, Y)                  :- not boyCousinOf(X, Y)                  , person(X), person(Y) .
~girlSecondCousinOf(X, Y)           :- not girlSecondCousinOf(X, Y)           , person(X), person(Y) .
~boySecondCousinOf(X, Y)            :- not boySecondCousinOf(X, Y)            , person(X), person(Y) .
~girlFirstCousinOnceRemovedOf(X, Y) :- not girlFirstCousinOnceRemovedOf(X, Y) , person(X), person(Y) .
~boyFirstCousinOnceRemovedOf(X, Y)  :- not boyFirstCousinOnceRemovedOf(X, Y)  , person(X), person(Y) .
~daughterOf(X, Y)                   :- not daughterOf(X, Y)                   , person(X), person(Y) .
~sonOf(X, Y)                        :- not sonOf(X, Y)                        , person(X), person(Y) .
~granddaughterOf(X, Y)              :- not granddaughterOf(X, Y)              , person(X), person(Y) .
~grandsonOf(X, Y)                   :- not grandsonOf(X, Y)                   , person(X), person(Y) .
~greatGranddaughterOf(X, Y)         :- not greatGranddaughterOf(X, Y)         , person(X), person(Y) .
~greatGrandsonOf(X, Y)              :- not greatGrandsonOf(X, Y)              , person(X), person(Y) .
~nieceOf(X, Y)                      :- not nieceOf(X, Y)                      , person(X), person(Y) .
~nephewOf(X, Y)                     :- not nephewOf(X, Y)                     , person(X), person(Y) .
