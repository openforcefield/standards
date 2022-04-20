# OFF-EP 6 — Define virtual site exclusion policy

**Status:** Accepted

**Authors:** Simon Boothroyd, simon.boothroyd@openforcefield.org

**Stakeholders:** David Mobley, John Chodera, Jeffrey Wagner, Simon Boothroyd

**Acceptance criteria:** Majority

**Created:** 2022-04-05

**Discussion:** [PR #35](https://github.com/openforcefield/standards/pull/35)

**Implementation:** [PR #35](https://github.com/openforcefield/standards/pull/35)

## Abstract

This OFF-EP aims to [define the allowed virtual site exclusion policies](#detailed-description), which are currently
only listed without definition.

## Motivation and Scope

The virtual site section of the SMIRNOFF specification states that the top level `<VirtualSites>`parameter handler 
allows an `exclusion_policy` to be defined, and the corresponding allowed values table (currently version 0.3) states 
that the only allowed value is `parents`. The section does not however define what this means, nor does it address how 
virtual site interactions are influenced by 1-N scale factors.

## Usage and Impact

Usage of virtual sites is understood to be currently limited to internal users on the OpenFF scientific team, and 
mostly only limited to TIP4P water which should likely not need exclusions. As such, the impact of changing 
the definition of the exclusion policy, even to one that doesn't necessarily agree with the current reference 
implementation in the OpenFF toolkit, should be minimal to none.

## Backward compatibility

The [proposed definition](#detailed-description) conflicts with the OpenFF Toolkit reference implementation of the 
`parents` exclusion policy, that currently assumes:

> the user would want to exclude all non-bonded interactions between the virtual site and each 'parent atom' used to 
  define the virtual sites' orientation and does no interaction scaling using, for example, the vdW or electrostatics 
  `scale14` factor.

This would mean that new versions of the reference implementation would yield different energies for molecules that
contain greater than three atoms, and hence not be backwards compatible.

To retain previous behaviour we could in principle incorporate the proposed definition as a new allowed exclusion 
policy, `'inherit'`, however given the low (to zero) number of users this change would affect it is unclear that it
is worth the extra maintenance burden, and is likely an acceptable break.

## Detailed description

This OFF-EP proposes defining the `parents` virtual site exclusion policy to mean:

> virtual site particles should exclude non-bonded interactions with, or scale their interactions with, the same atoms 
> as the main 'parent atom' that they are attached to does. Which atom is the 'parent atom' depends on the type of
> virtual site: for `BondCharge`, `MonovalentLonePair`, `DivalentLonePair`, and `TrivalentLonePair` types, it is the 
> atom labelled `:1` in the SMIRKS pattern.
>
> As an example, if the parent atom is separated by two bonds from another atom i.e a 1-3 pair, the virtual sites'
> interaction with that other atom should also be treated as a 1-3 pair. Similarly, if the parent atom is separated by 
> three bonds from another atom i.e a 1-4 pair, the virtual sites' interaction with that other atom should also be 
> treated as a 1-4 pair and the interaction should be scaled by the appropriate `scale14` factor. 

## Alternatives

* Implement the proposed definition as a new allowed value as described in the [backward compatibility](#backward-compatibility) 
  section. As mentioned however, it is not clear that the current `parents` implementation is broadly used, nor does it 
  take into account important settings such as 1-4 scaling factors, and hence it is likely justified to just overwrite
  the reference.

## Discussion

This preferred exclusion policy has been discussed by [external collaborators previously](https://github.com/openmm/openmm/issues/2045),
who have also settled on the same definition as is proposed here.

## Copyright

*This template is based upon the [``numpy`` NEP template](
https://github.com/numpy/numpy/blob/master/doc/neps/nep-template.rst) and the
[``conda-forge`` CFEP template.](https://github.com/conda-forge/cfep/blob/master/cfep-00.md)*

*All OFF-EPs are explicitly [CC0 1.0 Universal](https://creativecommons.org/publicdomain/zero/1.0/).*
