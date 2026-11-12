# 每个闭窗口的完整几何

24个域、96个不可约facet、110次顶点出现。各域由全部真实状态定义；独立真边裁切已逐域PASS。

| cell | dimension | raw states | raw constraints | primitive groups | facets | vertices | lambda layers |
|---|---:|---:|---:|---:|---:|---:|---|
| I3_Q6_L0_9 | 3 | 24 | 28 | 25 | 5 | 5 | 5/3:1, 9:4 |
| I3_Q6_L9_16 | 3 | 24 | 28 | 24 | 8 | 11 | 9:4, 15:3, 16:4 |
| I3_Q6_L16_25 | 3 | 24 | 28 | 24 | 8 | 12 | 16:4, 773/48:3, 111527/6912:1, 25:4 |
| I3_Q5_L0_9 | 3 | 24 | 28 | 25 | 5 | 5 | 2:1, 9:4 |
| I3_Q5_L9_16 | 3 | 24 | 28 | 24 | 8 | 11 | 9:4, 15:3, 16:4 |
| I3_Q5_L16_25 | 3 | 24 | 28 | 24 | 8 | 12 | 16:4, 129/8:3, 3103/192:1, 25:4 |
| I4_Q6_L0_4 | 2 | 16 | 19 | 15 | 3 | 3 | 5/3:1, 4:2 |
| I4_Q6_L4_9 | 2 | 16 | 19 | 14 | 4 | 4 | 4:2, 9:2 |
| I4_Q6_L9_16 | 2 | 16 | 19 | 14 | 5 | 5 | 9:2, 15:1, 16:2 |
| I4_Q6_L16_25 | 2 | 16 | 19 | 14 | 5 | 5 | 16:2, 773/48:1, 25:2 |
| I4_Q5_L0_4 | 2 | 16 | 19 | 15 | 3 | 3 | 2:1, 4:2 |
| I4_Q5_L4_9 | 2 | 16 | 19 | 14 | 4 | 4 | 4:2, 9:2 |
| I4_Q5_L9_16 | 2 | 16 | 19 | 14 | 5 | 5 | 9:2, 15:1, 16:2 |
| I4_Q5_L16_25 | 2 | 16 | 19 | 14 | 5 | 5 | 16:2, 129/8:1, 25:2 |
| I5_Q6_L0_1 | 1 | 10 | 12 | 7 | 2 | 2 | 0:1, 1:1 |
| I5_Q6_L1_4 | 1 | 10 | 12 | 6 | 2 | 2 | 1:1, 4:1 |
| I5_Q6_L4_9 | 1 | 10 | 12 | 6 | 2 | 2 | 4:1, 9:1 |
| I5_Q6_L9_16 | 1 | 10 | 12 | 6 | 2 | 2 | 9:1, 16:1 |
| I5_Q6_L16_25 | 1 | 10 | 12 | 6 | 2 | 2 | 16:1, 25:1 |
| I5_Q5_L0_1 | 1 | 10 | 12 | 7 | 2 | 2 | 0:1, 1:1 |
| I5_Q5_L1_4 | 1 | 10 | 12 | 6 | 2 | 2 | 1:1, 4:1 |
| I5_Q5_L4_9 | 1 | 10 | 12 | 6 | 2 | 2 | 4:1, 9:1 |
| I5_Q5_L9_16 | 1 | 10 | 12 | 6 | 2 | 2 | 9:1, 16:1 |
| I5_Q5_L16_25 | 1 | 10 | 12 | 6 | 2 | 2 | 16:1, 25:1 |

## I3_Q6_L0_9

严格内点：`(1166/6075, 44/225, 113/15)`。坐标：`(tau4, tau5, lambda)`。

| facet id | exact primitive inequality | support vertices | affine rank | raw source ids |
|---|---|---:|---:|---|
| I3_Q6_L0_9_H001 | − 15 − 135 tau4 − 5 tau5 + 9 lambda ≥ 0 | 3 | 2 | I3_Q6_L0_9_P2_R010 |
| I3_Q6_L0_9_H004 | − 5 − 45 tau5 + 3 lambda ≥ 0 | 3 | 2 | I3_Q6_L0_9_P2_R100 |
| I3_Q6_L0_9_H011 | tau5 ≥ 0 | 3 | 2 | I3_Q6_L0_9_TAU5_NONNEG |
| I3_Q6_L0_9_H012 | tau4 ≥ 0 | 3 | 2 | I3_Q6_L0_9_TAU4_NONNEG |
| I3_Q6_L0_9_H015 | 9 − lambda ≥ 0 | 4 | 2 | I3_Q6_L0_9_P0_R111, I3_Q6_L0_9_WINDOW_HIGH |

