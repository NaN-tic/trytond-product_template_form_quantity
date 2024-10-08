# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.pool import Pool
from . import product
from . import stock


def register():
    Pool.register(
        product.Product,
        stock.Configuration,
        stock.ConfigurationProductTemplateFormQuantity,
        module='product_template_form_quantity', type_='model')
