import pandas as pd
import numpy as np
from IPython.display import display
import hatchet as ht
import logging

import thicket as th

pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)

logging.basicConfig(filename="thicket.log", level=logging.DEBUG)


clang = "./data/quartz/clang14.0.6_BaseSeq_8388608/"
gcc = "./data/quartz/GCC_10.3.1_BaseSeq_08388608/O3"

# create thickets for each dataset originating from clang and gcc compilers
clang_th = th.Thicket.from_caliperreader(clang)
gcc_th = th.Thicket.from_caliperreader(gcc)

combined_th = th.Thicket.concat_thickets(
    axis="columns",
    thickets=[clang_th, gcc_th],
    headers=["Clang", "GCC"]
)
display(combined_th.dataframe.head(5))

# define metrics to calculate the maximum on
metrics = ["time (exc)", "Machine clears"]

th.stats.maximum(clang_th, columns=metrics)
# view the first 5 entries of the aggregated statistics table
display(clang_th.statsframe.dataframe.head(5))

metrics = [("Clang", "time (exc)"), ("GCC", "Machine clears")]

th.stats.maximum(combined_th, columns=metrics)
display(combined_th.statsframe.dataframe.head(5))

metrics = ["time (exc)", "Machine clears"]

th.stats.minimum(clang_th, columns=metrics)
display(clang_th.statsframe.dataframe.head(5))

metrics = [("Clang", "time (exc)"), ("GCC", "Machine clears")]

th.stats.minimum(combined_th, columns=metrics)
display(combined_th.statsframe.dataframe.head(5))

metrics = ["time (exc)", "Machine clears"]

th.stats.median(clang_th, columns=metrics)
display(clang_th.statsframe.dataframe.head(5))

metrics = ["time (exc)", "Machine clears"]

th.stats.mean(clang_th, columns=metrics)
display(clang_th.statsframe.dataframe.head(5))

metrics = [("Clang", "time (exc)"), ("GCC", "Machine clears")]

th.stats.mean(combined_th, columns=metrics)
display(combined_th.statsframe.dataframe.head(5))

metrics = ["time (exc)", "Machine clears"]

th.stats.variance(clang_th, columns=metrics)
display(clang_th.statsframe.dataframe.head(5))

metrics = [("Clang", "time (exc)"), ("GCC", "Machine clears")]

th.stats.variance(combined_th, columns=metrics)
display(combined_th.statsframe.dataframe.head(5))

metrics = ["time (exc)", "Machine clears"]

th.stats.std(clang_th, columns=metrics)
display(clang_th.statsframe.dataframe.head(5))

metrics = [("Clang", "time (exc)"), ("GCC", "Machine clears")]

th.stats.std(combined_th, columns=metrics)
display(combined_th.statsframe.dataframe.head(5))

metrics = ["time (exc)", "Machine clears"]

th.stats.percentiles(clang_th, columns=metrics)
display(clang_th.statsframe.dataframe.head(5))

metrics = [("Clang", "time (exc)"), ("GCC", "Machine clears")]

th.stats.percentiles(combined_th, columns=metrics)
display(combined_th.statsframe.dataframe.head(5))
