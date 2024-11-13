from flask import *
from database import *
import uuid

admin = Blueprint('admin', __name__)


@admin.route('/adminhome')
def adminhome():
    data = {}
    q = "SELECT COUNT(*) as count FROM tbl_customer"
    res = select(q)
    print(res)
    data['cust'] = res[0]['count']

    q = "SELECT COUNT(*) as count FROM tbl_staff"
    res = select(q)
    print(res)
    data['stf'] = res[0]['count']

    q = "SELECT COUNT(*) as count FROM tbl_brand"
    res = select(q)
    print(res)
    data['brd'] = res[0]['count']

    q = "SELECT COUNT(*) as count FROM tbl_item"
    res = select(q)
    print(res)
    data['prd'] = res[0]['count']

    q = "SELECT COUNT(*) as count FROM tbl_category"
    res = select(q)
    print(res)
    data['cat'] = res[0]['count']

    return render_template('adminhome.html', data=data)


@admin.route('/admincustomer', methods=['post', 'get'])
def admincustomer():
    # table view
    data = {}
    q = "select * from tbl_customer"
    res = select(q)
    data['view'] = res

    # active inactive
    if 'action' in request.args:
        action = request.args['action']
        cid = request.args['cid']
    else:
        action = None
    if action == "inactive":
        q = "update tbl_customer set status='0' where cust_id='%s'" % (cid)
        update(q)
        s = "update tbl_login set status='0' where email='%s'" % (cid)
        update(s)
        return redirect(url_for('admin.admincustomer'))
    if action == "active":
        s = "update tbl_customer set status='1' where cust_id='%s'" % (cid)
        update(s)
        return redirect(url_for('admin.admincustomer'))
    return render_template('admincustomer.html', data=data)


@admin.route('/custreport')
def admincustreport():
    data = {}
    q = "SELECT * FROM tbl_customer"
    data['pay'] = select(q)
    return render_template("admincustomerreport.html", data=data)


@admin.route('/adminstaff', methods=['post', 'get'])
def adminstaff():
    # form
    if 'submit' in request.form:
        email = request.form['email']
        fname = request.form['fname']
        lname = request.form['lname']
        city = request.form['city']
        phone = request.form['phone']
        gender = request.form['gender']
        password = request.form['pass']
        q = "select * from tbl_login where email='%s' " % (email)
        val = select(q)
        if val:
            flash('User Already Exists')
        else:
            r = "insert into tbl_login values('%s','%s','staff',1)" % (
                email, password)
            insert(r)
            s = "insert into tbl_staff values(null,'%s','%s','%s','%s','%s','%s',1)" % (
                email, fname, lname, city, phone, gender)
            insert(s)
            flash('User Successfully Added')
            return redirect(url_for("admin.adminstaff"))

    # table view
    data = {}
    q = "select * from tbl_staff"
    res = select(q)
    data['view'] = res

    # update details
    if 'action' in request.args:
        action = request.args['action']
        id = request.args['id']
    else:
        action = None

    if action == "update":
        q = "select * from tbl_staff where staff_id='%s'" % (id)
        res = select(q)
        data['up'] = res

    if 'update' in request.form:
        fname = request.form['fname']
        lname = request.form['lname']
        phone = request.form['phone']
        city = request.form['city']
        gender = request.form['gender']
        r = "update tbl_staff set staff_fname='%s',staff_lname='%s',staff_phone='%s',staff_city='%s',staff_gender='%s'where staff_id='%s'" % (
            fname, lname, phone, city, gender, id)
        update(r)
        return redirect(url_for('admin.adminstaff'))

    # active inactive
    if action == "inactive":
        q = "update tbl_staff set status='0' where staff_id='%s'" % (id)
        update(q)
        return redirect(url_for('admin.adminstaff'))
    if action == "active":
        s = "update tbl_staff set status='1' where staff_id='%s'" % (id)
        update(s)
        return redirect(url_for('admin.adminstaff'))
    return render_template('adminstaff.html', data=data)


@admin.route('/staffreport')
def adminstaffreport():
    data = {}
    q = "SELECT * FROM tbl_staff"
    data['pay'] = select(q)
    return render_template("adminstaffreport.html", data=data)


