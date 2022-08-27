from datetime import timedelta

from import_export.widgets import NumberWidget, Widget


class CommaFloatWidget(NumberWidget):
    """
    Widget for converting floats fields replacing , to .
    """

    def clean(self, value, row=None, *args, **kwargs):
        if self.is_empty(value):
            return None
        if ',' in value:
            value = value.replace(',', '.')
        return float(value)


class SecondsDurationWidget(Widget):
    """
    Widget for converting time duration fields.
    """

    def clean(self, value, row=None, *args, **kwargs):
        if not value:
            return None

        value = value.replace(',', '.')

        try:
            return timedelta(seconds=float(value))
        except (ValueError, TypeError):
            raise ValueError("Enter a valid duration.")
