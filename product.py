# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.pool import Pool, PoolMeta
from trytond.transaction import Transaction

__all__ = ['Template']
__metaclass__ = PoolMeta


class Template:
    __name__ = 'product.template'

    def sum_product(self, name):
        pool = Pool()
        StockConfiguration = pool.get('stock.configuration')

        if (name in ('quantity', 'forecast_quantity') and
                'locations' not in Transaction().context):
            warehouses = [StockConfiguration(1).warehouse]
            location_ids = [w.storage_location.id for w in warehouses]
            with Transaction().set_context(locations=location_ids):
                return super(Template, self).sum_product(name)
        return super(Template, self).sum_product(name)
