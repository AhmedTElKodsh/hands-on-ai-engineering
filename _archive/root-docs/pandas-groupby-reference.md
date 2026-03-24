# Pandas GroupBy Quick Reference Guide

## 🎯 The Split-Apply-Combine Pattern

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│   SPLIT     │ →   │   APPLY      │ →   │  COMBINE    │
│ Partition   │     │ Function to  │     │ Collect     │
│ data into   │     │ each group   │     │ results     │
│ groups      │     │ independently│     │             │
└─────────────┘     └──────────────┘     └─────────────┘
```

**Three Operation Types:**

| Type | Returns | Use When |
|------|---------|----------|
| **Aggregation** | One row per group | Computing summary statistics |
| **Transformation** | Same size as input | Group-wise calculations keeping original shape |
| **Filtration** | Subset of original | Removing entire groups based on criteria |

---

## 📚 Table of Contents

1. [Creating GroupBy Objects](#creating-groupby-objects)
2. [Aggregation Operations](#aggregation-operations)
3. [Transformation Operations](#transformation-operations)
4. [Filtration Operations](#filtration-operations)
5. [Apply Method](#apply-method)
6. [Common Parameters](#common-parameters)
7. [GroupBy Object Methods & Attributes](#groupby-object-methods--attributes)
8. [Common Patterns](#common-patterns)
9. [Decision Tree](#decision-tree-which-operation-to-use)

---

## Creating GroupBy Objects

### Basic Grouping

```python
# Single column
grouped = df.groupby("column_name")

# Multiple columns
grouped = df.groupby(["col1", "col2"])

# Group and select columns immediately
grouped = df.groupby("A")[["C", "D"]]
```

### Advanced Grouping

```python
# Group by index level
grouped = df.groupby(level=0)
grouped = df.groupby(level="level_name")

# Group by function (applied to index)
grouped = df.groupby(lambda x: x.year)

# Group by array/Series/dict
grouped = df.groupby(mapping_array)
grouped = df.groupby(mapping_series)
```

---

## Aggregation Operations

**Purpose:** Reduce each group to summary statistics (one row per group)

### Built-in Aggregation Methods

| Method | Description | Example |
|--------|-------------|---------|
| `sum()` | Sum of values | `grouped.sum()` |
| `mean()` | Arithmetic mean | `grouped.mean()` |
| `median()` | Median value | `grouped.median()` |
| `min()` | Minimum value | `grouped.min()` |
| `max()` | Maximum value | `grouped.max()` |
| `count()` | Count non-NA values | `grouped.count()` |
| `size()` | Count all values (incl. NA) | `grouped.size()` |
| `first()` | First occurring value | `grouped.first()` |
| `last()` | Last occurring value | `grouped.last()` |
| `std()` | Standard deviation | `grouped.std()` |
| `var()` | Variance | `grouped.var()` |
| `prod()` | Product of values | `grouped.prod()` |
| `nunique()` | Count unique values | `grouped.nunique()` |
| `sem()` | Standard error of mean | `grouped.sem()` |
| `skew()` | Skewness | `grouped.skew()` |
| `quantile(q)` | Value at given quantile | `grouped.quantile(0.75)` |
| `cov()` | Covariance | `grouped.cov()` |
| `corr()` | Correlation | `grouped.corr()` |
| `any()` | Any values truthy | `grouped.any()` |
| `all()` | All values truthy | `grouped.all()` |
| `idxmax()` | Index of max value | `grouped.idxmax()` |
| `idxmin()` | Index of min value | `grouped.idxmin()` |

### The `agg()` / `aggregate()` Method

```python
# Single function (string alias)
grouped.agg("sum")
grouped.aggregate("mean")

# Multiple functions on one column
grouped["C"].agg(["sum", "mean", "std"])

# Multiple functions on multiple columns
grouped[["C", "D"]].agg(["sum", "mean", "std"])

# Different functions per column
grouped.agg({
    "C": "sum",
    "D": "std"
})

# Custom functions
grouped["C"].agg(lambda x: x.max() - x.min())
grouped["C"].agg(lambda x: set(x))

