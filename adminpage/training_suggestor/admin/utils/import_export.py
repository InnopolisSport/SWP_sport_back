from import_export.widgets import NumberWidget


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
