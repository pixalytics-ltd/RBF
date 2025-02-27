'''
This module contains functions for building two and three-dimensional weight
matrices for linear elasticity problems.
'''
from rbf.pde.fd import weight_matrix

def elastic2d_body_force(x, p, n, lamb=1.0, mu=1.0, **kwargs):
    '''
    Returns weight matrices that map displacements at `p` to the body force at
    `x` in a two-dimensional (plane strain) homogeneous elastic medium

    Parameters
    ----------
    x : (N, 2) array
        Target points.

    p : (M, 2) array
        Observation points.

    n : int
        stencil size

    lamb, mu : float, optional
        Lame parameters

    **kwargs :
        additional arguments passed to `weight_matrix`

    Returns
    -------
    dict
        keys are the components and the values are the corresponding weight
        matrices.

    '''
    # x component of force resulting from displacement in the x direction.
    coeffs_xx = [lamb + 2*mu, mu]
    diffs_xx = [(2, 0), (0, 2)]
    # x component of force resulting from displacement in the y direction.
    coeffs_xy = [lamb + mu]
    diffs_xy = [(1, 1)]
    # y component of force resulting from displacement in the x direction.
    coeffs_yx = [lamb + mu]
    diffs_yx = [(1, 1)]
    # y component of force resulting from displacement in the y direction.
    coeffs_yy = [lamb + 2*mu, mu]
    diffs_yy =  [(0, 2), (2, 0)]
    # make the differentiation matrices that enforce the PDE on the interior
    # nodes.
    diffs = diffs_xx + diffs_xy + diffs_yx + diffs_yy
    coeffs = coeffs_xx + coeffs_xy + coeffs_yx + coeffs_yy
    Ds = weight_matrix(
        x, p, n, diffs, coeffs=coeffs, sum_terms=False, **kwargs
        )

    out = {
        'xx': Ds[0] + Ds[1],
        'xy': Ds[2],
        'yx': Ds[3],
        'yy': Ds[4] + Ds[5]
        }

    return out

    # The above should be equivalent to:
    #D_xx = weight_matrix(x, p, n, diffs_xx, coeffs=coeffs_xx, **kwargs)
    #D_xy = weight_matrix(x, p, n, diffs_xy, coeffs=coeffs_xy, **kwargs)
    #D_yx = weight_matrix(x, p, n, diffs_yx, coeffs=coeffs_yx, **kwargs)
    #D_yy = weight_matrix(x, p, n, diffs_yy, coeffs=coeffs_yy, **kwargs)
    #return {'xx':D_xx, 'xy':D_xy, 'yx':D_yx, 'yy':D_yy}

def elastic2d_surface_force(x, nrm, p, n, lamb=1.0, mu=1.0, **kwargs):
    '''
    Returns weight matrices that map displacements at `p` to the surface
    traction force at `x` with normals `nrm` in a two-dimensional (plane
    strain) homogeneous elastic medium.

    Parameters
    ----------
    x: (N, 2) array
        target points which reside on a surface.

    nrm: (N, 2) array
        surface normal vectors at each point in `x`.

    p: (M, 2) array
        observation points.

    n : int
        stencil size

    lamb, mu: float
        Lame parameters

    **kwargs:
        additional arguments passed to `weight_matrix`

    Returns
    -------
    dict
        keys are the components and the values are the corresponding weight
        matrices.

    '''
    # x component of traction force resulting from x displacement
    coeffs_xx = [nrm[:, 0]*(lamb + 2*mu), nrm[:, 1]*mu]
    diffs_xx =  [(1, 0), (0, 1)]
    # x component of traction force resulting from y displacement
    coeffs_xy = [nrm[:, 0]*lamb, nrm[:, 1]*mu]
    diffs_xy =  [(0, 1), (1, 0)]
    # y component of traction force resulting from x displacement
    coeffs_yx = [nrm[:, 0]*mu, nrm[:, 1]*lamb]
    diffs_yx =  [(0, 1), (1, 0)]
    # y component of force resulting from displacement in the y direction
    coeffs_yy = [nrm[:, 0]*mu, nrm[:, 1]*(lamb + 2*mu)]
    diffs_yy =  [(1, 0), (0, 1)]

    diffs = diffs_xx + diffs_xy + diffs_yx + diffs_yy
    coeffs = coeffs_xx + coeffs_xy + coeffs_yx + coeffs_yy
    Ds = weight_matrix(
        x, p, n, diffs, coeffs=coeffs, sum_terms=False, **kwargs
        )

    out = {
        'xx': Ds[0] + Ds[1],
        'xy': Ds[2] + Ds[3],
        'yx': Ds[4] + Ds[5],
        'yy': Ds[6] + Ds[7]
        }

    return out

    # make the differentiation matrices that enforce the free surface boundary
    # conditions.
    #D_xx = weight_matrix(x, p, n, diffs_xx, coeffs=coeffs_xx, **kwargs)
    #D_xy = weight_matrix(x, p, n, diffs_xy, coeffs=coeffs_xy, **kwargs)
    #D_yx = weight_matrix(x, p, n, diffs_yx, coeffs=coeffs_yx, **kwargs)
    #D_yy = weight_matrix(x, p, n, diffs_yy, coeffs=coeffs_yy, **kwargs)
    #return {'xx':D_xx, 'xy':D_xy, 'yx':D_yx, 'yy':D_yy}