# Named aggregation (DataFrame output with custom column names)
animals.groupby("kind").agg(
    min_height=("height", "min"),
    max_height=("height", "max"),
    average_weight=("weight", "mean")
)

# Rename with tuples
grouped["C"].agg([
    ("foo", "sum"),
    ("bar", "mean"),
    ("baz", "std")
])
```

### Examples

```python
# Single aggregation
df.groupby("A")[["C", "D"]].max()

# Multiple grouping keys
df.groupby(["A", "B"]).mean()

# Describe all groups (multiple stats)
grouped.describe()

# Unique values count
df4.groupby("A")["B"].nunique()
```

---

## Transformation Operations

**Purpose:** Return result with same index/shape as input

### Built-in Transformation Methods

| Method | Description | Example |
|--------|-------------|---------|
| `cumsum()` | Cumulative sum | `grouped.cumsum()` |
| `cummin()` | Cumulative minimum | `grouped.cummin()` |
| `cummax()` | Cumulative maximum | `grouped.cummax()` |
| `cumprod()` | Cumulative product | `grouped.cumprod()` |
| `cumcount()` | Cumulative count (0-indexed) | `grouped.cumcount()` |
| `shift()` | Shift values up/down | `grouped.shift(1)` |
| `diff()` | Difference from previous | `grouped.diff()` |
| `pct_change()` | Percent change | `grouped.pct_change()` |
| `rank()` | Rank within group | `grouped.rank()` |
| `bfill()` | Backward fill NA | `grouped.bfill()` |
| `ffill()` | Forward fill NA | `grouped.ffill()` |

### The `transform()` Method

```python
# Built-in transformation
grouped.transform("cumsum")

# Built-in aggregation broadcast to group size
grouped.transform("sum")  # Returns same size as input

# Standardize data (z-score) within each group
ts.groupby(lambda x: x.year).transform(
    lambda x: (x - x.mean()) / x.std()
)

# More efficient using built-ins
(ts - grouped.transform("mean")) / grouped.transform("std")

# Fill missing data with group mean
data_df.fillna(grouped.transform("mean"))

# Custom transformation
grouped.transform(lambda x: x - x.mean())
```

### Window Operations on Groups

```python
# Rolling window within groups
df.groupby("A").rolling(4).B.mean()

# Expanding window within groups
df.groupby("A").expanding().sum()

# Resample within groups
df.groupby("group").resample("1D").ffill()
```

### Examples

```python
# Add group mean as new column (same length as original)
df["group_mean"] = df.groupby("category")["sales"].transform("mean")

# Cumulative sum within each group
df["cumsum"] = grouped.cumsum()

# Difference from group mean
df["diff_from_mean"] = df["value"] - grouped.transform("mean")

# Rank within group
df["rank"] = grouped.rank()
```

---

## Filtration Operations

**Purpose:** Discard entire groups based on group-level criteria

### Built-in Filtration Methods

| Method | Description | Example |
|--------|-------------|---------|
| `head(n)` | First n rows of each group | `grouped.head(1)` |
| `tail(n)` | Last n rows of each group | `grouped.tail(1)` |
| `nth(n)` | nth row(s) of each group | `grouped.nth(0)` |

### The `filter()` Method

```python
# Filter groups with sum > 2
sf.groupby(sf).filter(lambda x: x.sum() > 2)

# Filter groups with more than 2 members
dff.groupby("B").filter(lambda x: len(x) > 2)

# Keep groups but fill non-matching with NaN
dff.groupby("B").filter(lambda x: len(x) > 2, dropna=False)

# Filter with column specification
dff.groupby("B").filter(lambda x: len(x["C"]) > 2)

# Keep groups where mean exceeds threshold
df.groupby("category").filter(lambda x: x["sales"].mean() > 1000)
```

### Complex Filtration with Boolean Indexing

```python
# Select largest products capturing ≤90% of total volume
product_volumes = product_volumes.sort_values("volume", ascending=False)
grouped = product_volumes.groupby("group")["volume"]
cumpct = grouped.cumsum() / grouped.transform("sum")
significant_products = product_volumes[cumpct <= 0.9]
```

### Nth Row Selection

```python
# Single nth row
g.nth(0)      # First row
g.nth(-1)     # Last row
g.nth(1)      # Second row

