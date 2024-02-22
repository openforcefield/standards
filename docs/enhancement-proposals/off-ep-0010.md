# OFF-EP 0010 — Clarify ProperTorsion implementation of idivf and dihedral calculation

**Status:** Submitted

**Authors:** Lily Wang

**Acceptance criteria:** Unanimity (4 approving reviews) or partial support (2 approvals and 2 week period with no reviews requesting changes)[https://openforcefield.atlassian.net/wiki/spaces/MEET/pages/2638774273/09-05-23+SMIRNOFF+Committee+Meeting]

**Stakeholders:** John Chodera, David Mobley, Jeff Wagner, Lily Wang, Matt Thompson

**Created:** 2024-02-07

**Discussion:** [Issue #59](https://github.com/openforcefield/standards/issues/59), [Issue #60](https://github.com/openforcefield/standards/issues/60)

**Implementation:** [``openforcefield/standards``](https://github.com/openforcefield/standards)

## Abstract

This change clarifies the implementation of SMIRKS matching, dihedral calculation, and `idivf="auto"` for ProperTorsion parameters.

## Motivation and Scope

A ProperTorsion is defined between a connected quartet of atoms `i-j-k-l`. The dihedral angle is calculated between the two planes defined by `i-j-k` and `j-k-l`. The directions of these planes, and the resulting sign of the dihedral, depend on how they are defined; however, it is currently unclear what standard to follow. While both directions yield the same result for symmetric torsions where the phase is 0 or pi, the choice of direction is important for for asymmetric torsions.

In addition, a SMIRKS pattern that can match a particular 
bonded quartet in either `i-j-k-l` or `l-k-j-i` order is 
ambiguous, and the SMIRNOFF specification does not 
guarantee that the match will be performed in any predetermined or deterministic order. As this may
potentially lead to undesired results, this proposal
adds a note highlighting this fact.

Finally, the effect of the `idivf="auto"` parameter on the ProperTorsion potential is outlined in words that can be interpreted ambiguously.

All of these ambiguities may cause confusion to anybody implementing the SMIRNOFF spec.

## Usage and Impact

This change defines the ``idivf`` parameter in line with the philosophy used in AMBER force fields. The OpenFF implementation has not hitherto used or implemented ``idivf="auto"`` in its ProperTorsion parameters. As such there should be no practical impact on existing workflows and simulations. Other force fields and software that have implemented and interpreted the `idivf="auto"` parameter in ways that do not align with our definition will need to be updated accordingly.

The proposed clarification of input vector order and symmetric SMIRKS matching reflects existing implementations and simulations in OpenFF and OpenMM. Software that converts systems out into other formats may need to adjust the input order to ensure the correct sign of the torsion.

## Backward compatibility

This proposal does not change behaviour, but rather explicitly defines what is currently implicit in the
specification and the implementation in OpenFF infrastructure.
Therefore, there should be no backwards compatibility issues.

## Detailed description

This proposal adds the following section (bolded) clarifying ``idivf`` to the ``ProperTorsion`` spec:

> For convenience, an optional attribute specifies a torsion multiplicity by which the barrier height (``k#``) should be divided (`idivf#`). **The final barrier height is calculated as ``k#/idivf#``. ``idivf`` can be assigned an integer value (such as `"1"`), or `"auto"`. If `idivf="auto"`, the following equation is used to determine the ``idivf`` value for a torsion applying to four atoms `i-j-k-l`, where ``n_j`` refers to the degree (i.e. number of bonds) of atom `j`:**
> 
> **```**
> **idivf = (n_j - 1) * (n_k - 1)**
> **```**
> 
> The default behavior of this ``idivf`` can be controlled by the top-level attribute `default_idivf` (default: `"auto"`) for `<ProperTorsions>`.

It also adds a section explaining the computation of ``theta`` to the ``ProperTorsion`` spec:

> In the potential function, the angle ``theta`` is calculated using input vectors
> defined by the four atoms of the torsion `i-j-k-l`.
> Where the vector ``r_ij`` is defined as the vector from atom `j` to atom `i`:
> ```
> r_ij = x_i - x_j
> ```
> the angle ``theta`` should be calculated using the input vectors ``r_ij``, ``r_kj``, and ``r_kl``.
> The directionality or sign of the angle is determined by comparing the `r_ij` vector to the `u_jkl` plane. If the angle is acute, the sign is positive; if obtuse, the sign is negative.
> 
> ```
> u_ijk = r_ij x r_kj
> u_jkl = r_kj x r_kl
> angle = acos(u_ijk • u_jkl)
> 
> rij_to_ujkl = r_ij • u_jkl
> if rij_to_ujkl < 0:
>     sign = -1
> else:
>     sign = 1
> theta = sign * angle
> ```
> 
> The directionality of the ``theta`` angle is important in cases where the torsion profile is asymmetric,
> i.e. where the ``phase`` is neither 0 nor pi.

And finally adds a note on how ProperTorsion SMIRKS are applied:

> !!! note
>     A SMIRKS pattern that can match a particular bonded 
>     quartet in either `i-j-k-l` or `l-k-j-i` order is 
>     ambiguous, and the specification cannot guarantee the 
>     match will be performed in any predetermined or 
>     deterministic order, potentially leading to undesired 
>     and undefined results.

## Alternatives

### Alternative 1: the `idivf` parameter could be removed

In this alternative scenario, `idivf` would be implicitly set to `1`, as has been the case
in current SMIRNOFF force fields. Torsion parameters would be explicitly enumerated
to only apply to one specific multiplicity, and the `k` barrier would be appropriately fit
to the required scale.

The approach of keeping and implementing `idivf="auto"` was chosen to enable scientific
experiments to investigate whether torsion multiplicity could be accounted for using `idivf`,
reducing the number of necessary parameters to fit.

### Alternative 2: disallow asymmetric torsions

In this alternative scenario, proper torsion parameters with asymmetric profiles
(e.g. with phases outside 0 or pi) would be explicitly disallowed in the SMIRNOFF spec
and OpenFF infrastructure. An error would be raised on reading these. This would render concerns about dihedral sign and the impact of atom order superfluous.

The approach of keeping asymmetric torsions was chosen to:
    * enable reading our existing Sage 2.0 force field, which was published with asymmetric torsions
    * allow asymmetric torsions for future research

## Discussion

- [Description of default_idivf="auto" not in accordance with community understanding](https://github.com/openforcefield/standards/issues/60)
- Suggestion to [Remove use of idivf](https://github.com/openforcefield/standards/issues/59)
- [Slack thread clarifying dihedral computation in OpenMM](https://openforcefieldgroup.slack.com/archives/C4VHEFXS5/p1707080215101849)
- This proposal was discussed at a [SMIRNOFF committee meeting](https://openforcefield.atlassian.net/wiki/spaces/MEET/pages/2730000385/02-06-24+SMIRNOFF+Committee+Meeting) with the following points:
    - The history of the `idivf` parameter stems from AMBER
    - `idivf` is not currently used in SMIRNOFF force fields with values other than 1
    - `idivf="auto"` is not currently implemented in OpenFF infrastructure
    - An implementation of `idivf` could simply take into account molecular topology
    - `idivf="auto"` can be defined using the degree of the atoms in the central bond
    - Sage 2.0 did contain asymmetric torsions, where the sign of the dihedral affects the potential
    - Measuring a dihedral angle from i-j-k-l *should* always give the same result as l-k-j-i 

## Copyright

*This template is based upon the [``numpy`` NEP template](
https://github.com/numpy/numpy/blob/master/doc/neps/nep-template.rst) and the
[``conda-forge`` CFEP template.](https://github.com/conda-forge/cfep/blob/master/cfep-00.md)*

*All OFF-EPs are explicitly [CC0 1.0 Universal](https://creativecommons.org/publicdomain/zero/1.0/).*