def elastic2d_displacement(x, p, n, **kwargs):
    '''
    Returns weight matrices that map displacements at `p` to the displacements
    at `x`.

    Parameters
    ----------
    x: (N, 2) array
        target points.

    p: (M, 2) array
        observation points.

    n : int
        stencil size

    **kwargs:
        additional arguments passed to `weight_matrix`

    Returns
    -------
    dict
        keys are the components and the values are the corresponding weight
        matrices.

    '''
    D_xx = weight_matrix(x, p, n, (0, 0), **kwargs)
    D_yy = weight_matrix(x, p, n, (0, 0), **kwargs)
    return {'xx':D_xx, 'yy':D_yy}


def elastic3d_body_force(x, p, n, lamb=1.0, mu=1.0, **kwargs):
    '''
    Returns weight matrices that map displacements at `p` to the body force at
    `x` in a three-dimensional homogeneous elastic medium.

    Parameters
    ----------
    x: (N, 3) array
        target points.

    p: (M, 3) array
        observation points.

    n : int
        stencil size

    lamb, mu: float
        first Lame parameter

    **kwargs:
        additional arguments passed to `weight_matrix`

    Returns
    -------
    dict
        keys are the components and the values are the corresponding weight
        matrices.

    '''
    coeffs_xx = [lamb + 2*mu, mu, mu]
    diffs_xx =  [(2, 0, 0), (0, 2, 0), (0, 0, 2)]
    coeffs_xy = [lamb + mu]
    diffs_xy =  [(1, 1, 0)]
    coeffs_xz = [lamb + mu]
    diffs_xz =  [(1, 0, 1)]
    coeffs_yx = [lamb + mu]
    diffs_yx =  [(1, 1, 0)]
    coeffs_yy = [ mu, lamb + 2*mu, mu]
    diffs_yy =  [(2, 0, 0), (0, 2, 0), (0, 0, 2)]
    coeffs_yz = [lamb + mu]
    diffs_yz =  [(0, 1, 1)]
    coeffs_zx = [lamb + mu]
    diffs_zx =  [(1, 0, 1)]
    coeffs_zy = [lamb + mu]
    diffs_zy =  [(0, 1, 1)]
    coeffs_zz = [mu, mu, lamb + 2*mu]
    diffs_zz =  [(2, 0, 0), (0, 2, 0), (0, 0, 2)]
    D_xx = weight_matrix(x, p, n, diffs_xx, coeffs=coeffs_xx, **kwargs)
    D_xy = weight_matrix(x, p, n, diffs_xy, coeffs=coeffs_xy, **kwargs)
    D_xz = weight_matrix(x, p, n, diffs_xz, coeffs=coeffs_xz, **kwargs)
    D_yx = weight_matrix(x, p, n, diffs_yx, coeffs=coeffs_yx, **kwargs)
    D_yy = weight_matrix(x, p, n, diffs_yy, coeffs=coeffs_yy, **kwargs)
    D_yz = weight_matrix(x, p, n, diffs_yz, coeffs=coeffs_yz, **kwargs)
    D_zx = weight_matrix(x, p, n, diffs_zx, coeffs=coeffs_zx, **kwargs)
    D_zy = weight_matrix(x, p, n, diffs_zy, coeffs=coeffs_zy, **kwargs)
    D_zz = weight_matrix(x, p, n, diffs_zz, coeffs=coeffs_zz, **kwargs)
    return {'xx':D_xx, 'xy':D_xy, 'xz':D_xz,
            'yx':D_yx, 'yy':D_yy, 'yz':D_yz,
            'zx':D_zx, 'zy':D_zy, 'zz':D_zz}


