# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from dateutil.relativedelta import relativedelta
from trytond.pool import Pool, PoolMeta
from trytond.transaction import Transaction

__all__ = ['Template']


class Template:
    __metaclass__ = PoolMeta
    __name__ = 'product.template'

    def sum_product(self, name):
        pool = Pool()
        Configuration = pool.get('stock.configuration')
        Location = pool.get('stock.location')
        Date = pool.get('ir.date')

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
                return super(Template, self).sum_product(name)

        return super(Template, self).sum_product(name)
