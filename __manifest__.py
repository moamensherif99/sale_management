{
    'name': 'Custom Sales Management',
    'version': '1.0',
    'depends': ['sale_management'],
    'data': [
        "views/sale_order.xml",
        "views/product_template.xml",
        "views/product_category.xml",
        "views/product_product.xml",
        "reports/sale_order_report.xml"
    ],
    'installable': True,
    'application': False,
}
