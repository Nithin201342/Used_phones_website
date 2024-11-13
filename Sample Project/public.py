from flask import Flask, Blueprint, render_template, request, redirect, url_for, flash, session
from database import *

public = Blueprint('public', __name__)


@public.route('/')
def home():
    return render_template('home.html')


@public.route('/login', methods=['get', 'post'])
def login():
    if 'submit' in request.form:
        email = request.form['email']
        password = request.form['pass']
        print("email="+email, "password="+password)
        q = "select * from tbl_login where email='%s' and password='%s'and status='1'" % (
            email, password)
        res = select(q)
        if res:
            if res[0]['usertype'] == "admin":
                session['email'] = res[0]['email']
                email = session['email']
                return redirect(url_for("admin.adminhome"))
            elif res[0]['usertype'] == "staff":
                q = "select * from tbl_staff where email='%s'" % (email)
                val = select(q)
                session['sid'] = val[0]['staff_id']
                sid = session['sid']

                session['name'] = val[0]['staff_fname']
                name = session['name']
                return redirect(url_for("staff.staffhome"))
            elif res[0]['usertype'] == "customer":
                q = "select * from tbl_customer where email='%s'" % (email)
                val = select(q)
                session['cid'] = val[0]['cust_id']
                cid = session['cid']

                session['name'] = val[0]['cust_fname']
                name = session['name']
                return redirect(url_for("customer.customerhome"))
            elif res[0]['usertype']  == "courier":
                q = "select * from tbl_cour where email='%s'" % (email)
                val = select(q)
                session['courid'] = val[0]['courier_id']
                courid = session['courid']
                
                session['name'] = val[0]['cour_name']
                name = session['name']
                return redirect(url_for("courier.courierhome"))

        else:
            flash("Invalid Username or Password!")
            return redirect(url_for('public.login'))

    return render_template('login.html')


@public.route('/register', methods=['get', 'post'])
def register():
    if 'submit' in request.form:
        email = request.form['email']
        fname = request.form['fname']
        lname = request.form['lname']
        city = request.form['city']
        pin = request.form['pin']
        phone = request.form['phone']
        password = request.form['pass']
        q = "select * from tbl_login where email='%s' " % (email)
        val = select(q)
        if val:
            flash('User Already Exists')
        else:
            r = "insert into tbl_login values('%s','%s','customer',1)" % (
                email, password)
            insert(r)
            s = "insert into tbl_customer values(null,'%s','%s','%s','%s','%s','%s',1)" % (
                email, fname, lname, city, pin, phone)
            insert(s)
            flash('Registered Successfully')
    return render_template('register.html')


@public.route('/product')
def product():
    #product view
    data = {}
    q = "SELECT * FROM tbl_purchase_master INNER JOIN tbl_purchase_child ON tbl_purchase_master.`pur_master_id`=tbl_purchase_child.`pur_master_id` INNER JOIN tbl_item ON tbl_purchase_child.item_id=tbl_item.item_id INNER JOIN tbl_category USING (cat_id) INNER JOIN tbl_brand USING (brand_id) WHERE tbl_purchase_master.status='paid' AND tbl_category.status=1 AND tbl_brand.status=1 AND p_status='1'"
    res = select(q)
    data['productsearch'] = res
    return render_template('product.html', data=data)
