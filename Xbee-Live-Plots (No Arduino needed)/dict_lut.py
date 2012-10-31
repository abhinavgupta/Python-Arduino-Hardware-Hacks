from bisect import bisect_right

Temperature = [15.0,15.1,15.2,15.3,15.4,15.5,15.6,15.7,15.8,15.9,16.0,16.1,16.2,16.3,16.4,16.5,16.6,16.7,16.8,16.9,17.0,17.1,17.2,17.3,17.4,17.5,17.6,17.7,17.8,17.9,18.0,18.1,18.2,18.3,18.4,18.5,18.6,18.7,18.8,18.9,19.0,19.1,19.2,19.3,19.4,19.5,19.6,19.7,19.8,19.9,20.0,20.1,20.2,20.3,20.4,20.5,20.6,20.7,20.8,20.9,21.0,21.1,21.2,21.3,21.4,21.5,21.6,21.7,21.8,21.9,22.0,22.1,22.2,22.3,22.4,22.5,22.6,22.7,22.8,22.9,23.0,23.1,23.2,23.3,23.4,23.5,23.6,23.7,23.8,23.9,24.0,24.1,24.2,24.3,24.4,24.5,24.6,24.7,24.8,24.9,25,25.1,25.2,25.3,25.4,25.5,25.6,25.7,25.8,25.9,26,26.1,26.2,26.3,26.4,26.5,26.6,26.7,26.8,26.9,27,27.1,27.2,27.3,27.4,27.5,27.6,27.7,27.8,27.9,28,28.1,28.2,28.3,28.4,28.5,28.6,28.7,28.8,28.9,29,29.1,29.2,29.3,29.4,29.5,29.6,29.7,29.8,29.9,30,30.1,30.2,30.3,30.4,30.5,30.6,30.7,30.8,30.9,31,31.1,31.2,31.3,31.4,31.5,31.6,31.7,31.8,31.9,32,32.1,32.2,32.3,32.4,32.5,32.6,32.7,32.8,32.9,33,33.1,33.2,33.3,33.4,33.5,33.6,33.7,33.8,33.9,34,34.1,34.2,34.3,34.4,34.5,34.6,34.7,34.8,34.9,35,35.1,35.2,35.3,35.4,35.5,35.6,35.7,35.8,35.9,36,36.1,36.2,36.3,36.4,36.5,36.6,36.7,36.8,36.9,37,37.1,37.2,37.3,37.4,37.5,37.6,37.7,37.8,37.9,38,38.1,38.2,38.3,38.4,38.5,38.6,38.7,38.8,38.9,39,39.1,39.2,39.3,39.4,39.5,39.6,39.7,39.8,39.9,40]
Resistance = [3.539,3.523,3.506,3.490,3.474,3.458,3.442,3.426,3.410,3.394,3.379,3.363,3.348,3.332,3.317,3.301,3.286,3.271,3.256,3.241,3.226,3.212,3.197,3.182,1.168,3.153,3.139,3.124,3.110,3.096,3.082,3.068,3.054,3.040,3.026,3.012,2.998,2.985,2.971,2.958,2.944,2.931,2.918,2.905,2.891,2.878,2.865,2.852,2.840,2.827,2.814,2.801,2.789,2.776,2.764,2.751,2.739,2.727,2.714,2.702,2.690,2.678,2.666,2.654,2.642,2.630,2.619,2.607,2.595,2.584,2.572,2.561,2.549,2.538,2.527,2.516,2.504,2.493,2.482,2.471,2.460,2.449,2.439,2.428,2.417,2.406,2.396,2.385,2.375,2.364,2.354,2.344,2.333,2.323,2.313,2.303,2.293,2.283,2.273,2.263,2.253,2.243,2.233,2.223,2.214,2.204,2.194,2.185,2.175,2.166,2.156,2.147,2.138,2.128,2.119,2.110,2.101,2.092,2.083,2.074,2.065,2.056,2.047,2.038,2.029,2.020,2.012,2.003,1.994,1.986,1.977,1.969,1.960,1.952,1.944,1.935,1.927,1.919,1.910,1.902,1.894,1.886,1.878,1.870,1.862,1.854,1.846,1.838,1.831,1.823,1.815,1.807,1.800,1.792,1.784,1.777,1.769,1.762,1.754,1.747,1.740,1.732,1.725,1.718,1.710,1.703,1.696,1.689,1.682,1.675,1.668,1.661,1.654,1.647,1.640,1.633,1.626,1.619,1.613,1.606,1.599,1.592,1.586,1.579,1.573,1.566,1.560,1.553,1.547,1.540,1.534,1.527,1.521,1.515,1.508,1.502,1.496,1.490,1.484,1.478,1.471,1.465,1.459,1.453,1.447,1.441,1.435,1.430,1.424,1.418,1.412,1.406,1.400,1.395,1.389,1.383,1.378,1.372,1.366,1.361,1.355,1.350,1.344,1.339,1.333,1.328,1.322,1.317,1.312,1.306,1.301,1.296,1.291,1.285,1.280,1.275,1.270,1.265,1.260,1.254,1.249,1.244,1.239,1.234,1.229,1.224,1.219,1.215,1.210,1.205,1.200]


data = dict(zip(Resistance, Temperature))

def closest_match(query):
	keys = sorted(data)
	binary_search = bisect_right(keys,query)
	value = data[min(map(abs, (keys[binary_search-1],keys[binary_search])))]
	
	return value
