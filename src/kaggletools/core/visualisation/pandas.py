from typing import Callable

from pandas.io.formats.style import Styler

__all__ = ['GradientBackgroundFiller', 'NumericalDataTransformer']


class GradientBackgroundFiller:
    @staticmethod
    def red_blue(vmin: float = -1, vmax: float = 1) -> Callable[[Styler], Styler]:
        def style_applier(styler: Styler):
            styler.background_gradient(vmin=vmin, vmax=vmax, cmap='seismic')
            return styler
        return style_applier


class NumericalDataTransformer:
    @staticmethod
    def round(precision=2, truncate_leading_zero=True) -> Callable[[Styler], Styler]:
        def style_applier(styler: Styler):
            formatter = f'{{:.{precision}f}}'
            if truncate_leading_zero:
                formatter = lambda v: formatter.format(v).lstrip('0')
            styler.format(formatter=formatter, na_rep='NA')
            return styler

        return style_applier
