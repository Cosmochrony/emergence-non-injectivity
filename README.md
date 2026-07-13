This repository contains the source of the  
Cosmochrony paper on projection-induced fluctuations and λ-dependent fibre dynamics.

This work provides a **structural derivation of apparent stochasticity**
in effective descriptions arising from a non-injective projection

$\Pi : \chi \to O$

by identifying fluctuations as the observable consequence of a
$\lambda$-dependent projection mechanism.

The key refinement is that the projection must be understood as a
**family of maps**

$\Pi_\lambda$,

where $\lambda$ is the relaxation-ordering parameter whose projection defines
operational time.

We show that:

- non-injectivity alone produces multiplicity but **not randomness**,
- the **irreversible advance of $\lambda$** induces a drift of the fibres,
- successive projections sample **different slices of co-projecting configurations**,
- the resulting residual differences are registered as **fluctuations**.

Fluctuations are therefore not intrinsic indeterminacy, but the
**effective signature of time evolution itself**.

## Conceptual Overview

The argument proceeds in three logical steps:

1. **Non-injectivity and fibre structure**  
   The projection $\Pi$ is non-injective, so each observable $o \in O$
   corresponds to a fibre $\Pi^{-1}(o)$ of indistinguishable substrate configurations.
   This multiplicity alone does not produce variability: identical reprojections
   would yield identical residuals.

2. **$\lambda$-dependent projection (dynamical lifting of Π)**  
   The projection must be understood as implicitly $\lambda$-dependent,
   defining an effective family $\Pi_\lambda$.
   At each step $U_n$, the system probes a slice of the fibre determined by
   the current value of the relaxation-ordering parameter $\lambda$.
   Since $\lambda$ advances monotonically, the co-projecting set is not
   identical between successive steps.

3. **Fluctuations as fibre drift**  
   Successive projections sample different slices of an evolving fibre.
   The residual differences between these slices appear as fluctuations
   in the effective description.
   If $\lambda$ could be held fixed, the same residuals would repeat:
   stochasticity is therefore not fundamental, but induced by
   the impossibility of projecting at fixed $\lambda$.

## Core Claims

The paper establishes the following statements:

1. **Non-injectivity does not imply randomness**  
   Fibre multiplicity alone produces degeneracy, not fluctuations.

2. **The projection is effectively $\lambda$-parametrized**  
   The observable map must be understood as a family $\Pi_\lambda$,
   reflecting the relaxation ordering of the substrate.

3. **Fluctuations arise from fibre drift**  
   The apparent randomness corresponds to differences between
   $\lambda$-indexed slices of the same co-projecting set.

4. **Time is the source of effective noise**  
   Operational time $\tau$ is the projected image of $\lambda$-ordering;
   fluctuations are therefore the observable imprint of time evolution.

5. **No intrinsic indeterminacy is required**  
   The framework explains stochasticity without introducing
   probabilistic postulates at the fundamental level.

## What This Paper Does Not Assume

To maintain structural clarity, the paper does not assume:

- intrinsic randomness in the substrate $\chi$,
- probabilistic dynamics at the fundamental level,
- hidden variables or stochastic evolution laws,
- any modification of the projection framework,
- any external noise source.

The analysis is entirely based on projection structure and relaxation ordering.

## Repository Contents
```
paper/
├── pdf/ # Compiled paper PDF
├── tex/ # LaTeX sources
└── README.md
```

## Citation

If you reference this work, please cite:

> J. Beau, *Non-Injectivity as a Structural Necessity of Genuine Emergence*, 2026.

## Acknowledgements

Portions of the editorial refinement benefited from iterative interactions with
large language models.
These tools were used as analytical assistants for exploring alternative
formulations, checking internal consistency, and improving clarity.
All claims, interpretations, and final formulations remain the sole
responsibility of the author.

## Contributions

This repository is intended as a research reference.

Critical feedback, independent analyses, and formal scrutiny are welcome.
Please open an issue to discuss conceptual points, projection structure,
fibre dynamics, or alternative interpretations.
