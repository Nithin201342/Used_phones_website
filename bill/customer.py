from flask import *
from database import *

customer=Blueprint('customer',__name__)

@customer.route('/customer_home')
def customer_home():
	return render_template('customer_home.html')

@customer.route('/customer_view_all_product',methods=['get','post'])
def customer_view_all_product():
	data={}
	if 'search' in request.form:
		serach='%'+request.form['search']+'%'

		q="SELECT * FROM `item` , `subcategory` ,`purchase_child` WHERE (`subcategory`.`subcategory_id`=`item`.`subcategory_id` AND `item`.`item_id`=`purchase_child`.`item_id` AND `item`.`status`='active'  AND `item_name` LIKE '%s')OR (`subcategory`.`subcategory_id`=`item`.`subcategory_id` AND `subcategory` AND `item`.`status`='active' AND `subcategory_name` LIKE '%s') GROUP BY item_name"%(serach,serach)
		print(q)


	else:
		q="SELECT * FROM `item` , `subcategory` ,`purchase_child` WHERE `subcategory`.`subcategory_id`=`item`.`subcategory_id` AND `item`.`item_id`=`purchase_child`.`item_id` AND `item`.`status`='active'  GROUP BY `item_name`"
		res=select(q)
		data['view']=res

	
	return render_template('customer_view_all_product.html',data=data)

@customer.route('/customer_view_item',methods=['get','post'])
def customer_view_item():
	data={}
	pid=request.args['pid']
	q="SELECT * FROM `item` INNER JOIN `purchase_child` USING(`item_id`) inner join subcategory using(subcategory_id) inner join category on subcategory.cat_id=category.category_id where item_id='%s'"%(pid)
	res=select(q)
	data['res']=res
	
	return render_template('customer_view_product.html',data=data)

@customer.route('/customer_add_tocart',methods=['get','post'])
def customer_add_tocart():
	data={}
	st=request.args['stock']
	item=request.args['item']
	amount=request.args['amount']
	pid=request.args['pid']

	if 'btn' in request.form:
		quantity=request.form['quantity']
		total=request.form['total']
		if int(st)< int(quantity):
			flash('enter less quantity')
		else:  
			q="SELECT * FROM `cart_master` WHERE `order_status`='pending' and customer_id='%s'"%(session['u_id'])
			res=select(q)
			if res:
				oid=res[0]['cart_master_id']
			else:
				q="INSERT INTO `cart_master` VALUES(NULL,'%s','0','pending')"%(session['u_id'])
				oid=insert(q)
			q="select * from cart_child where item_id='%s' and cart_master_id='%s'"%(pid,oid)
			res1=select(q)
			if res1:
				a=res1[0]['quantity']
				quantity=request.form['quantity']




				c=int(a)+int(quantity)
				print(c)

				if int(c) > int(st):
					
					flash('Out Of Stock')
					
				else:
					q="UPDATE `cart_child` SET `quantity`=quantity+'%s' , `total_price`=`total_price`+'%s' where cart_child_id='%s' and item_id='%s' "%(quantity,total,res1[0]['order_detail_id'],pid)
					print(q)
					update(q)
			else:
				q="INSERT INTO `cart_child` VALUES (NULL,'%s','%s','%s',curdate(),'%s')"%(oid,pid,quantity,total)
				insert(q)
			q="update cart_master set total_amount=total_amount+'%s' where cart_master_id='%s'"%(total,oid)
			print(q)
			update(q)
			flash("Successfully added to Cart")
			return redirect(url_for("customer.customer_view_all_product"))

	# data={}
	# item=request.args['item']
	# amount=request.args['amount']
	# pid=request.args['pid']

	# if 'btn' in request.form:
	# 	quantity=request.form['quantity']
	# 	total=request.form['total']
	# 	q="SELECT * FROM `cart_master` WHERE `order_status`='pending' and customer_id='%s'"%(session['u_id'])
	# 	res=select(q)
	# 	if res:
	# 		oid=res[0]['cart_master_id']
	# 	else:
	# 		q="INSERT INTO `cart_master` VALUES(NULL,'%s','0',CURDATE(),'pending')"%(session['u_id'])
	# 		oid=insert(q)
	# 	q="select * from cart_child where item_id='%s' and cart_master_id='%s'"%(pid,oid)
	# 	res1=select(q)
	# 	if res1:
	# 		q="UPDATE `cart_child` SET `quantity`=quantity+'%s' , `total_price`=`total_price`+'%s' where cart_child_id='%s' and item_id='%s' "%(quantity,total,res1[0]['cart_child_id'],pid)
	# 		print(q)
	# 		update(q)
	# 	else:
	# 		q="INSERT INTO `cart_child` VALUES (NULL,'%s','%s','%s','%s')"%(oid,pid,quantity,total)
	# 		insert(q)
	# 	q="update cart_master set total_amount=total_amount+'%s' where cart_master_id='%s'"%(total,oid)
	# 	print(q)
	# 	update(q)
	# 	flash("Successfully added to Cart")
	# 	return redirect(url_for("customer.customer_view_all_item"))
	return render_template('customer_add_tocart.html',data=data,item=item,amount=amount,st=st)

