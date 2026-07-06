# Call Path Query Language

The **Call Path Query Language** is a programmatic tool designed to identify performance bottlenecks by extracting specific paths from complex, hierarchical profiling data. By leveraging pattern matching, you can reduce massive calling context trees into meaningful subsets for focused analysis.

## Overview

A query is defined as a sequence of one or more **query nodes**. Each query node consists of two primary components:

*   **Quantifier**: Specifies how many real nodes in a call path must match the query node.
    *   `.`: Match exactly one node.
    *   `*`: Match zero or more nodes.
    *   `+`: Match one or more nodes.
    *   **Integer**: Match exactly that specific number of nodes.
*   **Predicate**: Defines the logical conditions (such as function names or performance metrics) that a node must satisfy to be considered a match.

After writing a query, you can apply it to a `Thicket` object using the `query` method (applies to the performance data) or the `query_stats` method (applies to the StatsFrame). These methods will search the performance data or StatsFrame and find _all_ paths in their graphs that satisfy the entire query.

## Query Dialects

Thicket supports three distinct dialects to accommodate different programming environments and complexity needs.

### 1. Base Syntax
The core implementation utilizes the `Query` class (historically accessed via `QueryMatcher`). Predicates are represented as Python **callables** (such as lambdas) that take the DataFrame rows for a given node in the graph as input and return a Boolean. This dialect offers the most flexibility but is the most verbose.

### 2. Object Dialect

This dialect uses Python's built-in data structures—**lists, tuples, and dictionaries**—to define queries. Predicates are key-value pairs within a dictionary, where the key is a metric name and the value is a comparison expression. Multiple predicates in a single dictionary are combined using **conjunction (AND)**.

### 3. String Dialect

Inspired by the **Cypher** graph query language, this dialect allows users to write queries as formal strings. It utilizes `MATCH` statements to define the path structure and `WHERE` statements for Boolean predicates. This dialect is particularly useful for transferring queries between different tools, such as from a JavaScript-based visualization back to a Python notebook.

## Thicket-Specific Features

Thicket extends the query language to support the multi-dimensional nature of performance ensembles.

### Multi-Index Support
When analyzing data across multiple MPI ranks and threads, Thicket uses **MultiIndexed DataFrames**. Both the object and string dialects support a `multi_index_mode` argument to determine how predicates apply to multiple rows associated with a single node:
*   **"off"**: Default; assumes no MultiIndex.
*   **"all"**: Every row associated with the node must satisfy the predicate.
*   **"any"**: At least one row associated with the node must satisfy the predicate.

Additionally, the dialects support **MultiIndex columns**, allowing queries to target metrics nested under specific column levels using tuples (e.g., `('CPU', 'time')`).

<!--
### Performance Optimization
For GraphFrames using a row MultiIndex, the query engine utilizes `pandas.DataFrame.xs` internally for data access, providing a significant speedup during query execution.
-->

## Advanced Syntax

### Leaf Node Matching
Special syntax is available to identify **leaf nodes** (functions that call no other functions):
*   **Object Dialect**: Use the predicate `{"depth": -1}`.
*   **String Dialect**: Use the explicit `p IS LEAF` condition.

### Compound Queries
Users can construct complex queries using logical operators like **AND**, **OR**, and **XOR**. Queries in any dialect can be combined using the `ConjunctionQuery` (**AND**), `DisjunctionQuery` (**OR**), and `ExclusiveDisjunctionQuery` (**XOR**) classes. The string dialect also provides a shorthand for these compound queries. In this shorthand, individual queries are wrapped in curly braces and literal operator names (e.g., "AND", "OR", "XOR") are used to link them together.

## Usage Examples

### Example 1: Filtering MPI Calls
Extract all paths starting with an MPI function that has more than 5 L2 cache misses, followed by any number of subsequent calls.

:::{tab-set}
:::{tab-item} Base Syntax
```python
from thicket.query import Query
import re

def _mpi_cache_miss_predicate(row) -> bool:
    is_mpi = re.fullmatch("P?MPI_.*", row["name"]) is not None
    ge_5_cache_misses = row["PAPI_L2_TCM"] > 5
    return is_mpi and ge_5_cache_misses

# Match MPI calls with high cache misses
query = (
    Query()
    .match(".", _mpi_cache_miss_predicate)
    .rel("*")
)
# Apply to a Thicket object
filtered_thicket = t_obj.query_stats(query)
```
:::
:::{tab-item} Object Dialect
```python
# Match MPI calls with high cache misses
query = [
    (".", {"name": "P?MPI_.*", "PAPI_L2_TCM": "> 5"}), 
    "*"
]
# Apply to a Thicket object
filtered_thicket = t_obj.query_stats(query)
```
:::
:::{tab-item} String Dialect
```python
# Match MPI calls with high cache misses
query = """
MATCH (p)->("*")
WHERE p."name" =~ "P?MPI_.*" AND p."PAPI_L2_TCM" > 5
"""
# Apply to a Thicket object
filtered_thicket = t_obj.query_stats(query)
```
:::
:::

