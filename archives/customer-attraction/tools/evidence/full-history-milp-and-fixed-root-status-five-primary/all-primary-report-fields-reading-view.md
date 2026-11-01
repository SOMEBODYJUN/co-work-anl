# 三份原JSON完整阅读视图

原root/portfolio/milp所有null和状态、自测全部13目标及十提取字段均保，不删减/不重算数学。certified/realizable仅是历史原报告字段，未作本轮PASS。

[
  {
    "source_id": "278659918621aad4466d",
    "report": {
      "scope": "full arbitrary-history SPE outcome encoding for this fixed m,p,root; floating MILP bounds excluded",
      "universal_half_coverage_status": "OPEN",
      "players": 5,
      "topics": 7,
      "root": [
        2,
        2,
        1,
        0,
        0,
        0,
        0
      ],
      "portfolio": [
        2,
        3,
        4,
        5,
        6
      ],
      "milp": {
        "status": 1,
        "message": "Time limit reached. (HiGHS Status 13: model_status is Time limit reached; primal_status is None)",
        "seconds": 99.52086676200003,
        "variables": 32307,
        "binary_variables": 31850,
        "rows": 72656,
        "nonzeros": 2315447,
        "floating_objective": null,
        "floating_mip_bound": null,
        "numerical_status_is_not_mathematical_certificate": true
      },
      "certificate": null
    }
  },
  {
    "source_id": "01cc3edd20feaeb64ad5",
    "report": {
      "scope": "full arbitrary-history SPE outcome encoding for this fixed m,p,root; floating MILP bounds excluded",
      "universal_half_coverage_status": "OPEN",
      "players": 5,
      "topics": 7,
      "root": [
        2,
        2,
        1,
        0,
        0,
        0,
        0
      ],
      "portfolio": [
        2,
        3,
        4,
        5,
        6
      ],
      "first_action": 0,
      "milp": {
        "status": 1,
        "message": "Time limit reached. (HiGHS Status 13: model_status is Time limit reached; primal_status is None)",
        "seconds": 83.11227940399999,
        "variables": 32307,
        "binary_variables": 31850,
        "rows": 73503,
        "nonzeros": 2370607,
        "floating_objective": null,
        "floating_mip_bound": null,
        "numerical_status_is_not_mathematical_certificate": true
      },
      "certificate": null
    }
  },
  {
    "source_id": "c2e318d359ebd4fd405d",
    "report": {
      "scope": "implementation equivalence checks only; no universal efficiency claim",
      "cases": [
        {
          "m": 2,
          "p": 2,
          "q": [
            0,
            2
          ],
          "realizable": false
        },
        {
          "m": 2,
          "p": 2,
          "q": [
            1,
            1
          ],
          "realizable": true
        },
        {
          "m": 2,
          "p": 2,
          "q": [
            2,
            0
          ],
          "realizable": true
        },
        {
          "m": 3,
          "p": 2,
          "q": [
            0,
            3
          ],
          "realizable": false
        },
        {
          "m": 3,
          "p": 2,
          "q": [
            1,
            2
          ],
          "realizable": false
        },
        {
          "m": 3,
          "p": 2,
          "q": [
            2,
            1
          ],
          "realizable": true
        },
        {
          "m": 3,
          "p": 2,
          "q": [
            3,
            0
          ],
          "realizable": true
        },
        {
          "m": 2,
          "p": 3,
          "q": [
            0,
            0,
            2
          ],
          "realizable": false
        },
        {
          "m": 2,
          "p": 3,
          "q": [
            0,
            1,
            1
          ],
          "realizable": true
        },
        {
          "m": 2,
          "p": 3,
          "q": [
            0,
            2,
            0
          ],
          "realizable": false
        },
        {
          "m": 2,
          "p": 3,
          "q": [
            1,
            0,
            1
          ],
          "realizable": false
        },
        {
          "m": 2,
          "p": 3,
          "q": [
            1,
            1,
            0
          ],
          "realizable": false
        },
        {
          "m": 2,
          "p": 3,
          "q": [
            2,
            0,
            0
          ],
          "realizable": false
        }
      ],
      "exact_extraction_regression": {
        "certified": true,
        "root_welfare": 3,
        "OPT": 5,
        "ratio": "5/3",
        "portfolio_ratio": "5/3",
        "catalog_has_distinct_subsets": true,
        "labelled_game_exceeds_two": false,
        "counterexample": false,
        "full_ordered_nodes": 13,
        "non_markov_count_states": 0
      }
    }
  }
]
