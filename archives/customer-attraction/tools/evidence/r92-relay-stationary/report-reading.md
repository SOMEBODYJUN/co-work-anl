# 三份冻结报告的全部字段

原字节也逐份保存。以下仅将完整解码结果重排，未执行原程序。

## 03af380226e5ba437d88

```json
{
  "status": 0,
  "message": "Optimization terminated successfully. (HiGHS Status 7: Optimal)",
  "objective": -0.125,
  "fixed_selector_objective": -0.125,
  "exact_valid": true,
  "stationary_defect": "-1/4",
  "weights": {
    "3": 1,
    "12": 1
  },
  "terminal_actions": {
    "(0, 0)": 2,
    "(0, 1)": 2,
    "(0, 2)": 2,
    "(0, 3)": 3,
    "(1, 0)": 3,
    "(1, 1)": 2,
    "(1, 2)": 2,
    "(1, 3)": 3,
    "(2, 0)": 3,
    "(2, 1)": 2,
    "(2, 2)": 0,
    "(2, 3)": 0,
    "(3, 0)": 1,
    "(3, 1)": 2,
    "(3, 2)": 1,
    "(3, 3)": 1
  }
}
```

## a6e6412f08cd56667290

```json
{
  "status": "passed",
  "grid_cases": 354,
  "samples": [
    {
      "r": 3,
      "b": 0,
      "loss": "1/8",
      "a": 1,
      "t": 1
    },
    {
      "r": 3,
      "b": 1,
      "loss": "1/24",
      "a": 1,
      "t": 1
    },
    {
      "r": 3,
      "b": 1000,
      "loss": "1/4012008",
      "a": 1,
      "t": 1
    },
    {
      "r": 4,
      "b": 0,
      "loss": "1/9",
      "a": 2,
      "t": 1
    },
    {
      "r": 4,
      "b": 1,
      "loss": "1/24",
      "a": 1,
      "t": 1
    },
    {
      "r": 4,
      "b": 1000,
      "loss": "1/3012009",
      "a": 1,
      "t": 1
    },
    {
      "r": 5,
      "b": 0,
      "loss": "1/9",
      "a": 2,
      "t": 1
    },
    {
      "r": 5,
      "b": 1,
      "loss": "1/24",
      "a": 2,
      "t": 1
    },
    {
      "r": 5,
      "b": 1000,
      "loss": "3/8040032",
      "a": 1,
      "t": 1
    },
    {
      "r": 10,
      "b": 0,
      "loss": "2/27",
      "a": 5,
      "t": 1
    },
    {
      "r": 10,
      "b": 1,
      "loss": "2/63",
      "a": 4,
      "t": 1
    },
    {
      "r": 10,
      "b": 1000,
      "loss": "1/1513521",
      "a": 3,
      "t": 2
    },
    {
      "r": 60,
      "b": 0,
      "loss": "29/1829",
      "a": 30,
      "t": 1
    },
    {
      "r": 60,
      "b": 1,
      "loss": "81/8024",
      "a": 27,
      "t": 3
    },
    {
      "r": 60,
      "b": 1000,
      "loss": "9/2503193",
      "a": 15,
      "t": 15
    }
  ]
}
```

## 80fd349243c9ff02560d

```json
{
  "status": "passed",
  "seed": 9221,
  "scope": "r=2..41, b=0,1,3,19; exact rational checks only",
  "checks": {
    "pair_checks": 88560,
    "mixture_checks": 800,
    "partial_checks": 800,
    "derivative_checks": 42640,
    "sharp_multiplicative": 160
  }
}
```
