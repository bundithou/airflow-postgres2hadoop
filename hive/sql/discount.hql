
SELECT restaurant.category, AVG('discount'), AVG('discount_no_null')
FROM order_detail_new order
LEFT OUTER JOIN restaurant_detail_new restaurant
ON order.restaurant_id = restaurant.id
GROUP BY restaurant.category
