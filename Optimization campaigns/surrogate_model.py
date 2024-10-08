from baybe.surrogates.gaussian_process.core import GaussianProcessSurrogate
from baybe.kernels import RBFKernel, RQKernel, MaternKernel, AdditiveKernel
from baybe.surrogates.gaussian_process.kernel_factory import PlainKernelFactory
from baybe.surrogates.gaussian_process.core import GaussianProcessSurrogate
from baybe.kernels.base import Kernel
import gpytorch
import torch

class DotProductKernel(Kernel):
    def __init__(self, sigma=1.0):
        super().__init__()
        object.__setattr__(self, '_sigma', sigma)  # Use object.__setattr__ for immutability

    @property
    def sigma(self):
        return self._sigma

    def forward(self, X, Y):
        return self.sigma**2 + torch.mm(X, Y.T)

    def to_gpytorch(self, ard_num_dims=None, batch_shape=torch.Size([]), active_dims=None):
        # Map your custom kernel to an existing gpytorch kernel
        return gpytorch.kernels.LinearKernel(
            num_dims=ard_num_dims,
            batch_shape=batch_shape,
            active_dims=active_dims,
            variance_prior=None,
            bias_prior=None,
        )

def gp_model():

    # Create an instance of the DotProduct kernel with sigma
    dot_product_kernel = DotProductKernel(sigma=0.01)

    rq_kernel = RQKernel(lengthscale_initial_value=0.01)
    matern_kernel = MaternKernel(lengthscale_initial_value=0.1, nu=1.5)

    kernel = AdditiveKernel((dot_product_kernel, rq_kernel, matern_kernel))
    # Wrap the RBF kernel in a PlainKernelFactory
    kernel_factory = PlainKernelFactory(kernel=kernel)

    # Initialize the GaussianProcessSurrogate with the RBF kernel
    gp_surrogate = GaussianProcessSurrogate(kernel_or_factory=kernel_factory)

    return gp_surrogate