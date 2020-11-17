import numpy as np
from controller.recursive_model import *
from scipy import optimize
import copy
import scipy.sparse.linalg as splinalg

class SolowayNR:

    def __init__(self, d_model):
        self.d_model = d_model
        self.previous_norm = 1e2
    def fsolve_newtonkrylov(self, F, u0, epsilon=1e-8, rtol=1e-10, maxit=50, verbose=False):
        u = u0.copy()
        Fu = F(u)
        norm0 = np.linalg.norm(Fu)
        for i in range(maxit):
            def Ju_fd(v):
                return (F(u + epsilon * v) - Fu) / epsilon

            Ju = splinalg.LinearOperator((len(Fu), len(u)), matvec=Ju_fd)
            du, info = splinalg.gmres(Ju, Fu)
            if info != 0:
                raise RuntimeError('GMRES failed to converge: {:d}'.format(info))
            u -= du
            Fu = F(u)
            norm = np.linalg.norm(Fu)
            if verbose:
                print('Newton {:d} anorm {:6.2e} rnorm {:6.2e}'.format(i, norm, norm / norm0))
            if norm < rtol * norm0:
                break
        return u, i

    def __online_fsolve_newton(self, u0, del_u, rtol=1e-10, maxit=50, verbose=False):
        u = np.array(u0).copy()
        del_u = np.zeros(u.shape)
        Fu = -self.d_model.jacobian(u, del_u)
        du = splinalg.spsolve(self.d_model.hessian(u, del_u), Fu)
        u -= du
        del_u = du
        return u, del_u, 0

    def optimize(self, u, delu,maxit = 1, rtol = 1e-8, verbose=False):
       return self.__online_fsolve_newton(u0 = u, del_u = delu, rtol = rtol, maxit = maxit,  verbose = verbose)
