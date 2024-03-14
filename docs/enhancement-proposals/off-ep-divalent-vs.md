# OFF-EP X — Template

**Status:** Draft

**Authors:** Tom Potter (Cresset)

**Stakeholders:** Users of SMIRNOFF virtual sites

**Acceptance criteria:** Acceptance by at least 3 of John Chodera, David Mobley, Lily Wang, or Jeff Wagner

**Created:** 2024-03-14

## Abstract

This change would update the SMIRNOFF `DivalentLonePair` virtual site specification to allow virtual sites to be defined using both
an in-plane and an out-of-plane angle, allowing this type to describe a wider range of virtual site geometries.

## Motivation and Scope

Virtual sites are often to used to model the electrostatic potential of a molecule, when a more accurate description is required than 
can be obtained by atom-centred charges, and the optimal positions for these sites vary significantly depending on the
chemical group and the use case.
The current implementation of `DivalentLonePair` sites allows the position of a virtual site to be specified with the `distance` and `outOfPlaneAngle` 
parameters. However, there are a number of useful virtual site geometries which cannot be achieved with these parameters. Using these geometries with a SMIRNOFF forcefield currently
requires additional editing of the simulation inputs, after parametrizing the molecule. Adding an
`inPlaneAngle` parameter would allow any virtual site position to be defined for functional groups matching a DivalentLonePair site, removing the need to add virtual site parameters
manually or with external tools.

## Usage and Impact

This parameter could be used in a number of chemical systems. For example, when modelling sulfur compounds such as thiophenes, virtual sites can be placed to represent sigma holes along the C-S bond axes (ie. in the plane of the C-S-C angle). 
This approach is taken in [OPLS4](https://pubmed.ncbi.nlm.nih.gov/34096718/) and the [Astex charge model](https://pubmed.ncbi.nlm.nih.gov/31553186/). In both cases, placing two in-plane and two out-of-plane sites on sulfur was found to give the best results. In the same Astex model, the orientations of sites on divalent atoms (such as oxygen in an alcohol group) were placed to best capture the ESP surface, and will not always exactly match the axis bisecting the bond angle, as described in the current `DivalentLonePair` specification.

Adding an out-of-plane angle would allow all of these virtual site models to be defined using a SMIRNOFF forcefield, as well as allowing users more flexibility to define their own virtual site geometries.

## Backward compatibility

This would require all DivalentLonePair sites to specify an inPlaneAngle parameter.
Any existing implementations of this site would need to add `inPlaneAngle="0.0 * degree"` to their definitions.

Alternatively, `inPlaneAngle` could be optional, with a default value of 0. This would keep backwards compatibility
with existing implementations.

## Detailed description

Examples of new virtual site definitions would be:
```
<VirtualSite
    type="DivalentLonePair"
    name="VS"
    smirks="[#16X2:1](~[*:2])~[*:3]"
    distance="0.4 * angstrom"
    charge_increment1="0.1*elementary_charge"
    outOfPlaneAngle="0.0 * degree"
    inPlaneAngle="60.0 * degree"
    match="all_permutations" >
</VirtualSite>
```
for an in-plane sulfur sites, or:
```
<VirtualSite
    type="DivalentLonePair"
    name="VS1"
    smirks="[#8X2:1](~[*:2])~[#1:3]"
    distance="0.4 * angstrom"
    charge_increment1="0.1*elementary_charge"
    outOfPlaneAngle="60.0 * degree"
    inPlaneAngle="20.0 * degree"
    match="once" >
</VirtualSite>
<VirtualSite
    type="DivalentLonePair"
    name="VS2"
    smirks="[#8X2:1](~[*:2])~[#1:3]"
    distance="0.4 * angstrom"
    charge_increment1="0.1*elementary_charge"
    outOfPlaneAngle="-60.0 * degree"
    inPlaneAngle="20.0 * degree"
    match="once" >
</VirtualSite>
```
for the off-centre -OH sites. Referring to the diagram in the [existing SMIRNOFF standards](https://openforcefield.github.io/standards/standards/smirnoff/#virtualsites-virtual-sites-for-off-atom-charges),
`inPlaneAngle` is the angle between the angle bisecting the 2-1-3 angle and the 1-VS vector.

These new definitions could be directly converted to existing virtual site types in common MD packages, including the LocalCoordinatesSite in OpenMM and the 3out site in Gromacs.

## Copyright

*This template is based upon the [``numpy`` NEP template](
https://github.com/numpy/numpy/blob/master/doc/neps/nep-template.rst) and the
[``conda-forge`` CFEP template.](https://github.com/conda-forge/cfep/blob/master/cfep-00.md)*

*All OFF-EPs are explicitly [CC0 1.0 Universal](https://creativecommons.org/publicdomain/zero/1.0/).*
