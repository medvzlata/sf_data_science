import pandas as pd

orders_df = pd.read_csv('hw_orders/orders.csv', sep=';')
print(orders_df.info())
product_df = pd.read_csv('hw_orders/products.csv', sep=';')
print(product_df.info())
#Объедините заданные таблицы в таблицу orders_products, чтобы в результирующей таблице оказалась информация обо всех заказах,
# но не оказалось информации о продуктах, на которых заказов ещё не поступало. 
orders_products = orders_df.merge(
    product_df, 
    left_on='ID товара',
    right_on='Product_ID',
    how='left')
#print(orders_products.tail(1)['Order ID'])
print(orders_products)
#На какой товар была произведена отмена? В качестве ответа запишите название этого товара (Name).
print(orders_products[orders_products['Отменен'] == 'Да']['Name'])
#Какой покупатель принёс наибольшую суммарную прибыль интернет-магазину за указанный период?
#Прибыль состоит только из оплаченных заказов и рассчитывается как количество купленного товара, умноженное на его цену
orders_products['Profit'] = orders_products['Количество']*orders_products['Price']
print(orders_products[orders_products['Оплачен'] == 'Да'].groupby('ID Покупателя')['Profit'].sum().sort_values(ascending=False))