## I3_Q6_L9_16

严格内点：`(1802/4455, 68/165, 145/11)`。坐标：`(tau4, tau5, lambda)`。

| facet id | exact primitive inequality | support vertices | affine rank | raw source ids |
|---|---|---:|---:|---|
| I3_Q6_L9_16_H003 | − 15 − 135 tau4 − 5 tau5 + 9 lambda ≥ 0 | 4 | 2 | I3_Q6_L9_16_P2_R010 |
| I3_Q6_L9_16_H006 | − 9 + lambda ≥ 0 | 4 | 2 | I3_Q6_L9_16_P0_R110, I3_Q6_L9_16_WINDOW_LOW |
| I3_Q6_L9_16_H009 | − 5 − 45 tau5 + 3 lambda ≥ 0 | 4 | 2 | I3_Q6_L9_16_P2_R100 |
| I3_Q6_L9_16_H014 | tau5 ≥ 0 | 5 | 2 | I3_Q6_L9_16_TAU5_NONNEG |
| I3_Q6_L9_16_H015 | tau4 ≥ 0 | 5 | 2 | I3_Q6_L9_16_TAU4_NONNEG |
| I3_Q6_L9_16_H016 | 8 − 9 tau5 ≥ 0 | 4 | 2 | I3_Q6_L9_16_P1_R101 |
| I3_Q6_L9_16_H017 | 16 − lambda ≥ 0 | 4 | 2 | I3_Q6_L9_16_P1_R111, I3_Q6_L9_16_WINDOW_HIGH |
| I3_Q6_L9_16_H019 | 24 − 27 tau4 − tau5 ≥ 0 | 4 | 2 | I3_Q6_L9_16_P1_R011 |

## I3_Q6_L16_25

严格内点：`(190625/373248, 901/1728, 1579031/82944)`。坐标：`(tau4, tau5, lambda)`。

| facet id | exact primitive inequality | support vertices | affine rank | raw source ids |
|---|---|---:|---:|---|
| I3_Q6_L16_25_H007 | − 24 − 135 tau4 − 5 tau5 + 9 lambda ≥ 0 | 5 | 2 | I3_Q6_L16_25_P1_R011 |
| I3_Q6_L16_25_H008 | − 16 + lambda ≥ 0 | 4 | 2 | I3_Q6_L16_25_P1_R110, I3_Q6_L16_25_WINDOW_LOW |
| I3_Q6_L16_25_H013 | − 8 − 45 tau5 + 3 lambda ≥ 0 | 4 | 2 | I3_Q6_L16_25_P1_R101 |
| I3_Q6_L16_25_H018 | tau5 ≥ 0 | 5 | 2 | I3_Q6_L16_25_TAU5_NONNEG |
| I3_Q6_L16_25_H019 | tau4 ≥ 0 | 5 | 2 | I3_Q6_L16_25_TAU4_NONNEG |
| I3_Q6_L16_25_H020 | 25 − lambda ≥ 0 | 4 | 2 | I3_Q6_L16_25_P2_R111, I3_Q6_L16_25_WINDOW_HIGH |
| I3_Q6_L16_25_H021 | 43 − 48 tau5 ≥ 0 | 5 | 2 | I3_Q6_L16_25_P2_R101 |
| I3_Q6_L16_25_H023 | 129 − 144 tau4 − 5 tau5 ≥ 0 | 4 | 2 | I3_Q6_L16_25_P2_R011 |

## I3_Q5_L0_9

严格内点：`(616/3375, 14/75, 38/5)`。坐标：`(tau4, tau5, lambda)`。

| facet id | exact primitive inequality | support vertices | affine rank | raw source ids |
|---|---|---:|---:|---|
| I3_Q5_L0_9_H001 | − 6 − 45 tau4 − 2 tau5 + 3 lambda ≥ 0 | 3 | 2 | I3_Q5_L0_9_P2_R010 |
| I3_Q5_L0_9_H008 | − 2 − 15 tau5 + lambda ≥ 0 | 3 | 2 | I3_Q5_L0_9_P2_R100 |
| I3_Q5_L0_9_H011 | tau5 ≥ 0 | 3 | 2 | I3_Q5_L0_9_TAU5_NONNEG |
| I3_Q5_L0_9_H012 | tau4 ≥ 0 | 3 | 2 | I3_Q5_L0_9_TAU4_NONNEG |
| I3_Q5_L0_9_H015 | 9 − lambda ≥ 0 | 4 | 2 | I3_Q5_L0_9_P0_R111, I3_Q5_L0_9_WINDOW_HIGH |

