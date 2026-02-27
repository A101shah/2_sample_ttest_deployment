import streamlit as st
import numpy as np
from statistics import stdev
from scipy import stats
from scipy.stats import t


def two_sample(a, b, alternative):
    xbar1 = np.mean(a)
    xbar2 = np.mean(b)

    sd1 = stdev(a)
    sd2 = stdev(b)

    n1 = len(a)
    n2 = len(b)

    alpha = 0.05
    df = n1 + n2 - 2

    se = np.sqrt((sd1**2)/n1 + (sd2**2)/n2)
    tcal = (xbar1 - xbar2) / se

    if alternative == "two-sided":
        p_value = 2 * (1 - t.cdf(abs(tcal), df))
    elif alternative == "left":
        p_value = t.cdf(tcal, df)
    else:
        p_value = 1 - t.cdf(tcal, df)

    scipy_result = stats.ttest_ind(a, b, alternative=alternative, equal_var=False)

    return tcal, df, p_value, scipy_result


# ---------- Streamlit UI ----------

st.title("Two-Sample t-Test Calculator")

st.write("Enter numbers separated by commas")

sample1_input = st.text_input("Sample 1", "10, 12, 14, 15, 13")
sample2_input = st.text_input("Sample 2", "8, 9, 11, 7, 10")

alternative = st.selectbox(
    "Alternative Hypothesis",
    ["two-sided", "left", "right"]
)

if st.button("Calculate"):
    try:
        a = [float(x.strip()) for x in sample1_input.split(",")]
        b = [float(x.strip()) for x in sample2_input.split(",")]

        tcal, df, p_value, scipy_result = two_sample(a, b, alternative)

        st.subheader("Manual Calculation")
        st.write("t statistic:", tcal)
        st.write("Degrees of freedom:", df)
        st.write("p-value:", p_value)

        st.subheader("Scipy Result")
        st.write(scipy_result)

    except:
        st.error("Please enter valid numbers.")