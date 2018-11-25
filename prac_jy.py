# %%
import numpy as np
x = np.arange(10)

# %%
import matplotlib.pyplot as plt
plt.plot(x, x**2, lw=2, ls="--", marker="o", label="sample")
plt.legend(loc="best")
plt.show()

# %%
