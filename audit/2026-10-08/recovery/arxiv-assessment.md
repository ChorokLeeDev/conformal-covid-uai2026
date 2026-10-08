# Existing arXiv version and material correction

The official page and source for [arXiv:2601.00908v2](https://arxiv.org/abs/2601.00908v2) were fetched successfully on 2026-10-08. The page records v2 on 2026-08-27 and the UAI/PMLR publication. URLs, response sizes and SHA-256 values are in `arxiv/retrieval.json`; the official source tarball and HTML are preserved locally in this audit directory.

Its `main.tex` is byte-identical to this repository's original commit `96d9616961e5ae8607373181d35262cb21a2b0d1:paper/main.tex`, SHA-256 `8b7456b576cbcb5631345f761fff384d86c7e67b3e59b7915b8ffc95e65f7fbe`. Its bibliography is also byte-identical, SHA-256 `828ddfa60391b30216203b9a70950ad7987e022e0ee0f713c8a823170d8a3a97`.

A material update is warranted: the revised theorem, incompatible historical APS conventions, unvalidated ICC/class-count inference, failed positive-association replication on the recovered full follow-up panel, demonstrated date-truncated join artifact on the pinned snapshot, and withdrawn hyperparameter/deployment claims change scientific interpretation. An update should explicitly distinguish the historical 50-seed results (not reconstructed) from the newly reproduced 24-model follow-up and disclose that the private source archive is not a public replication package.

The separate revised PDF is `../revision/uai-statistical-audit-revision.pdf`. No arXiv submission, withdrawal, version replacement, or publisher communication has been performed by this audit. Original publication artifacts remain unchanged.
