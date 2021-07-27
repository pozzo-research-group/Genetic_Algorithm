import warnings
try:
	from .datareps import UVVis
	from .metrics import func_norm
except ImportError as error:
	warnings.warn("scikit-fda installation is not found thus its applications will be excluded")
		
from .designspace import Euclidean, Hyperplane
from .policies import thompson_sampling
from .utils import get_spectrum, ExampleRunnerSimulation, ExampleRunner
from .metrics import euclidean_dist