## I3_Q5_L9_16

严格内点：`(88/225, 2/5, 145/11)`。坐标：`(tau4, tau5, lambda)`。

| facet id | exact primitive inequality | support vertices | affine rank | raw source ids |
|---|---|---:|---:|---|
| I3_Q5_L9_16_H007 | − 9 + lambda ≥ 0 | 4 | 2 | I3_Q5_L9_16_P0_R110, I3_Q5_L9_16_WINDOW_LOW |
| I3_Q5_L9_16_H008 | − 6 − 45 tau4 − 2 tau5 + 3 lambda ≥ 0 | 4 | 2 | I3_Q5_L9_16_P2_R010 |
| I3_Q5_L9_16_H012 | − 2 − 15 tau5 + lambda ≥ 0 | 4 | 2 | I3_Q5_L9_16_P2_R100 |
| I3_Q5_L9_16_H014 | tau5 ≥ 0 | 5 | 2 | I3_Q5_L9_16_TAU5_NONNEG |
| I3_Q5_L9_16_H015 | tau4 ≥ 0 | 5 | 2 | I3_Q5_L9_16_TAU4_NONNEG |
| I3_Q5_L9_16_H017 | 13 − 15 tau5 ≥ 0 | 4 | 2 | I3_Q5_L9_16_P1_R101 |
| I3_Q5_L9_16_H018 | 16 − lambda ≥ 0 | 4 | 2 | I3_Q5_L9_16_P1_R111, I3_Q5_L9_16_WINDOW_HIGH |
| I3_Q5_L9_16_H023 | 39 − 45 tau4 − 2 tau5 ≥ 0 | 4 | 2 | I3_Q5_L9_16_P1_R011 |

## I3_Q5_L16_25

严格内点：`(128693/259200, 733/1440, 43879/2304)`。坐标：`(tau4, tau5, lambda)`。

| facet id | exact primitive inequality | support vertices | affine rank | raw source ids |
|---|---|---:|---:|---|
| I3_Q5_L16_25_H007 | − 16 + lambda ≥ 0 | 4 | 2 | I3_Q5_L16_25_P1_R110, I3_Q5_L16_25_WINDOW_LOW |
| I3_Q5_L16_25_H011 | − 9 − 45 tau4 − 2 tau5 + 3 lambda ≥ 0 | 5 | 2 | I3_Q5_L16_25_P1_R011 |
| I3_Q5_L16_25_H015 | − 3 − 15 tau5 + lambda ≥ 0 | 4 | 2 | I3_Q5_L16_25_P1_R101 |
| I3_Q5_L16_25_H018 | tau5 ≥ 0 | 5 | 2 | I3_Q5_L16_25_TAU5_NONNEG |
| I3_Q5_L16_25_H019 | tau4 ≥ 0 | 5 | 2 | I3_Q5_L16_25_TAU4_NONNEG |
| I3_Q5_L16_25_H020 | 7 − 8 tau5 ≥ 0 | 5 | 2 | I3_Q5_L16_25_P2_R101 |
| I3_Q5_L16_25_H021 | 21 − 24 tau4 − tau5 ≥ 0 | 4 | 2 | I3_Q5_L16_25_P2_R011 |
| I3_Q5_L16_25_H022 | 25 − lambda ≥ 0 | 4 | 2 | I3_Q5_L16_25_P2_R111, I3_Q5_L16_25_WINDOW_HIGH |

## I4_Q6_L0_4

严格内点：`(7/135, 29/9)`。坐标：`(tau5, lambda)`。

| facet id | exact primitive inequality | support vertices | affine rank | raw source ids |
|---|---|---:|---:|---|
| I4_Q6_L0_4_H000 | − 5 − 45 tau5 + 3 lambda ≥ 0 | 2 | 1 | I4_Q6_L0_4_P3_R00 |
| I4_Q6_L0_4_H006 | tau5 ≥ 0 | 2 | 1 | I4_Q6_L0_4_TAU5_NONNEG |
| I4_Q6_L0_4_H007 | 4 − lambda ≥ 0 | 2 | 1 | I4_Q6_L0_4_P0_R11, I4_Q6_L0_4_WINDOW_HIGH |