# With dropna
g.nth(0, dropna="any")

# Multiple rows
g.nth([0, 3, -1])

# Slices
g.nth[1:]
g.nth[1:, :-1]
```

---

## Apply Method

**Purpose:** Apply arbitrary function to each group (most flexible)

```python
# Apply custom function
grouped.apply(lambda x: x.describe())

# Apply function with arguments
grouped.apply(custom_func, arg1, arg2)

# Apply returning different shapes
# Can return scalar, Series, DataFrame, or list
```

**Note:** `apply()` is more flexible but slower than `agg()` or `transform()`. Use specific methods when possible.

---

## Common Parameters

| Parameter | Default | Description | Example |
|-----------|---------|-------------|---------|
| `sort` | `True` | Sort group keys in output | `df.groupby("X", sort=False).sum()` |
| `as_index` | `True` | Use group keys as index | `df.groupby("kind", as_index=False).sum()` |
| `dropna` | `True` | Exclude NA from group keys | `df.groupby("b", dropna=False).sum()` |
| `observed` | `False` | Show only observed categorical values | `groupby(cat, observed=True)` |
| `group_keys` | `True` | Include group keys in apply output | `df.groupby("A", group_keys=False).apply(f)` |
| `numeric_only` | `False` | Exclude non-numeric columns | `df.groupby("A").std(numeric_only=True)` |

### Parameter Examples

```python
# sort=False preserves order of appearance
df2.groupby(["X"], sort=False).sum()

# as_index=False includes group keys as columns
animals.groupby("kind", as_index=False).sum()

# dropna=False includes NA in group keys
df_dropna.groupby(by=["b"], dropna=False).sum()

# observed=True shows only observed categorical values
series.groupby(categorical, observed=True).count()
```

---

## GroupBy Object Methods & Attributes

### Attributes

| Attribute | Description |
|-----------|-------------|
| `.groups` | Dict mapping group keys to index labels |
| `.indices` | Dict mapping group keys to index positions |
| `.ngroups` | Number of groups |
| `.name` | Name of the GroupBy object |

```python
df.groupby("A").groups  # {'bar': [1, 3, 5], 'foo': [0, 2, 4, 6, 7]}
len(grouped)            # Number of groups
```

### Key Methods

| Method | Description |
|--------|-------------|
| `get_group(name)` | Select single group by name |
| `apply(func)` | Apply arbitrary function |
| `agg()/aggregate()` | Aggregate with function(s) |
| `transform(func)` | Transform with function |
| `filter(func)` | Filter groups |

### Iteration

```python
# Iterate through groups
for name, group in df.groupby('A'):
    print(name)
    print(group)

# Multiple keys (tuple names)
for name, group in df.groupby(['A', 'B']):
    print(name)  # ('bar', 'one')
```

### Column Selection

```python
# Select columns after groupby
grouped = df.groupby(["A"])
grouped_C = grouped["C"]
grouped_D = grouped["D"]

# Multiple columns
grouped[["A", "B"]].sum()
```

### Enumeration

```python
# Row order within group (0-indexed)
dfg.groupby("A").cumcount()

# Group order (integer encoding)
dfg.groupby("A").ngroup()

# Multi-column factorization
dfg.groupby(["A", "B"]).ngroup()
```

---

## Common Patterns

### 1. Standardize Data Within Groups
```python
grouped = ts.groupby(lambda x: x.year)
result = (ts - grouped.transform("mean")) / grouped.transform("std")
```

### 2. Fill Missing Data with Group Mean
```python
result = data_df.fillna(grouped.transform("mean"))
```

### 3. Compute Multiple Metrics
```python
grouped["C"].agg(["sum", "mean", "std"])
```

### 4. Named Aggregation for Clear Output
```python
animals.groupby("kind").agg(
    min_height=("height", "min"),
    max_height=("height", "max"),
    average_weight=("weight", "mean")
)
```

### 5. Filter by Group Size
```python
dff.groupby("B").filter(lambda x: len(x) > 2)
```

### 6. Cumulative Operations Within Groups
```python
grouped.cumsum()
grouped.cumcount()
```

### 7. First/Last N Rows Per Group
```python
g.head(1)   # First row
g.tail(1)   # Last row
```

### 8. Multi-Column Factorization
```python
dfg.groupby(["A", "B"]).ngroup()  # Integer encoding
```

### 9. GroupBy with Time Grouper
```python
df.groupby([pd.Grouper(freq="1ME", key="Date"), "Buyer"])[["Quantity"]].sum()
```

### 10. Piping for Readable Chains
```python
(df.groupby(["Store", "Product"])
 .pipe(lambda grp: grp.Revenue.sum() / grp.Quantity.sum())
 .unstack()
 .round(2))
