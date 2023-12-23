
SELECT restaurant.cooking_bin, count(order.restaurant_id)
FROM order_detail_new order
LEFT OUTER JOIN restaurant_detail_new restaurant
ON order.restaurant_id = restaurant.id
GROUP BY restaurant.cooking_bin