## I4_Q6_L4_9

严格内点：`(29/180, 13/2)`。坐标：`(tau5, lambda)`。

| facet id | exact primitive inequality | support vertices | affine rank | raw source ids |
|---|---|---:|---:|---|
| I4_Q6_L4_9_H001 | − 5 − 45 tau5 + 3 lambda ≥ 0 | 2 | 1 | I4_Q6_L4_9_P3_R00 |
| I4_Q6_L4_9_H002 | − 4 + lambda ≥ 0 | 2 | 1 | I4_Q6_L4_9_P0_R10, I4_Q6_L4_9_WINDOW_LOW |
| I4_Q6_L4_9_H007 | tau5 ≥ 0 | 2 | 1 | I4_Q6_L4_9_TAU5_NONNEG |
| I4_Q6_L4_9_H010 | 9 − lambda ≥ 0 | 2 | 1 | I4_Q6_L4_9_P1_R11, I4_Q6_L4_9_WINDOW_HIGH |

## I4_Q6_L9_16

严格内点：`(34/75, 13)`。坐标：`(tau5, lambda)`。

| facet id | exact primitive inequality | support vertices | affine rank | raw source ids |
|---|---|---:|---:|---|
| I4_Q6_L9_16_H001 | − 9 + lambda ≥ 0 | 2 | 1 | I4_Q6_L9_16_P1_R10, I4_Q6_L9_16_WINDOW_LOW |
| I4_Q6_L9_16_H003 | − 5 − 45 tau5 + 3 lambda ≥ 0 | 2 | 1 | I4_Q6_L9_16_P3_R00 |
| I4_Q6_L9_16_H009 | tau5 ≥ 0 | 2 | 1 | I4_Q6_L9_16_TAU5_NONNEG |
| I4_Q6_L9_16_H010 | 8 − 9 tau5 ≥ 0 | 2 | 1 | I4_Q6_L9_16_P2_R01 |
| I4_Q6_L9_16_H011 | 16 − lambda ≥ 0 | 2 | 1 | I4_Q6_L9_16_P2_R11, I4_Q6_L9_16_WINDOW_HIGH |

## I4_Q6_L16_25

严格内点：`(193/360, 4709/240)`。坐标：`(tau5, lambda)`。

| facet id | exact primitive inequality | support vertices | affine rank | raw source ids |
|---|---|---:|---:|---|
| I4_Q6_L16_25_H001 | − 16 + lambda ≥ 0 | 2 | 1 | I4_Q6_L16_25_P2_R10, I4_Q6_L16_25_WINDOW_LOW |
| I4_Q6_L16_25_H005 | − 8 − 45 tau5 + 3 lambda ≥ 0 | 2 | 1 | I4_Q6_L16_25_P2_R01 |
| I4_Q6_L16_25_H011 | tau5 ≥ 0 | 2 | 1 | I4_Q6_L16_25_TAU5_NONNEG |
| I4_Q6_L16_25_H012 | 25 − lambda ≥ 0 | 2 | 1 | I4_Q6_L16_25_P3_R11, I4_Q6_L16_25_WINDOW_HIGH |
| I4_Q6_L16_25_H013 | 43 − 48 tau5 ≥ 0 | 2 | 1 | I4_Q6_L16_25_P3_R01 |

## I4_Q5_L0_4

严格内点：`(2/45, 10/3)`。坐标：`(tau5, lambda)`。

| facet id | exact primitive inequality | support vertices | affine rank | raw source ids |
|---|---|---:|---:|---|
| I4_Q5_L0_4_H002 | − 2 − 15 tau5 + lambda ≥ 0 | 2 | 1 | I4_Q5_L0_4_P3_R00 |
| I4_Q5_L0_4_H006 | tau5 ≥ 0 | 2 | 1 | I4_Q5_L0_4_TAU5_NONNEG |
| I4_Q5_L0_4_H008 | 4 − lambda ≥ 0 | 2 | 1 | I4_Q5_L0_4_P0_R11, I4_Q5_L0_4_WINDOW_HIGH |

## I4_Q5_L4_9

严格内点：`(3/20, 13/2)`。坐标：`(tau5, lambda)`。