```

### 11. Apply Different Functions Per Column
```python
grouped.agg({
    "C": "sum",
    "D": lambda x: np.std(x, ddof=1)
})
```

### 12. Add Group Results Back to Original DataFrame
```python
result = speeds.copy()
result["cumsum"] = grouped.cumsum()
result["diff"] = grouped.diff()
```

### 13. Group Percentage of Total
```python
grouped = df.groupby("category")["sales"]
df["pct_of_total"] = grouped.transform(lambda x: x / x.sum())
```

### 14. Rank Within Groups
```python
df["rank_in_group"] = df.groupby("category")["sales"].rank(ascending=False)
```

### 15. Count Unique Values Per Group
```python
df.groupby("category")["product"].nunique()
```

---

## Decision Tree: Which Operation to Use?

```
Start: What do you want to do?
│
├─→ Compute summary statistics per group?
│   └─→ Use AGGREGATION (sum, mean, count, agg())
│
├─→ Keep original DataFrame shape but add group calculations?
│   └─→ Use TRANSFORMATION (transform, cumsum, shift, rank)
│
├─→ Remove entire groups based on criteria?
│   └─→ Use FILTRATION (filter, head, tail, nth)
│
└─→ Need custom logic that doesn't fit above?
    └─→ Use APPLY (most flexible, but slower)
```

### Quick Reference Table

| Operation | Method | Returns | Example Use Case |
|-----------|--------|---------|------------------|
| **Aggregation** | `sum()`, `mean()`, `agg()` | Reduced (one row per group) | Total sales per category |
| **Transformation** | `cumsum()`, `transform()` | Same size as input | Add group mean column |
| **Filtration** | `filter()`, `head()`, `nth()` | Subset of input | Keep groups with >10 rows |
| **Apply** | `apply()` | Flexible (any shape) | Custom group operations |

---

## Troubleshooting Tips

### Common Errors

**Error:** "Cannot use name aggregation with SeriesGroupBy"
- **Fix:** Use `agg()` on DataFrame, not Series

**Error:** "transform must return a scalar value for each group"
- **Fix:** Ensure transform function returns same-sized result

**Error:** "filter function returned wrong shape"
- **Fix:** Filter function must return single boolean value

### Performance Tips

1. Use built-in methods (`sum`, `mean`) over `apply()` when possible
2. Use `transform("sum")` instead of `transform(lambda x: x.sum())`
3. Set `sort=False` if you don't need sorted output
4. Use `numeric_only=True` for numeric operations on mixed DataFrames

---

## Quick Syntax Cheat Sheet

```python
# Create GroupBy object
grouped = df.groupby("column")
grouped = df.groupby(["col1", "col2"])

# Aggregation
grouped.sum()
grouped.mean()
grouped.agg(["sum", "mean"])
grouped.agg({"col1": "sum", "col2": "mean"})

# Transformation
grouped.cumsum()
grouped.transform("sum")
grouped.transform(lambda x: (x - x.mean()) / x.std())

# Filtration
grouped.filter(lambda x: len(x) > 5)
grouped.head(1)
grouped.nth(0)

# Apply
grouped.apply(custom_function)

# Access attributes
grouped.groups
grouped.ngroups

# Iterate
for name, group in grouped:
    print(name, group)
```

---

**References:**
- [Official pandas GroupBy Documentation](https://pandas.pydata.org/docs/user_guide/groupby.html)
- *Python for Data Analysis*, Wes McKinney (O'Reilly)
- Wickham, H. (2011). The Split-Apply-Combine Strategy for Data Analysis