@admin.route('/admincategory', methods=['post', 'get'])
def admincategory():
    # form
    if 'submit' in request.form:
        cate = request.form['cate']
        desc = request.form['desc']
        q = "select * from tbl_category where cat_name='%s' " % (cate)
        val = select(q)
        if val:
            flash('Category Already Exists')
        else:
            r = "insert into tbl_category values(null,'%s','%s',1)" % (
                cate, desc)
            insert(r)
            flash('Category Successfully Added')
            return redirect(url_for("admin.admincategory"))

    # table view
    data = {}
    q = "select * from tbl_category"
    res = select(q)
    data['view'] = res

    # update details
    if 'action' in request.args:
        action = request.args['action']
        id = request.args['id']
    else:
        action = None

    if action == "update":
        q = "select * from tbl_category where cat_id='%s'" % (id)
        res = select(q)
        data['up'] = res

    if 'update' in request.form:
        cate = request.form['cate']
        desc = request.form['desc']
        r = "update tbl_category set cat_name='%s',cat_desc='%s'where cat_id='%s'" % (
            cate, desc, id)
        update(r)
        flash('Category Successfully Updated')
        return redirect(url_for('admin.admincategory'))

    # active inactive
    if action == "inactive":
        q = "update tbl_category set status='0' where cat_id='%s'" % (id)
        update(q)
        return redirect(url_for('admin.admincategory'))
    if action == "active":
        s = "update tbl_category set status='1' where cat_id='%s'" % (id)
        update(s)
        return redirect(url_for('admin.admincategory'))
    return render_template('admincategory.html', data=data)


@admin.route('/adminbrand', methods=['post', 'get'])
def adminbrand():
    # form
    if 'submit' in request.form:
        bname = request.form['bname']
        desc = request.form['desc']
        q = "select * from tbl_brand where brand_name='%s' " % (bname)
        val = select(q)
        if val:
            flash('Brand Already Exists')
        else:
            r = "insert into tbl_brand values(null,'%s','%s','1')" % (
                bname, desc)
            insert(r)
            flash('Brand Successfully Added')
            return redirect(url_for("admin.adminbrand"))

    # table view
    data = {}
    q = "select * from tbl_brand"
    res = select(q)
    data['vv'] = res
    print(res)

    # update details
    if 'action' in request.args:
        action = request.args['action']
        id = request.args['id']
    else:
        action = None

    if action == "update":
        q = "select * from tbl_brand where brand_id='%s'" % (id)
        res = select(q)
        data['up'] = res

    if 'update' in request.form:
        bname = request.form['bname']
        desc = request.form['desc']
        n = "update tbl_brand set brand_name='%s',brand_desc='%s'where brand_id='%s'" % (
            bname, desc, id)
        update(n)
        flash('Brand Successfully Updated')
        return redirect(url_for('admin.adminbrand'))

    # active inactive
    if action == "inactive":
        q = "update tbl_brand set status='0' where brand_id='%s'" % (id)
        update(q)
        return redirect(url_for('admin.adminbrand'))
    if action == "active":
        s = "update tbl_brand set status='1' where brand_id='%s'" % (id)
        update(s)
        return redirect(url_for('admin.adminbrand'))

    return render_template('adminbrand.html', data=data)


@admin.route('/adminproduct', methods=['post', 'get'])
def adminproduct():
    # form
    data = {}
    q = "select * from tbl_category where status=1"
    res1 = select(q)
    data['cat'] = res1

    r = "select * from tbl_brand where status=1"
    res = select(r)
    data['view'] = res

    if 'submit' in request.form:
        cat = request.form['cat']
        brand = request.form['brand']
        name = request.form['name']
        q = "select * from tbl_item where item_name='%s' " % (name)
        val = select(q)
        if val:
            flash('Product Already Exists')
        else:
            r = "insert into tbl_item values(null,'%s','%s','%s',1)" % (
                cat, brand, name)
            insert(r)
            flash('Product Successfully Added')
        return redirect(url_for('admin.adminproduct'))

    # table view
    q = "SELECT * FROM tbl_item INNER JOIN tbl_brand USING (brand_id) INNER JOIN tbl_category USING (cat_id) WHERE tbl_brand.status='1' AND tbl_category.status='1'"
    res = select(q)
    data['vv'] = res
    print(res)

    # update details
    if 'action' in request.args:
        action = request.args['action']
        id = request.args['id']
    else:
        action = None

    if action == "update":
        q = "select * from tbl_item where item_id='%s'" % (id)
        res = select(q)
        data['up'] = res

    if 'update' in request.form:
        cat = request.form['cat']
        brand = request.form['brand']
        name = request.form['name']
        n = "update tbl_item set cat_id='%s',brand_id='%s',item_name='%s' where brand_id='%s'" % (
            cat, brand, name, id)
        update(n)
        flash('Product Successfully Updated')
        return redirect(url_for('admin.adminproduct'))

    # active inactive
    if action == "inactive":
        q = "update tbl_item set status='0' where item_id='%s'" % (id)
        update(q)
        return redirect(url_for('admin.adminproduct'))
    if action == "active":
        s = "update tbl_item set status='1' where item_id='%s'" % (id)
        update(s)
        return redirect(url_for('admin.adminproduct'))

    return render_template('adminproduct.html', data=data)


