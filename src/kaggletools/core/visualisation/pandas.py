from pandas.io.formats.style import Styler

__all__ = ['GradientBackgroundFiller']


class GradientBackgroundFiller:
    @staticmethod
    def red_blue(styler: Styler, vmin: float = -1, vmax: float = 1) -> Styler:
        styler.background_gradient(vmin=vmin, vmax=vmax, cmap='seismic')
        return styler


class NumericalDataTransformer:
    @staticmethod
    def round(styler: Styler, ):
        ...
