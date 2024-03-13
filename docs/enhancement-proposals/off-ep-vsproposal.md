# OFF-EP X — Template

**Status:** Draft

**Authors:** Tom Potter (Cresset)

**Stakeholders:** Cresset and other users of SMIRNOFF virtual sites

**Acceptance criteria:** Acceptance by at least 3 of John Chodera, David Mobley, Lily Wang, or Jeff Wagner

**Created:** &lt;date created>

**Discussion:** &lt;link to the PR / issue where proposal is being discussed>

**Implementation:** &lt;link an example / reference implementation of the proposal>

## Abstract

This change would update the SMIRNOFF DivalentLonePair virtual site specification to allow virtual sites to be defined using both
an in-plane and an out-of-plane angle.

## Motivation and Scope

The current implementation of DivalentLonePair sites allows the geometry to be specified with the distance and outOfPlaneAngle 
parameters. There are a number of useful virtual site geometries which cannot be achieved with these parameters. Adding an
inPlaneAngle parameter would allow these, and other geometries to be generated using the DivalentLonePair site.

## Usage and Impact

This section describes how users of the ecosystem will use features 
described in this SMIRNOFF EP. It should be comprised mainly of code / file 
examples that wouldn't  be possible without acceptance and implementation 
of this proposal, as well as the impact the proposed changes would have 
on the ecosystem. 

## Backward compatibility

This would require all DivalentLonePair sites to specify an inPlaneAngle parameter.
Any existing implementations would need to set this to 0 to capture the same geometries
as before. 

## Detailed description

This section should provide a detailed description of the proposed
change. It should include examples of how the new functionality would be
used, intended use-cases and pseudo-code illustrating its use.

## Copyright

*This template is based upon the [``numpy`` NEP template](
https://github.com/numpy/numpy/blob/master/doc/neps/nep-template.rst) and the
[``conda-forge`` CFEP template.](https://github.com/conda-forge/cfep/blob/master/cfep-00.md)*

*All OFF-EPs are explicitly [CC0 1.0 Universal](https://creativecommons.org/publicdomain/zero/1.0/).*