def elastic3d_surface_force(x, nrm, p, n, lamb=1.0, mu=1.0, **kwargs):
    '''
    Returns weight matrices that map displacements at `p` to the surface
    traction force at `x` with normals `nrm` in a three-dimensional homogeneous
    elastic medium.

    Parameters
    ----------
    x: (N, 3) array
        target points which reside on a surface.

    nrm: (N, 3) array
        surface normal vectors at each point in `x`.

    p: (M, 3) array
        observation points.

    n : int
        stencil size

    lamb, mu: float
        Lame parameters

    **kwargs:
        additional arguments passed to `weight_matrix`

    Returns
    -------
    dict
        keys are the components and the values are the corresponding weight
        matrices.

    '''
    coeffs_xx = [nrm[:, 0]*(lamb + 2*mu), nrm[:, 1]*mu, nrm[:, 2]*mu]
    diffs_xx =  [(1, 0, 0), (0, 1, 0), (0, 0, 1)]
    coeffs_xy = [nrm[:, 0]*lamb, nrm[:, 1]*mu]
    diffs_xy =  [(0, 1, 0), (1, 0, 0)]
    coeffs_xz = [nrm[:, 0]*lamb, nrm[:, 2]*mu]
    diffs_xz =  [(0, 0, 1), (1, 0, 0)]
    coeffs_yx = [nrm[:, 0]*mu, nrm[:, 1]*lamb]
    diffs_yx =  [(0, 1, 0), (1, 0, 0)]
    coeffs_yy = [nrm[:, 0]*mu, nrm[:, 1]*(lamb + 2*mu), nrm[:, 2]*mu]
    diffs_yy =  [(1, 0, 0), (0, 1, 0), (0, 0, 1)]
    coeffs_yz = [nrm[:, 1]*lamb, nrm[:, 2]*mu]
    diffs_yz =  [(0, 0, 1), (0, 1, 0)]
    coeffs_zx = [nrm[:, 0]*mu, nrm[:, 2]*lamb]
    diffs_zx =  [(0, 0, 1), (1, 0, 0)]
    coeffs_zy = [nrm[:, 1]*mu, nrm[:, 2]*lamb]
    diffs_zy =  [(0, 0, 1), (0, 1, 0)]
    coeffs_zz = [nrm[:, 0]*mu, nrm[:, 1]*mu, nrm[:, 2]*(lamb + 2*mu)]
    diffs_zz =  [(1, 0, 0), (0, 1, 0), (0, 0, 1)]
    D_xx = weight_matrix(x, p, n, diffs_xx, coeffs=coeffs_xx, **kwargs)
    D_xy = weight_matrix(x, p, n, diffs_xy, coeffs=coeffs_xy, **kwargs)
    D_xz = weight_matrix(x, p, n, diffs_xz, coeffs=coeffs_xz, **kwargs)
    D_yx = weight_matrix(x, p, n, diffs_yx, coeffs=coeffs_yx, **kwargs)
    D_yy = weight_matrix(x, p, n, diffs_yy, coeffs=coeffs_yy, **kwargs)
    D_yz = weight_matrix(x, p, n, diffs_yz, coeffs=coeffs_yz, **kwargs)
    D_zx = weight_matrix(x, p, n, diffs_zx, coeffs=coeffs_zx, **kwargs)
    D_zy = weight_matrix(x, p, n, diffs_zy, coeffs=coeffs_zy, **kwargs)
    D_zz = weight_matrix(x, p, n, diffs_zz, coeffs=coeffs_zz, **kwargs)
    return {'xx':D_xx, 'xy':D_xy, 'xz':D_xz,
            'yx':D_yx, 'yy':D_yy, 'yz':D_yz,
            'zx':D_zx, 'zy':D_zy, 'zz':D_zz}


def elastic3d_displacement(x, p, n, **kwargs):
    '''
    Returns weight matrices that map displacements at `p` to the displacements
    at `x`.

    Parameters
    ----------
    x: (N, 3) array
        target points.

    p: (M, 3) array
        observation points.

    n : int
        stencil size

    **kwargs:
        additional arguments passed to `weight_matrix`

    Returns
    -------
    dict
        keys are the components and the values are the corresponding weight
        matrices.

    '''
    D_xx = weight_matrix(x, p, n, (0, 0, 0), **kwargs)
    D_yy = weight_matrix(x, p, n, (0, 0, 0), **kwargs)
    D_zz = weight_matrix(x, p, n, (0, 0, 0), **kwargs)
    return {'xx':D_xx, 'yy':D_yy, 'zz':D_zz}
