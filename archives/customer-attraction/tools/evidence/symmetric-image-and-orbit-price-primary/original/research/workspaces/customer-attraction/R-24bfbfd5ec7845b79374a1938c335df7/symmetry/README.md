# Symmetry and fractional prices

Personal mathematical backup; general Q-CAG-HALF remains OPEN.

- `balanced_partition_price_certificate.md`: exact version BPC-v2, with
  no symmetry assumption. Cellwise maximum mass for one actual provider
  and an overlap bound imply C(z)<=(tau+m-1)u_i for every real query; if
  that provider has minimum utility, OPT_m<=(2-1/m)W follows without SPE.
- `orbit_overlap_price_certificate.md`: exact unrestricted fractional
  query certificate under a transitive-catalog orbit overlap condition;
  every minority-group provider satisfies it in a distinct two-block
  profile. It proves B(u_i)<=(m-1)u_i, with no SPE assumption for that
  principal lemma.
- `automorphic_image_cover.md`: the parent's two-image coverage mechanism,
  with explicit repeated-action support threshold. In the fully symmetric
  two-block class, OPT_d<=2W always, and OPT_m<=2W whenever actual distinct
  support d>=min(k,m).
- `non_spe_price_boundary.md`: a 504-unit-customer symmetric all-distinct
  profile with B(min u)>=392>W=378. It is not SPE; it separates the
  stronger price bridge from the deterministic image coverage bound.

Next steps: independent reconstruction of the orbit theorem; identify
whether repeated-support cases admit a genuine sequential argument. The
present two-block results do not extend automatically to arbitrary menus.