@admin.route('/adminpurchase', methods=['post', 'get'])
def adminpurchase():
    # form
    data = {}
    q = "select * from tbl_customer where status=1"
    res1 = select(q)
    data['cust'] = res1

    r = "select * from tbl_item where status=1"
    res = select(r)
    data['item'] = res

    # purchase
    q = "SELECT * FROM tbl_purchase_master INNER JOIN tbl_purchase_child ON tbl_purchase_master.`pur_master_id`=tbl_purchase_child.`pur_master_id` INNER JOIN tbl_item ON tbl_purchase_child.item_id=tbl_item.item_id where tbl_purchase_master.status='pending'"
    res2 = select(q)
    if res2:
        data['view'] = res2
        data['purcahse'] = res2[0]['pur_master_id']
        purmid = res2[0]['pur_master_id']

    if 'submit' in request.form:
        cid = request.form['cid']
        product = request.form['product']
        desc = request.form['desc']
        profit = request.form['profit']
        cprice = request.form['cprice']
        image = request.files['image']
        sellp = int(profit)*int(cprice)/100
        newsellp = int(cprice)+sellp

        path = "static/uploads/"+str(uuid.uuid4())+str(image.filename)
        image.save(path)

        r = "select * from tbl_purchase_master where cust_id='%s' and status='pending'" % (
            cid)
        res = select(r)
        if res:
            r1 = "select * from tbl_purchase_child where item_id='%s' and p_status='1'" % (
                product)
            res1 = select(r1)
            if res1:
                purmid = res1[0]['pur_master_id']

                q = "update tbl_purchase_master set tot_amt=tot_amt+'%s' where pur_master_id='%s'" % (
                    cprice, purmid)
                update(q)
                q1 = "update tbl_purchase_child set cost_price=cost_price+'%s' where pur_master_id='%s' and item_id='%s'" % (
                    cprice, purmid, product)
                update(q1)

            else:
                s = "update tbl_purchase_master set tot_amt=tot_amt+'%s' pur_master_id='%s'" % (
                    cprice, purmid)
                update(s)
                s1 = "insert into tbl_purchase_child values(null,'%s','%s','%s','%s','%s','%s','%s','1')" % (
                    purmid, product, desc, profit, cprice, newsellp, path)
                insert(s1)

        else:
            q = "insert into tbl_purchase_master values(null,0,'%s',curdate(),'%s','pending')" % (
                cid, cprice)
            pmid = insert(q)
            q = "insert into tbl_purchase_child values(null,'%s','%s','%s','%s','%s','%s','%s','1')" % (
                pmid, product, desc, profit, cprice, newsellp, path)
            insert(q)
            flash("Added To Purchase List")
            return redirect(url_for('admin.adminpurchase'))

    if 'id' in request.args:
        id = request.args['id']
        q = "update tbl_purchase_master set status='paid' where pur_master_id='%s'" % (
            id)
        update(q)
        flash("Purchase Successfull")
        return redirect(url_for('admin.adminpurchase'))

    return render_template('adminpurchase.html', data=data)


