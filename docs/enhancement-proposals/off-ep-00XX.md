# OFF-EP X — Template

**Status:** Draft

**Authors:** Lily Wang, Matt Thompson, Jeff Wagner

**Stakeholders:** &lt;list of stakeholders that would be affected by this proposal>

**Acceptance criteria:** 

**Created:** &lt;date created>

**Discussion:** &lt;link to the PR / issue where proposal is being discussed>

**Implementation:** &lt;link an example / reference implementation of the proposal>

## Abstract

This change adds a `<NAGLCharges>` tag which describes a graph-convolutional neural network (GNN) that can be used to assign atomic partial charges.

## Motivation and Scope

**Motivation:** OpenFF NAGL has built on existing work and trained a GNN that reproduced AM1-BCC ELF10 partial charges for a substantial set of chemistries. Currently, there is not a canonical method by which these GNN-provided charges can be requested in a SMIRNOFF force field. At the moment, a user can generate partial charges from a GNN and pass them to `create_interchange` or `create_openmm_system` alongside a SMIRNOFF force field as prespecified charges. To use GNNs in a flagship force field, this approach is not sufficient, and the SMIRNOFF specification must be updated to include enough information that an external developer have sufficient guidance to implement the charge method themselves. 

**Who this EP would affect:** The changes outlined in this proposal affect any consumer of SMIRNOFF force fields which include `<NAGLCharges>`, which is likely to be the case for `openff-2.3.0` and beyond. Since it is not a required section, force field developers who choose to use other partial charge methods would not be affected. SMIRNOFF implementations must implement `<NAGLCharges>`, by definition, to use force fields that include this section. Existing force fields cannot use this section, so they are not affected.

**Changes needed:** The contents of this proposal derive from the current structure of OpenFF NAGL and the model(s) it implements. If this proposal is accepted, OpenFF NAGL will need minor updates to properly check its GNN implementation against the details encoded in a SMIRNOFF force field, but we expect these changes will be minor because the proposed changes derive directly from this software. The OpenFF Toolkit and Interchange will need minor updates to properly support this section and some edge cases that arise from using this section in combination with other section(s) and tools, such as prespecified charges and virtual site parameter which modify charges. Similar tools which also implement the encoded GNN and/or the SMIRNOFF specification more broadly will need similar updates.

**Interaction with other sections:** This proposal does not include changes or interactions with sections that do not modify partial charges, such as `<vdW>`, `<Constraints>`, `<Bonds>`, `<Angles>`, etc.

`NAGLCharges` fits into the current charge hierarchy as follows (with methods high in the list taking priority over those lower):

- Pre-specified charges (charge_from_molecules)
- Library charges
- GNN charges
- ToolkitAM1BCC charges
- ChargeIncrementModel charges

The initial `0.3` version of the `NAGLCharges` section does have special interactions with virtual sites, though future versions of this section may include direct assignment of partial charges to virtual sites. If the `NAGLCharges` section is present in a force field with virtual sites, NAGL is used to assign initial charges to the molecule, and then virtual sites apply their charge increments on top of those initial charges. 

## Usage and Impact

This section describes how users of the ecosystem will use features 
described in this SMIRNOFF EP. It should be comprised mainly of code / file 
examples that wouldn't  be possible without acceptance and implementation 
of this proposal, as well as the impact the proposed changes would have 
on the ecosystem. 

## Backward compatibility

This proposal adds a new section which does not affect backwards compatibility. While in practice we intend for the NAGLCharges section to become the new default charge method in our future flagship force fields, we do not propose that existing force fields with the ToolkitAM1BCC section be assumed to be compatible with/automatically upgrade-able to NAGLCharges sections.

## Detailed description

This proposal adds a section named `<NAGLCharges`>. The initial version of this section, 0.3, is defined as follows:

The `NAGLCharges` top-level element defines that the force field should use the `openff-nagl` software to assign partial charges. It contains the following  attributes:

- `version`
- `weights`

The attribute `weights` points to a file that includes models weights. This by convention is a PyTorch `.pt` file containing additional information about the model that is read by the `openff-nagl` software. By their nature, GNNs use many more weights than can reasonably be encoded into an XML file, so pointing to an external file is a necessary and unavoidable layer of complexity.

The `NAGLCharges` top-level element contains the following elements:

- `AtomFeatures`: information about atom features
- `BondFeatures`: information about bond features

