# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.model import fields
from trytond.pyson import Eval
from dateutil.relativedelta import relativedelta
from trytond.pool import Pool, PoolMeta
from trytond.transaction import Transaction

__all__ = ['Template']


class Template:
    __metaclass__ = PoolMeta
    __name__ = 'product.template'

    unit_digits = fields.Function(fields.Integer('Unit Digits'),
        'on_change_with_unit_digits')

    @classmethod
    def __setup__(cls):
        super(Template, cls).__setup__()
        cls.quantity.digits=(16, Eval('unit_digits', 2))

    @fields.depends('default_uom')
    def on_change_with_unit_digits(self, name=None):
        if self.default_uom:
            return self.default_uom.digits
        return 2

    def sum_product(self, name):
        pool = Pool()
        Configuration = pool.get('stock.configuration')
        Location = pool.get('stock.location')
        Date = pool.get('ir.date')
        Uom = pool.get('product.uom')

        if (name in ('quantity', 'forecast_quantity')):
            context = Transaction().context
            configuration = Configuration(1)

            if 'locations' in context:
                location_ids = context['locations']
            else:
                location_ids = (configuration.warehouse and
                    [configuration.warehouse.id] or [])

            if not location_ids:
                location_ids = [l.id for l in Location.search([
                    ('type', '=', 'warehouse'),
                    ])]

            lag_days = configuration.lag_days or 0
            stock_date_end = Date.today() + relativedelta(days=int(lag_days))

            with Transaction().set_context({
                    'locations': location_ids,
                    'stock_date_end': stock_date_end,
                    }):
                self = self.__class__(self.id)

        sum_ = super(Template, self).sum_product(name)
        sum_ = Uom.compute_qty(self.default_uom, sum_)
        return sum_
