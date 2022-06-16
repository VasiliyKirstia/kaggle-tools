from typing import Callable

from pandas.io.formats.style import Styler

__all__ = ['GradientBackgroundFiller', 'NumericalDataTransformer']


class GradientBackgroundFiller:
    @staticmethod
    def red_blue(vmin: float = -1, vmax: float = 1):
        def style_applier(styler):
            return styler \
                .background_gradient(vmin=vmin, vmax=vmax, cmap='seismic') \
                .highlight_null(null_color='yellow')

        return style_applier


class NumericalDataTransformer:
    @staticmethod
    def round(precision=2, truncate_leading_zero=True, na_rep='NA') -> Callable[[Styler], Styler]:
        def style_applier(styler: Styler):
            template = f'{{:.{precision}f}}'
            if truncate_leading_zero:
                def formatter(v): template.format(v).lstrip('0')
            else:
                formatter = template

            return styler.format(formatter=formatter, na_rep=na_rep)

        return style_applier
