#This file is part of Tryton.  The COPYRIGHT file at the top level of
#this repository contains the full copyright notices and license terms.
import unittest
import doctest
import datetime
from decimal import Decimal
from dateutil.relativedelta import relativedelta

import trytond.tests.test_tryton
from trytond.tests.test_tryton import POOL, DB_NAME, USER, CONTEXT, test_view,\
    test_depends
from trytond.transaction import Transaction


class ProductTemplateFormQuantityTestCase(unittest.TestCase):
    'Test Product Template Form Quantity module'

    def setUp(self):
        trytond.tests.test_tryton.install_module('product_template_form_quantity')
        self.company = POOL.get('company.company')
        self.user = POOL.get('res.user')
        self.configuration = POOL.get('stock.configuration')
        self.move = POOL.get('stock.move')
        self.location = POOL.get('stock.location')
        self.template = POOL.get('product.template')
        self.uom = POOL.get('product.uom')

    def test0005views(self):
        'Test views'
        test_view('product_template_form_quantity')

    def test0006depends(self):
        'Test depends'
        test_depends()

    def test0010quantity(self):
        'Test quantity'
        with Transaction().start(DB_NAME, USER, context=CONTEXT):
            company, = self.company.search([
                    ('rec_name', '=', 'Dunder Mifflin'),
                    ])
            currency = company.currency
            self.user.write([self.user(USER)], {
                'main_company': company.id,
                'company': company.id,
                })

            today = datetime.date.today()

            u, = self.uom.search([('name', '=', 'Unit')])
            template, = self.template.create([{
                        'name': 'Product',
                        'default_uom': u.id,
                        'list_price': Decimal(0),
                        'cost_price': Decimal(10),
                        'products': [('create', [{}])],
                        }])
            product, = template.products

            input_location, output_location, storage_location  = self.location.create([{
                        'name': 'Input 2',
                        'type': 'storage',
                        }, {
                        'name': 'Output 2',
                        'type': 'storage',
                        }, {
                        'name': 'Storage 2',
                        'type': 'storage',
                        }])

            self.location.create([{
                        'name': 'Warehouse2',
                        'type': 'warehouse',
                        'input_location': input_location,
                        'output_location': output_location,
                        'storage_location': storage_location,
                        }])

            warehouse1, warehouse2 = self.location.search([
                        ('type', '=', 'warehouse'),
                        ])
            lost_found, = self.location.search([('type', '=', 'lost_found')])

            moves = self.move.create([{
                        'product': product.id,
                        'uom': u.id,
                        'quantity': 5,
                        'from_location': lost_found.id,
                        'to_location': warehouse1.storage_location.id,
                        'company': company.id,
                        'unit_price': Decimal('1'),
                        'currency': currency.id,
                        }, {
                        'product': product.id,
                        'uom': u.id,
                        'quantity': 10,
                        'from_location': lost_found.id,
                        'to_location': warehouse2.storage_location.id,
                        'company': company.id,
                        'unit_price': Decimal('1'),
                        'currency': currency.id,
                        }])
            self.move.do(moves)

            template = self.template(product.template.id)
            self.assertEqual(template.quantity, Decimal('15.0'))

            moves = self.move.create([{
                        'product': product.id,
                        'uom': u.id,
                        'quantity': 5,
                        'from_location': lost_found.id,
                        'to_location': warehouse1.storage_location.id,
                        'planned_date': today + relativedelta(days=5),
                        'effective_date': today + relativedelta(days=5),
                        'company': company.id,
                        'unit_price': Decimal('1'),
                        'currency': currency.id,
                        }])
            self.move.do(moves)

            configuration = self.configuration(1)
            configuration.warehouse = warehouse1
            configuration.leg_days = 10
            configuration.save()

            template = self.template(product.template.id)
            # not sum 5 + 5 (total 10)
            # because effective date last move is today + 5
            self.assertEqual(template.quantity, Decimal('5.0'))


def suite():
    suite = trytond.tests.test_tryton.suite()
    from trytond.modules.company.tests import test_company
    for test in test_company.suite():
        if test not in suite and not isinstance(test, doctest.DocTestCase):
            suite.addTest(test)
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(
        ProductTemplateFormQuantityTestCase))
    return suite
