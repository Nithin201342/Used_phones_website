from flask import *
from database import *
import uuid

staff = Blueprint('staff', __name__)


@staff.route('/staffhome')
def staffhome():
    return render_template('staffhome.html')


@staff.route('/staffcustomer', methods=['post', 'get'])
def staffcustomer():
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
        return redirect(url_for('staff.staffcustomer'))
    if action == "active":
        s = "update tbl_customer set status='1' where cust_id='%s'" % (cid)
        update(s)
        return redirect(url_for('staff.staffcustomer'))
    return render_template('staffcustomer.html', data=data)


@staff.route('/staffcategory', methods=['post', 'get'])
def staffcategory():
    # form
    if 'submit' in request.form:
        cate = request.form['cate']
        desc = request.form['desc']
        r = "insert into tbl_category values(null,'%s','%s',1)" % (cate, desc)
        insert(r)

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
        return redirect(url_for('staff.staffcategory'))

    # active inactive
    if action == "inactive":
        q = "update tbl_category set status='0' where cat_id='%s'" % (id)
        update(q)
        return redirect(url_for('staff.staffcategory'))
    if action == "active":
        s = "update tbl_category set status='1' where cat_id='%s'" % (id)
        update(s)
        return redirect(url_for('staff.staffcategory'))
    return render_template('staffcategory.html', data=data)


@staff.route('/staffbrand', methods=['post', 'get'])
def staffbrand():
    # form
    if 'submit' in request.form:
        bname = request.form['bname']
        desc = request.form['desc']
        r = "insert into tbl_brand values(null,'%s','%s',1)" % (bname, desc)
        insert(r)

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
        return redirect(url_for('staff.staffbrand'))

    # active inactive
    if action == "inactive":
        q = "update tbl_brand set status='0' where brand_id='%s'" % (id)
        update(q)
        return redirect(url_for('staff.staffbrand'))
    if action == "active":
        s = "update tbl_brand set status='1' where brand_id='%s'" % (id)
        update(s)
        return redirect(url_for('staff.staffbrand'))

    return render_template('staffbrand.html', data=data)


@staff.route('/staffproduct', methods=['post', 'get'])
def staffproduct():
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
        r = "insert into tbl_item values(null,'%s','%s','%s',1)" % (
            cat, brand, name)
        insert(r)
        return redirect(url_for('staff.staffproduct'))

    # table view
    q = "select * from ((tbl_item INNER JOIN tbl_category ON tbl_item.cat_id=tbl_category.cat_id)INNER JOIN tbl_brand ON tbl_item.brand_id=tbl_brand.brand_id)"
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
        return redirect(url_for('staff.staffproduct'))

    # active inactive
    if action == "inactive":
        q = "update tbl_item set status='0' where item_id='%s'" % (id)
        update(q)
        return redirect(url_for('staff.staffproduct'))
    if action == "active":
        s = "update tbl_item set status='1' where item_id='%s'" % (id)
        update(s)
        return redirect(url_for('staff.staffproduct'))

    return render_template('staffproduct.html', data=data)


@staff.route('/staffpurchase', methods=['post', 'get'])
def staffpurchase():
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
            q = "insert into tbl_purchase_master values(null,'%s','%s',curdate(),'%s','pending')" % (
                session['sid'], cid, cprice)
            pmid = insert(q)
            q = "insert into tbl_purchase_child values(null,'%s','%s','%s','%s','%s','%s','%s','1')" % (
                pmid, product, desc, profit, cprice, newsellp, path)
            insert(q)
            flash("Added To Purchase List")
            return redirect(url_for('staff.staffpurchase'))

    if 'id' in request.args:
        id = request.args['id']
        q = "update tbl_purchase_master set status='paid' where pur_master_id='%s'" % (
            id)
        update(q)
        flash("Purchase Successfull")
        return redirect(url_for('staff.staffpurchase'))

    return render_template('staffpurchase.html', data=data)