@admin.route('/adminpurchaseview', methods=['post', 'get'])
def adminpurchaseview():
    # table view
    data = {}
    q = "SELECT * FROM tbl_purchase_master INNER JOIN tbl_purchase_child USING(pur_master_id)INNER JOIN tbl_item USING(item_id) INNER JOIN tbl_category USING(cat_id) INNER JOIN tbl_brand USING(brand_id) INNER JOIN tbl_customer USING(cust_id) WHERE tbl_purchase_master.status='paid'"
    res = select(q)
    data['view'] = res

    if 'dsch' in request.form:
        dsearch = request.form['dsearch']
        q = "SELECT * FROM tbl_purchase_master om,tbl_purchase_child od,tbl_item p,tbl_customer u WHERE om.pur_master_id=od.pur_master_id AND od.item_id=p.item_id AND om.cust_id=u.cust_id AND om.date='%s'  GROUP BY om.pur_master_id " % (
            dsearch)
        res = select(q)
        data['res'] = select(q)

    # if 'nsch' in request.form:
    #     search="%"+request.form['search']+"%"
    #     q="SELECT * FROM tbl_purchase_master om,tbl_purchase_child od,tbl_item p,tbl_customer u WHERE om.pur_master_id=od.pur_master_id AND od.item_id=p.item_id AND om.cust_id=u.cust_id and cust_fname like '%s'  group by om.pur_master_id "%(search)
    #     res=select(q)
    #     data['res']=select(q)
    return render_template('adminpurchaseview.html', data=data)


@admin.route('/adminpurchaselist', methods=['post', 'get'])
def adminpurchaselist():
    # table view
    data = {}
    q = "SELECT * FROM tbl_purchase_master INNER JOIN tbl_purchase_child USING(pur_master_id)INNER JOIN tbl_item USING(item_id) INNER JOIN tbl_category USING(cat_id) INNER JOIN tbl_brand USING(brand_id) INNER JOIN tbl_customer USING(cust_id) WHERE tbl_purchase_master.status='paid'"
    res = select(q)
    data['view'] = res
    return render_template('adminpurchaselist.html', data=data)


@admin.route('/purchasereport')
def purchasereport():
    data = {}
    q = "SELECT * FROM tbl_purchase_master INNER JOIN tbl_purchase_child USING(pur_master_id)INNER JOIN tbl_item USING(item_id) INNER JOIN tbl_category USING(cat_id) INNER JOIN tbl_brand USING(brand_id) INNER JOIN tbl_customer USING(cust_id) WHERE tbl_purchase_master.status='paid'"
    res = select(q)
    data['view'] = res
    return render_template('purchasereport.html', data=data)


@admin.route('/admincourier', methods=['post', 'get'])
def admincourier():
    # form
    if 'submit' in request.form:
        email = request.form['email']
        fname = request.form['fname']
        gdno = request.form['gdno']
        city = request.form['city']
        phone = request.form['phone']
        pin = request.form['pin']
        password = request.form['pas']
        q = "select * from tbl_login where email='%s' " % (email)
        val = select(q)
        if val:
            flash('User Already Exists')
        else:
            r = "insert into tbl_login values('%s','%s','courier',1)" % (
                email, password)
            insert(r)
            s = "insert into tbl_cour values(null,'%s','%s','%s','%s','%s','%s',1)" % (
                email, fname, gdno, city, pin, phone)
            insert(s)
            flash('User Successfully Added')
            return redirect(url_for("admin.admincourier"))

    # table view
    data = {}
    q = "select * from tbl_cour"
    res = select(q)
    data['view'] = res

    # update details
    if 'action' in request.args:
        action = request.args['action']
        id = request.args['id']
    else:
        action = None

    if action == "update":
        q = "select * from tbl_cour where cour_id='%s'" % (id)
        res = select(q)
        data['up'] = res

    if 'update' in request.form:
        fname = request.form['fname']
        gdno = request.form['gdno']
        phone = request.form['phone']
        city = request.form['city']
        pin = request.form['pin']
        r = "update tbl_cour set cour_name='%s',cour_gno='%s',cour_city='%s',cour_pin='%s',cour_phone='%s'where cour_id='%s'" % (
            fname, gdno, phone, city, pin, id)
        update(r)
        return redirect(url_for('admin.admincourier'))

    # active inactive
    # if action == "inactive":
    #     q = "update tbl_cour set status='0' where cour_id='%s'" % (id)
    #     update(q)
    #     return redirect(url_for('admin.admincourier'))
    if action == "inactive":
        q = "SELECT * FROM `tbl_cart_master` INNER JOIN `tbl_payment` USING (cart_master_id) INNER JOIN `tbl_delivery` USING (cart_master_id) WHERE tbl_delivery.courier_id='%s' AND `tbl_cart_master`.c_status = 'dispatch'" % (
            id)
        print(q)
        exist = select(q)
        # cart_master_id=exist[0]['cart_master_id']
        # val = select(q)
        for w in exist:
            q = "update tbl_cart_master set c_status='paid' where cart_master_id='%s'" % (
                w['cart_master_id'])
            update(q)
            q = "delete from tbl_delivery where cart_master_id='%s'" % (
                w['cart_master_id'])
            delete(q)
            q = "update tbl_cour set status='0' where courier_id='%s'" % (id)
            update(q)
            q = "update tbl_login set status='0' where email='%s'" % (id)
            update(q)
        return redirect(url_for("admin.admincourier"))
    if action == "active":
        s = "update tbl_cour set status='1' where courier_id='%s'" % (id)
        update(s)
        s = "update tbl_login set status='1 where email='%s'" % (id)
        update(s)
        return redirect(url_for('admin.admincourier'))
    return render_template('admincourier.html', data=data)