| facet id | exact primitive inequality | support vertices | affine rank | raw source ids |
|---|---|---:|---:|---|
| I4_Q5_L4_9_H003 | − 4 + lambda ≥ 0 | 2 | 1 | I4_Q5_L4_9_P0_R10, I4_Q5_L4_9_WINDOW_LOW |
| I4_Q5_L4_9_H005 | − 2 − 15 tau5 + lambda ≥ 0 | 2 | 1 | I4_Q5_L4_9_P3_R00 |
| I4_Q5_L4_9_H007 | tau5 ≥ 0 | 2 | 1 | I4_Q5_L4_9_TAU5_NONNEG |
| I4_Q5_L4_9_H009 | 9 − lambda ≥ 0 | 2 | 1 | I4_Q5_L4_9_P1_R11, I4_Q5_L4_9_WINDOW_HIGH |

## I4_Q5_L9_16

严格内点：`(11/25, 13)`。坐标：`(tau5, lambda)`。

| facet id | exact primitive inequality | support vertices | affine rank | raw source ids |
|---|---|---:|---:|---|
| I4_Q5_L9_16_H003 | − 9 + lambda ≥ 0 | 2 | 1 | I4_Q5_L9_16_P1_R10, I4_Q5_L9_16_WINDOW_LOW |
| I4_Q5_L9_16_H007 | − 2 − 15 tau5 + lambda ≥ 0 | 2 | 1 | I4_Q5_L9_16_P3_R00 |
| I4_Q5_L9_16_H009 | tau5 ≥ 0 | 2 | 1 | I4_Q5_L9_16_TAU5_NONNEG |
| I4_Q5_L9_16_H011 | 13 − 15 tau5 ≥ 0 | 2 | 1 | I4_Q5_L9_16_P2_R01 |
| I4_Q5_L9_16_H012 | 16 − lambda ≥ 0 | 2 | 1 | I4_Q5_L9_16_P2_R11, I4_Q5_L9_16_WINDOW_HIGH |

## I4_Q5_L16_25

严格内点：`(157/300, 157/8)`。坐标：`(tau5, lambda)`。

| facet id | exact primitive inequality | support vertices | affine rank | raw source ids |
|---|---|---:|---:|---|
| I4_Q5_L16_25_H003 | − 16 + lambda ≥ 0 | 2 | 1 | I4_Q5_L16_25_P2_R10, I4_Q5_L16_25_WINDOW_LOW |
| I4_Q5_L16_25_H008 | − 3 − 15 tau5 + lambda ≥ 0 | 2 | 1 | I4_Q5_L16_25_P2_R01 |
| I4_Q5_L16_25_H011 | tau5 ≥ 0 | 2 | 1 | I4_Q5_L16_25_TAU5_NONNEG |
| I4_Q5_L16_25_H012 | 7 − 8 tau5 ≥ 0 | 2 | 1 | I4_Q5_L16_25_P3_R01 |
| I4_Q5_L16_25_H013 | 25 − lambda ≥ 0 | 2 | 1 | I4_Q5_L16_25_P3_R11, I4_Q5_L16_25_WINDOW_HIGH |

## I5_Q6_L0_1

严格内点：`(1/2)`。坐标：`(lambda)`。

| facet id | exact primitive inequality | support vertices | affine rank | raw source ids |
|---|---|---:|---:|---|
| I5_Q6_L0_1_H001 | lambda ≥ 0 | 1 | 0 | I5_Q6_L0_1_WINDOW_LOW |
| I5_Q6_L0_1_H002 | 1 − lambda ≥ 0 | 1 | 0 | I5_Q6_L0_1_P0_R1, I5_Q6_L0_1_WINDOW_HIGH |

## I5_Q6_L1_4

严格内点：`(5/2)`。坐标：`(lambda)`。

| facet id | exact primitive inequality | support vertices | affine rank | raw source ids |
|---|---|---:|---:|---|
| I5_Q6_L1_4_H000 | − 1 + lambda ≥ 0 | 1 | 0 | I5_Q6_L1_4_P0_R0, I5_Q6_L1_4_WINDOW_LOW |
| I5_Q6_L1_4_H002 | 4 − lambda ≥ 0 | 1 | 0 | I5_Q6_L1_4_P1_R1, I5_Q6_L1_4_WINDOW_HIGH |

## I5_Q6_L4_9

严格内点：`(13/2)`。坐标：`(lambda)`。

| facet id | exact primitive inequality | support vertices | affine rank | raw source ids |
|---|---|---:|---:|---|
| I5_Q6_L4_9_H000 | − 4 + lambda ≥ 0 | 1 | 0 | I5_Q6_L4_9_P1_R0, I5_Q6_L4_9_WINDOW_LOW |
| I5_Q6_L4_9_H003 | 9 − lambda ≥ 0 | 1 | 0 | I5_Q6_L4_9_P2_R1, I5_Q6_L4_9_WINDOW_HIGH |

