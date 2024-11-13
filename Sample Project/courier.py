from flask import *
from database import *

courier = Blueprint('courier', __name__)


@courier.route('/courierhome', methods=['post', 'get'])
def courierhome():
    # display name
    data = {}
    # data['name'] = session['name']
    q = "SELECT * FROM tbl_cart_master INNER JOIN tbl_cart_child USING(cart_master_id)INNER JOIN tbl_item USING(item_id) INNER JOIN tbl_category USING(cat_id) INNER JOIN tbl_brand USING(brand_id)INNER JOIN tbl_payment USING(cart_master_id) INNER JOIN tbl_purchase_child USING(pur_child_id) INNER JOIN tbl_customer USING(cust_id) INNER JOIN tbl_delivery USING(cart_master_id) INNER JOIN tbl_cour USING(courier_id) WHERE c_status='pickup' AND tbl_delivery.status='pickup' OR c_status='dispatch' AND tbl_delivery.status='dispatch' OR c_status='delivered' AND tbl_delivery.status='delivered' AND p_status=0 AND courier_id='%s'" % (
        session['courid'])
    res = select(q)
    data['view'] = res

    if 'action' in request.args:
        action = request.args['action']
        omid = request.args['omid']
        # dil_id=request.args['dil_id']
    else:
        action=None

    if action=='accept':
        # q="UPDATE `delivery` SET `status`='pickup' WHERE `delivery_id`='%s'"%(res[0]['delivery_id'])
        q="UPDATE `tbl_delivery` SET `status`='pickup' WHERE `cart_master_id`='%s'"%(omid)
        update(q)
        q="UPDATE `tbl_cart_master` SET `c_status`='pickup' WHERE `cart_master_id`='%s'"%(omid)
        update(q)
        flash("Get Ready For Pickup!")
        return redirect(url_for('courier.courierhome'))
    
    if action=='delivered':
        # q="UPDATE `delivery` SET `status`='pickup' WHERE `delivery_id`='%s'"%(res[0]['delivery_id'])
        q="UPDATE `tbl_delivery` SET `status`='delivered' WHERE `cart_master_id`='%s'"%(omid)
        update(q)
        q="UPDATE `tbl_cart_master` SET `c_status`='delivered' WHERE `cart_master_id`='%s'"%(omid)
        update(q)
        flash("Thanks For Delivering...")
        return redirect(url_for('courier.courierhome'))


    return render_template('courierhome.html', data=data)