@admin.route('/adminsales', methods=['post', 'get'])
def adminsales():
    # table view
    data = {}
    q = "SELECT * FROM tbl_cart_master INNER JOIN tbl_cart_child USING(cart_master_id)INNER JOIN tbl_item USING(item_id) INNER JOIN tbl_category USING(cat_id) INNER JOIN tbl_brand USING(brand_id)INNER JOIN tbl_payment USING(cart_master_id) INNER JOIN tbl_purchase_child USING(pur_child_id) INNER JOIN tbl_customer USING(cust_id) WHERE p_status=0"
    res = select(q)
    data['view'] = res
    return render_template('adminsales.html', data=data)


@admin.route('/adminsalesreport', methods=['post', 'get'])
def adminsalesreport():
    # table view
    data = {}
    q = "SELECT * FROM tbl_cart_master INNER JOIN tbl_cart_child USING(cart_master_id)INNER JOIN tbl_item USING(item_id) INNER JOIN tbl_category USING(cat_id) INNER JOIN tbl_brand USING(brand_id)INNER JOIN tbl_payment USING(cart_master_id) INNER JOIN tbl_purchase_child USING(pur_child_id) INNER JOIN tbl_customer USING(cust_id) WHERE p_status=0"
    res = select(q)
    data['view'] = res

    if 'dsch' in request.form:
        dsearch = request.form['dsearch']
        q = "SELECT * FROM tbl_cart_master om,tbl_cart_child od,tbl_item p,tbl_customer u,tbl_payment py WHERE om.cart_master_id=od.cart_master_id AND od.item_id=p.item_id AND om.cust_id=u.cust_id AND py.payment_date='%s'  GROUP BY om.cart_master_id " % (
            dsearch)
        res = select(q)
        data['res'] = select(q)

    if 'nsch' in request.form:
        search = "%"+request.form['search']+"%"
        q = "SELECT * FROM tbl_cart_master om,tbl_cart_child od,tbl_item p,tbl_customer u,tbl_payment py WHERE om.cart_master_id=od.cart_master_id AND od.item_id=p.item_id AND om.cust_id=u.cust_id AND cust_fname LIKE '%s'  GROUP BY om.cart_master_id" % (
            search)
        res = select(q)
        data['res'] = select(q)
    return render_template('adminsalesreport.html', data=data)


@admin.route('/salesreport')
def salesreport():
    data = {}
    q = "SELECT * FROM tbl_cart_master INNER JOIN tbl_cart_child USING(cart_master_id)INNER JOIN tbl_item USING(item_id) INNER JOIN tbl_category USING(cat_id) INNER JOIN tbl_brand USING(brand_id)INNER JOIN tbl_payment USING(cart_master_id) INNER JOIN tbl_purchase_child USING(pur_child_id) INNER JOIN tbl_customer USING(cust_id) WHERE p_status=0"
    res = select(q)
    data['view'] = res
    return render_template('salesreport.html', data=data)


@admin.route('/adminassign', methods=['get', 'post'])
def adminassign():
    data = {}
    q = "select * from tbl_cour where status='1'"
    data['courier_view'] = select(q)
    omid = request.args['omid']

    if 'submit' in request.form:
        delivery = request.form['delivery']
        q = "INSERT INTO tbl_delivery VALUES(null,'%s','%s',CURDATE(),'dispatch') " % (
            omid, delivery)
        insert(q)
        q = "UPDATE tbl_cart_master SET c_status ='dispatch' WHERE `cart_master_id`='%s'" % (
            omid)
        update(q)
        return redirect(url_for('admin.adminsales', omid=omid))

    return render_template('adminassigncourier.html', data=data)