## I5_Q6_L9_16

严格内点：`(25/2)`。坐标：`(lambda)`。

| facet id | exact primitive inequality | support vertices | affine rank | raw source ids |
|---|---|---:|---:|---|
| I5_Q6_L9_16_H000 | − 9 + lambda ≥ 0 | 1 | 0 | I5_Q6_L9_16_P2_R0, I5_Q6_L9_16_WINDOW_LOW |
| I5_Q6_L9_16_H004 | 16 − lambda ≥ 0 | 1 | 0 | I5_Q6_L9_16_P3_R1, I5_Q6_L9_16_WINDOW_HIGH |

## I5_Q6_L16_25

严格内点：`(41/2)`。坐标：`(lambda)`。

| facet id | exact primitive inequality | support vertices | affine rank | raw source ids |
|---|---|---:|---:|---|
| I5_Q6_L16_25_H000 | − 16 + lambda ≥ 0 | 1 | 0 | I5_Q6_L16_25_P3_R0, I5_Q6_L16_25_WINDOW_LOW |
| I5_Q6_L16_25_H005 | 25 − lambda ≥ 0 | 1 | 0 | I5_Q6_L16_25_P4_R1, I5_Q6_L16_25_WINDOW_HIGH |

## I5_Q5_L0_1

严格内点：`(1/2)`。坐标：`(lambda)`。

| facet id | exact primitive inequality | support vertices | affine rank | raw source ids |
|---|---|---:|---:|---|
| I5_Q5_L0_1_H001 | lambda ≥ 0 | 1 | 0 | I5_Q5_L0_1_WINDOW_LOW |
| I5_Q5_L0_1_H002 | 1 − lambda ≥ 0 | 1 | 0 | I5_Q5_L0_1_P0_R1, I5_Q5_L0_1_WINDOW_HIGH |

## I5_Q5_L1_4

严格内点：`(5/2)`。坐标：`(lambda)`。

| facet id | exact primitive inequality | support vertices | affine rank | raw source ids |
|---|---|---:|---:|---|
| I5_Q5_L1_4_H000 | − 1 + lambda ≥ 0 | 1 | 0 | I5_Q5_L1_4_P0_R0, I5_Q5_L1_4_WINDOW_LOW |
| I5_Q5_L1_4_H002 | 4 − lambda ≥ 0 | 1 | 0 | I5_Q5_L1_4_P1_R1, I5_Q5_L1_4_WINDOW_HIGH |

## I5_Q5_L4_9

严格内点：`(13/2)`。坐标：`(lambda)`。

| facet id | exact primitive inequality | support vertices | affine rank | raw source ids |
|---|---|---:|---:|---|
| I5_Q5_L4_9_H000 | − 4 + lambda ≥ 0 | 1 | 0 | I5_Q5_L4_9_P1_R0, I5_Q5_L4_9_WINDOW_LOW |
| I5_Q5_L4_9_H003 | 9 − lambda ≥ 0 | 1 | 0 | I5_Q5_L4_9_P2_R1, I5_Q5_L4_9_WINDOW_HIGH |

## I5_Q5_L9_16

严格内点：`(25/2)`。坐标：`(lambda)`。

| facet id | exact primitive inequality | support vertices | affine rank | raw source ids |
|---|---|---:|---:|---|
| I5_Q5_L9_16_H000 | − 9 + lambda ≥ 0 | 1 | 0 | I5_Q5_L9_16_P2_R0, I5_Q5_L9_16_WINDOW_LOW |
| I5_Q5_L9_16_H004 | 16 − lambda ≥ 0 | 1 | 0 | I5_Q5_L9_16_P3_R1, I5_Q5_L9_16_WINDOW_HIGH |

## I5_Q5_L16_25

严格内点：`(41/2)`。坐标：`(lambda)`。

| facet id | exact primitive inequality | support vertices | affine rank | raw source ids |
|---|---|---:|---:|---|
| I5_Q5_L16_25_H000 | − 16 + lambda ≥ 0 | 1 | 0 | I5_Q5_L16_25_P3_R0, I5_Q5_L16_25_WINDOW_LOW |
| I5_Q5_L16_25_H005 | 25 − lambda ≥ 0 | 1 | 0 | I5_Q5_L16_25_P4_R1, I5_Q5_L16_25_WINDOW_HIGH |
