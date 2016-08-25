# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
import unittest
import trytond.tests.test_tryton
from trytond.tests.test_tryton import ModuleTestCase


class ProductTemplateFormQuantityTestCase(ModuleTestCase):
    'Test Product Template Form Quantity module'
    module = 'product_template_form_quantity'


def suite():
    suite = trytond.tests.test_tryton.suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(
        ProductTemplateFormQuantityTestCase))
    return suite
