# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from dateutil.relativedelta import relativedelta
from trytond.pool import Pool, PoolMeta
from trytond.transaction import Transaction


def get_context():
    pool = Pool()
    Configuration = pool.get('stock.configuration')
    Location = pool.get('stock.location')
    Date = pool.get('ir.date')

    configuration = Configuration(1)

    if configuration.warehouse:
        location_ids = [configuration.warehouse.id]
    else:
        location_ids = [l.id for l in Location.search([
            ('type', '=', 'warehouse'),
            ])]

    lag_days = configuration.lag_days or 0
    stock_date_end = Date.today() + relativedelta(days=int(lag_days))
    return {
        'locations': location_ids,
        'stock_date_end': stock_date_end,
        }


class Product(metaclass=PoolMeta):
    __name__ = 'product.product'

    @classmethod
    def get_quantity(cls, products, name):
        # Only override the behaviour when context does not already
        # condition the quantity to be computed
        if 'locations' in Transaction().context:
            return super().get_quantity(products, name)
        with Transaction().set_context(get_context()):
            return super().get_quantity(products, name)

    @classmethod
    def search_quantity(cls, name, domain=None):
        # Only override the behaviour when context does not already
        # condition the quantity to be computed
        if 'locations' in Transaction().context:
            return super().search_quantity(name, domain)
        with Transaction().set_context(get_context()):
            return super().search_quantity(name, domain)