@customer.route('/customer_view_cart',methods=['get','post'])
def customer_view_cart():
	data={}
	q="SELECT *,`cart_child`.cart_child_id AS cart_child_id,cart_child.quantity as quantity FROM `cart_master`, `cart_child`, `item`,purchase_child WHERE `cart_master`.`cart_master_id`=`cart_child`.`cart_master_id` AND `cart_child`.`item_id`=`item`.`item_id` AND purchase_child.item_id=item.item_id AND  customer_id='%s' AND order_status='pending'"%(session['u_id'])
	res=select(q)

	# print(len(res))
	data['val']=len(res)


	data['res']=res

	if 'action' in request.args:
		action=request.args['action']    
		omid=request.args['omid']
		odid=request.args['odid']
		pid=request.args['pid']
	else: 
		action=None

	if action == "remove":
		q="select * from cart_child where cart_child_id='%s'"%(odid)
		print(q)
		amount=select(q)[0]['total_price']
		q="delete from cart_child where cart_child_id='%s'"%(odid)
		delete(q)
		q="update cart_master set total_amount=total_amount-'%s' where cart_master_id='%s'"%(amount,omid)
		update(q)
		q="select * from cart_child where cart_master_id='%s'"%(omid)
		res7=select(q)
		if len(res7) < 1:
			q="delete from cart_master where cart_master_id='%s'"%(omid)
			delete(q)

			return redirect(url_for("customer.customer_view_cart"))

	if action == "add":
		q="select * from item inner join purchase_child using (item_id) where item_id='%s'"%(pid)
		price=select(q)[0]['selling_price']
		q="update cart_child set quantity = quantity+1, total_price=total_price+'%s' where cart_child_id='%s'"%(price,odid)
		update(q)
		q="update cart_master set total_amount=total_amount+'%s' where cart_master_id='%s'"%(price,omid)
		update(q)
		return redirect(url_for("customer.customer_view_cart"))


	if action == "dec":
		q="select * from item inner join purchase_child using (item_id) where item_id='%s'"%(pid)
		price=select(q)[0]['selling_price']
		q="update cart_child set quantity = quantity-1, total_price=total_price-'%s' where cart_child_id='%s'"%(price,odid)
		update(q)
		q="update cart_master set total_amount=total_amount-'%s' where cart_master_id='%s'"%(price,omid)
		update(q)
		return redirect(url_for("customer.customer_view_cart"))

	if 'btncheckout' in request.form:
		total=request.form['total']
		print("ssssssssssssssssssssssssssssssss"+total)
		omid=request.form['om_id']
		q="update cart_master set order_status='checkout', total_amount='%s' where cart_master_id='%s'"%(total,omid)
		update(q)
				
		for i in range(1,len(res)+1):
		
			qty=request.form['qty'+str(i)]
			single_price=request.form['single'+str(i)]
			product_id=request.form['pid'+str(i)]
			total_single_price=request.form['singletotal'+str(i)]
			print("bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb"+total)
			
			q="update cart_child set quantity='%s', total_price='%s' where item_id='%s' and cart_master_id='%s'"%(qty,total_single_price,product_id,omid)
			update(q)

		return redirect(url_for("customer.customer_view_cart",amount=total,bmid=omid))
	return render_template('customer_view_cart.html',data=data)

@customer.route('/customer_payment',methods=['get','post'])
def customer_payment():
	data={}
	total=request.args['total']
	om_id=request.args['omid']
	
	data['omid']=om_id

	if 'btn' in request.form:
		q="INSERT INTO `payment` VALUES(NULL,'%s','%s','%s',CURDATE())"%(om_id,session['u_id'],total)
		insert(q)
		flash("Order placed Successfully")
		return redirect(url_for('customer.customer_home',total=total,om_id=om_id))

	return render_template('customer_payment.html',data=data,total=total,om_id=om_id)

@customer.route('/customer_view_orders',methods=['get','post'])
def customer_view_orders():
	data={}

	q="SELECT * FROM `cart_master`, `cart_child` , `item` WHERE `cart_master`.`cart_master_id`=`cart_child`.`cart_master_id` AND `cart_child`.`item_id`=`item`.`item_id` AND `customer_id`='%s' group by item_name"%(session['u_id'])
	res=select(q)
	data['res']=res

	return render_template('customer_view_orders.html',data=data)





@customer.route('/customer_send_complaint',methods=['get','post'])
def customer_send_complaint():
	data={}
	if 'submit' in request.form:
		complaint=request.form['complaint']
		q="INSERT INTO `complaint` VALUES(NULL,'%s','%s','pending',CURDATE())"%(session['u_id'],complaint)
		insert(q)

	q="SELECT * FROM `complaint` WHERE `customer_id`='%s'"%(session['u_id'])
	res=select(q)
	data['view']=res

	return render_template('customer_send_complaint.html',data=data)
@customer.route('/viewinvoice')
def viewinvoice():
    data={} 
    omid=request.args['id']
    q="SELECT * FROM `cart_master`,`cart_child`,`item`,`customer` WHERE `cart_master`.cart_master_id=`cart_child`.cart_master_id AND `cart_child`.item_id=`item`.item_id AND `cart_master`.customer_id=`customer`.customer_id and cart_master.cart_master_id='%s' and cart_master.customer_id='%s' "%(omid,session['u_id'])
    print(q)
    data['pay']=select(q)
    return render_template("bill.html",data=data)