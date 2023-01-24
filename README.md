# Thicket

A Python-based toolkit for analyzing ensemble performance data.

### Installation

If you want to develop with this repo directly, run the install script from the
root directory, which will build the package and add the cloned directory to
your `PYTHONPATH`:

```
$ source install.sh
```

#### Build Requirements

<!-- The contents of this section will be collapsed by default -->
<details>
<summary>Click to expand and see our full list of dependencies</summary>

| Name          | Version Range | Required? | Package Name                                                       |
| :---:         | :---:         | :---:     | :---:                                                              |
| Hatchet       |               | Yes       | [llnl-hatchet](https://pypi.org/project/llnl-hatchet/)             |
| pandas        | >= 1.1        | Yes       | [pandas](https://pypi.org/project/pandas/)                         |
| SciPy         | Not Specified | Yes       | [scipy](https://pypi.org/project/scipy/)                           |
| NumPy         | Not Specified | Yes       | [numpy](https://pypi.org/project/numpy/)                           |
| seaborn       | Not Specified | Yes       | [seaborn](https://pypi.org/project/seaborn/)                       |
| matplotlib    | Not Specified | Yes       | [matplotlib](https://pypi.org/project/matplotlib/)                 |
| pydot         | Not Specified | Yes       | [pydot](https://pypi.org/project/pydot/)                           |
| Extra-P       | Not Specified | No        | [extrap](https://pypi.org/project/extrap/)                         |
| Node.js       | Not Specified | Yes       | [Node.js](https://nodejs.org)                                      |
| Webpack       | ^4.10.0       | Yes       | [webpack-cli](https://www.npmjs.com/package/webpack-cli)           |
| Redux Toolkit | ^1.8.3        | Yes       | [@reduxjs/toolkit](https://www.npmjs.com/package/@reduxjs/toolkit) |
| D3            | ^7.6.1        | Yes       | [d3](https://www.npmjs.com/package/d3)                             |
| Redux         | ^4.2.0        | Yes       | [redux](https://www.npmjs.com/package/redux)                       |
| Vega-Embed    | ^6.21.0       | Yes       | [vega-embed](https://www.npmjs.com/package/vega-embed)             |
| Vega-Lite     | ^5.6.0        | Yes       | [vega-lite](https://www.npmjs.com/package/vega-lite)               |

*Note: __Not Specified__ means that thicket does not specify a version range for a particular
dependency. As a result, the actual version range is dictated by the dependencies themselves. For example,
if thicket is built with pandas 1.1, the pandas dependency will enforce a specific version range on the
SciPy, NumPy, and matplotlib dependencies.*

</details>

### Contributing

Thicket is an open-source project. We welcome contributions via pull requests,
and questions, feature requests, or bug reports via issues.

### License

Thicket is distributed under the terms of the MIT license.

All contributions must be made under the MIT license. Copyrights in the
Thicket project are retained by contributors. No copyright assignment is
required to contribute to Thicket.

See [LICENSE](https://github.com/llnl/thicket/blob/develop/LICENSE) and
[NOTICE](https://github.com/llnl/thicket/blob/develop/NOTICE) for details.

SPDX-License-Identifier: MIT

LLNL-CODE-834749
