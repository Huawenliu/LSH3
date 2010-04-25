from scipy import weave
from scipy.weave import converters

def sparse_jaccard(x0, x1):
	#return 1 - len(x0 & x1) / float(len(x0 | x1))
	return 1 - len(set(x0.indices) & set(x1.indices)) / float((x0 + x1).getnnz())

def quick_jaccard(x0, x1):
	"""This sadly does not work."""
	l = x0.shape[0]
	code = """
	double num, denom;
	num = 0.0;
	denom = 0.0;
	for (int i = 0; i < l; ++i) {
		if (x0[i] == x1[i]) {
			num += 1.0;
		}
		printf(x0[i]);
		if (x0[i] > 0.0 || x1[i] > 0.0) {
			denom += 1.0;
		}
		return_val = num / denom;
	}
	"""
	distance = weave.inline(code, 
							['l', 'x0', 'x1'],
							type_converters=converters.blitz,
							compiler = 'gcc')
	return 1 - distance

