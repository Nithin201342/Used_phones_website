from flask import *
from database import *

customer = Blueprint('customer', __name__)


@customer.route('/customerhome', methods=['post', 'get'])
def customerhome():
    # display name
    data = {}
    data['name'] = session['name']

    return render_template('customerhome.html', data=data)


@customer.route('/customerproduct', methods=['post', 'get'])
def customerproduct():
    # product display
    data = {}
    q = "SELECT * FROM tbl_purchase_master INNER JOIN tbl_purchase_child ON tbl_purchase_master.`pur_master_id`=tbl_purchase_child.`pur_master_id` INNER JOIN tbl_item ON tbl_purchase_child.item_id=tbl_item.item_id INNER JOIN tbl_category USING (cat_id) INNER JOIN tbl_brand USING (brand_id) WHERE tbl_purchase_master.status='paid' AND tbl_category.status=1 AND tbl_brand.status=1 AND p_status='1'"
    res = select(q)
    data['productsearch'] = res

    if 'action' in request.args:
        action = request.args['action']
        amount = request.args['amount']
        pid = request.args['pid']
        pcid = request.args['pcid']
    else:
        action = None

    if action == "cart":
        # q = "SELECT * FROM `tbl_cart_master` WHERE `status`='pending' and cust_id='%s'" % (session['cid'])
        q = "SELECT * FROM `tbl_cart_master` INNER JOIN tbl_cart_child USING(cart_master_id) INNER JOIN tbl_purchase_child USING(item_id) WHERE `c_status`='pending' AND cust_id='%s'" % (
            session['cid'])
        print(q)
        res = select(q)
        if res:
            oid = res[0]['cart_master_id']
        else:
            q = "INSERT INTO `tbl_cart_master` VALUES(NULL,'%s','0','pending')" % (
                session['cid'])
            oid = insert(q)

        q = "select * from tbl_cart_child where pur_child_id='%s' and cart_master_id='%s'" % (
            pcid, oid)
        res1 = select(q)
        if res1:
            flash("Already Added To Cart!")
        else:
            q = "INSERT INTO `tbl_cart_child` VALUES (NULL,'%s','%s','%s','%s')" % (
                oid, pcid, pid, amount)
            insert(q)
            q = "update tbl_cart_master set tot_amt=tot_amt+'%s' where cart_master_id='%s'" % (
                amount, oid)
            update(q)
            flash("Successfully Added To Cart")
        return redirect(url_for("customer.customerproduct"))

    # if action == "details":
    #     n = "SELECT * FROM tbl_purchase_child INNER JOIN tbl_item USING(item_id) INNER JOIN tbl_brand USING(brand_id) WHERE pur_child_id='%s'" % (pcid)
    #     res = select(n)
    #     data['productsearch'] = res

    return render_template('customerproduct.html', data=data)


@customer.route('/customerproductdetails')
def customerproductdetails():
    return render_template('customerproductdetails.html')


@customer.route('/customercart', methods=['post', 'get'])
def customercart():
    # cart view
    data = {}
    # pcid = request.form['pcid']
    flag = 0
    outs = ""
    ss = ""
    print("/////////////////////////////////")
    q = """ SELECT * FROM tbl_cart_master INNER JOIN tbl_cart_child USING(cart_master_id)INNER JOIN
        tbl_item USING(item_id) INNER JOIN tbl_category USING(cat_id) INNER JOIN tbl_brand USING(brand_id)
        INNER JOIN tbl_purchase_child USING(pur_child_id) WHERE c_status='pending' AND cust_id='%s'
        AND tbl_brand.status='1' AND tbl_category.status='1' GROUP BY `tbl_cart_child`.pur_child_id """ % (session['cid'])
    print(q)
    res = select(q)
    for row in res:
        print("ppppppp", row['p_status'])
        out = row['p_status']
        if out == "0":
            flag = 1
            outs = outs+row['item_name']+", "

    if flag == 1:
        ss = outs+" Is Out Of Stock"
    data['flag'] = flag
    data['out'] = ss

    data['view'] = res

    # from datetime import date
    # today=date.today()
    # data['today']=today

    # r = "SELECT COUNT(*) AS COUNT FROM tbl_cart_master WHERE status='pending' AND cust_id='%s'"%(session['cid'])
    # res = select(r)
    # data['cart'] = res[0]['count']

    if 'action' in request.args:
        action = request.args['action']
        cmid = request.args['cmid']
        ccid = request.args['ccid']
        price = request.args['price']
    else:
        action = None

    if action == "remove":
        q = "delete from tbl_cart_child where cart_child_id='%s'" % (ccid)
        delete(q)
        q = "update tbl_cart_master set tot_amt=tot_amt-'%s' where cart_master_id='%s'" % (
            price, cmid)
        update(q)
        q = "select * from tbl_cart_child where cart_master_id='%s'" % (cmid)
        val = select(q)
        if val:
            flash("Item Removed")
        else:
            q = "delete from tbl_cart_master where cart_master_id='%s'" % (
                cmid)
            delete(q)
        return redirect(url_for("customer.customercart"))

    return render_template('customercart.html', data=data)


@ customer.route('/customerpayment', methods=['post', 'get'])
def customerpayment():
    data = {}
    cmid = request.args['cmid']
    pcid = request.args['pcid']
    q = "SELECT * FROM tbl_payment where cart_master_id='%s'" % (cmid)
    data['res'] = select(q)

    if 'btn' in request.form:
        cname = request.form['name']
        cno = request.form['cardno']
        expdate = request.form['expdate']

        q = "insert into tbl_payment values(null,'%s',curdate())" % (cmid)
        insert(q)
        w = "update tbl_cart_master set c_status='paid' where cart_master_id='%s'" % (
            cmid)
        update(w)
        x = "update tbl_purchase_child set p_status='0' where pur_child_id='%s'" % (
            pcid)
        update(x)
        e = "insert into tbl_card values(null,'%s','%s','%s','%s')" % (
            session['cid'], cno, cname, expdate)
        insert(e)
        flash("Payment Successfull")
        return redirect(url_for('customer.customerhome'))

    return render_template('customerpayment.html', data=data)


@ customer.route('/customerorders', methods=['post', 'get'])
def customerorders():
    data = {}
    q = "SELECT * FROM tbl_cart_master INNER JOIN tbl_cart_child USING(cart_master_id)INNER JOIN tbl_item USING(item_id) INNER JOIN tbl_category USING(cat_id) INNER JOIN tbl_brand USING(brand_id) INNER JOIN tbl_purchase_child USING(pur_child_id) INNER JOIN tbl_payment USING(cart_master_id) WHERE p_status='0' and cust_id='%s'" % (
        session['cid'])
    res = select(q)
    data['view'] = res
    return render_template('customerorders.html', data=data)


@customer.route('/bill')
def bill():
    data = {}
    omid = request.args['billcmid']
    cid = session['cid']
    q = "SELECT * FROM `tbl_cart_master`,`tbl_cart_child`,`tbl_item`,`tbl_customer` WHERE `tbl_cart_master`.cart_master_id=`tbl_cart_child`.cart_master_id AND `tbl_cart_child`.item_id=`tbl_item`.item_id AND `tbl_cart_master`.cust_id=`tbl_customer`.cust_id and tbl_cart_master.cart_master_id='%s' and tbl_cart_master.cust_id='%s' " % (
        omid, cid)
    data['pay'] = select(q)
    return render_template("bill.html", data=data)