Both of the inner elements - `AtomFeatures` and `BondFeatures` - operate on a "resonance-averaged" representation of the molecule. This representation is generated by enumerating all resonance forms of the molecule using the method described in [Gilson et al.](https://pubs.acs.org/doi/10.1021/ci034148o), and then averaging the formal charges and bond orders to get a single "resonance-averaged" molecule representation. Importantly, this means that there may be noninteger formal charges and bond orders fed into the network.  

The second-level element `AtomFeatures` includes a list of `AtomFeature` elements, each of which describes a feature used by the model. Each feature includes a descriptive `name` attribute and other attribute-specific properties. The following attributes are supported:

- `"atomic_element"`, which represents the elemental symbol of an atom, containing the `categories` attribute which specifies (in a comma-separated stringified list) the elements supported by the model, in the order in which they are one-hot encoded.
- `"atom_connectivity"`, which represents the number of unique bonds an atom is involved in (not considering bond order), containing the `categories` attribute which specifies (in a comma-separated stringified list) the per-atom bond counts supported by this model and the order in which they are one-hot encoded.
- `"atom_average_formal_charge"`, corresponding to the resonance-averaged formal charge as described above, containing no attributes.
- `"atom_in_ring_of_size"`, which represents the ring membership of an atom, containing the `"ring_size"` attribute.


The tag `BondFeatures` structurally mirrors the `AtomFeatures` section, but describes bond featurization with analogously-named elements.
- (need to talk to Lily for details here)

Below is an example `<NAGLCharges>` section:

```xml
<NAGLCharges weights="elm-v1.1.pt" version="0.3">
    <!-- specify precision? -->
    <!-- feature_size could be included as a check -- should sum to the total shape of feature tensor -->
    <AtomFeatures>
        <!-- could include first_index, last_index as check if these are not ordered -->
        <AtomFeature name="atomic_element" categories="C,O,H,N,S,F,Br,Cl,I,P" />
        <AtomFeature name="atom_connectivity" categories="1,2,3,4,5,6" />
        <AtomFeature name="atom_average_formal_charge" />
        <AtomFeature name="atom_in_ring_of_size" ring_size="3" />
        <AtomFeature name="atom_in_ring_of_size" ring_size="4" />
        <AtomFeature name="atom_in_ring_of_size" ring_size="5" />
        <AtomFeature name="atom_in_ring_of_size" ring_size="6" />
    </AtomFeatures>
    <BondFeatures>
        <BondFeature ... />
    </BondFeatures>
</NAGLCharges>
```

## Alternatives

The first GNN trained with the intent to be shipped in SMIRNOFF force fields is one that models AM1-BCC partial
charges, so another solution could involve updating the existing `<ToolkitAM1BCC>` section instead of adding a new
section altogether. This might involve a new tag in the `<ToolkitAM1BCC>` section that distinguishes a particular GNN
from the existing QuacPac and/or `sqm`-based approach. This approach is limiting, however, since GNNs can be used to
predict other charge models than AM1-BCC; if a GNN was trained to ABCG2 or a RESP variant, it's not obvious if that
could drop in to `<ToolkitAM1BCC>`.

Another similar solution could involve not updating the `ToolkitAM1BCC` specification at all and simply letting
implementations use GNNs in place of QuacPac or `sqm` as currently specified. This in principle produces the same
results, to the extent that the GNN accurately reproduces AM1-BCC charges, but is inconsistent with the philosophy that
the details of a force field must be communicated to users and not hidden from view.

The solution in this proposal makes clear to any person or tool inspecting a force field that GNNs are a different tool
than existing AM1-BCC charge providers. It attempts to provide enough detail that somebody could re-implement the same
GNN provided weights that are shipped alongside a force field. It allows for future modifications in which a different
underlying charge model is targeted.

## Discussion

This section may just be a bullet list including links to any discussions
regarding the proposal:

- This includes links to mailing list threads and / or relevant GitHub issues.

## Copyright

*This template is based upon the [``numpy`` NEP template](
https://github.com/numpy/numpy/blob/master/doc/neps/nep-template.rst) and the
[``conda-forge`` CFEP template.](https://github.com/conda-forge/cfep/blob/master/cfep-00.md)*

*All OFF-EPs are explicitly [CC0 1.0 Universal](https://creativecommons.org/publicdomain/zero/1.0/).*