### Example 2: Finding Specific Leaf Nodes
Identify paths that end in a leaf node with a name ending in `.block_128`.

:::{tab-set}
:::{tab-item} Base Syntax
```python
from thicket.query import Query
import re

def _match_block_128_leaf(row) -> bool:
    is_leaf = len(row.name.children) == 0
    is_block_128 = re.match(".*\.block_128", row["name"]) is not None
    return is_leaf and is_block_128

query = (
    Query()
    .match("*")
    .rel(".", _match_block_128_leaf)
)
filtered_thicket = t_obj.query_stats(query)
```
:::
:::{tab-item} Object Dialect 
```python
query = [
    "*",
    (".", {"depth": -1, "name": ".*\.block_128"}),
]
filtered_thicket = t_obj.query_stats(query)
```
:::
:::{tab-item} String Dialect
```python
# String dialect query for specific leaf nodes
query = """
MATCH ("*")->(".", l) 
WHERE l IS LEAF AND l."name" =~ ".*\.block_128"
"""
filtered_thicket = t_obj.query_stats(query)
```
:::
:::

### Example 3: Compound Query (String Dialect)
Combine multiple path matches to find nodes named "leaf_a" or "leaf_b" while excluding paths containing "inner_a".

:::{tab-set}
:::{tab-item} Base Syntax 
```python
from thicket.query import ConjunctionQuery, Query

query1 = (
    Query()
    .match("*")
    .rel(".", lambda row: row["name"] == "leaf_a")
)
query2 = (
    Query()
    .match(".", lambda row: row["name"] != "inner_a")
)

query = ConjunctionQuery(query1, query2)
filtered_thicket = t_obj.query_stats(query)
```
:::
:::{tab-item} Object Dialect
```python
from thicket.query import ConjunctionQuery

query1 = [
    "*",
    (".", {"name": "leaf_a"})
]
# The Object dialect does not provide a built-in way to apply a NOT operator
# to a predicate. To work around this here, we use negative lookahead from
# the Python re module.
query2 = [
    (".", "name": "^(?!inner_a)$")
]

query = ConjunctionQuery(query1, query2)
filtered_thicket = t_obj.query_stats(query)
```
:::
:::{tab-item} String Dialect (Class-Based)
```python
from thicket.query import ConjunctionQuery

query1 = """
MATCH ("*")->(".", l) WHERE l."name" = "leaf_a"
"""
query2 = """
MATCH (".", p) WHERE NOT p."name" = "inner_a"
"""

query = ConjunctionQuery(query1, query2)
filtered_thicket = t_obj.query_stats(query)
```
:::
:::{tab-item} String Dialect (Built-In)
```python
query = """
{ MATCH ("*")->(".", l) WHERE l."name" = "leaf_a" }
AND
{ MATCH (".", p) WHERE NOT p."name" = "inner_a" }
"""
filtered_thicket = t_obj.query_stats(query)
```
:::
:::

### Example 4: Disjunction Predicate Query

TBA

### Example 5: Multi-Index Thicket Query
Query a Thicket object where **any** rank for a specific node has a "time" value greater than 10.

:::{tab-set}
:::{tab-item} Base Syntax
```python
from thicket.query import Query

def _time_predicate(rows_for_node) -> bool:
    # Check if the "time" column is greater than 10 for each
    # row in 'rows_for_node'
    time_gt_10_series = rows_for_node["time"] > 10
    # Use pandas's `Series.any` method to check if any row has
    # a "time" value greater than 10
    return time_gt_10_series.any()

query = (
    Query()
    .match(".", _time_predicate)
)
# Note that `multi_index_mode` is not used here.
# That parameter only applies to the Object and String Dialects.
# When using the base syntax, logic for aggregating across rows
# should be baked into the predicate
filtered_thicket = t_obj.query(query)
```
:::
:::{tab-item} Object Dialect
```python
# Object dialect with MultiIndex mode
query = [(".", {"time": "> 10"})]
# In this call, `multi_index_mode="any"` tells Thicket to aggregate
# the rows for each node using the `Series.any` method
filtered_thicket = t_obj.query(query, multi_index_mode="any")
```
:::
:::{tab-item} String Dialect
```python
query = """
MATCH (".", p)
WHERE p."time" > 10
"""
# In this call, `multi_index_mode="any"` tells Thicket to aggregate
# the rows for each node using the `Series.any` method
filtered_thicket = t_obj.query(query, multi_index_mode="any")
```
:::
:::
