import numpy as np
from scipy.interpolate import griddata

def interpolate_missing_point(data, mask, method = 'linear'):
    
    # get height and width
    m, n = data.shape[:2]
    xx, yy = np.meshgrid(np.arange(n), np.arange(m))
    
    # get locations of the good data
    known_x = xx[~mask]
    known_y = yy[~mask]
    known_data = data[~mask]
    # get locations of the missing data
    missing_x = xx[mask]
    missing_y = yy[mask]
    
    # interpolate over the good data
    interp_values = griddata(
        (known_x, known_y), known_data, (missing_x, missing_y),
        method=method
    )
    
    # put in the interpolated value where required
    interp_data = data.copy()
    interp_data[missing_y, missing_x] = interp_values

    return interp_data


def compute_okubo_weiss_parameter(v_x, v_y):
    curl = np.gradient(v_y, axis=1) - np.gradient(v_x, axis=0)
    strain_normal = np.gradient(v_x, axis=1) - np.gradient(v_y, axis=0)
    strain_shear = np.gradient(v_y, axis=1) + np.gradient(v_x, axis=0)
    
    return strain_normal**2 + strain_shear**2 - curl**2
