# iglsynth 
[![Build Status](https://travis-ci.com/abhibp1993/iglsynth.svg?branch=cpp-devel)](https://travis-ci.com/abhibp1993/iglsynth)
[![Coverage Status](https://codecov.io/gh/abhibp1993/iglsynth/branch/cpp-devel/graph/badge.svg)](https://codecov.io/gh/abhibp1993/iglsynth/branch/devel)

## Testing Steps

1. Place your code appropriately in ``iglsynth-cpp/`` folder.
2. Go to ``iglsynth/cmake-build-debug`` or equivalent cmake-build folder. (If not existing create one.)
3. Run ``cmake ..`` and ``make`` **inside** cmake build folder.
4. Go to ``iglsynth/util/`` folder and run ``python`` or ``python3`` to start python (>= 3.7).
5. Run the following
```python
import iglsynth
print(iglsynth.version())

import iglsynth.util as util
g = util.Graph()
print(g)
```
and any new C++ functions that you have bound to python.
 

