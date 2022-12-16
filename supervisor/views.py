from django.db import connection
from django.shortcuts import render, redirect
from supervisor.models import orderlist,product_master
import pyqrcode

from pyqrcode import QRCode

# Create your views here.

def supervisor_login(request):
    pickassign()

    return render(request, "supervisor_login.html")

def bincode(request):
    pickassign()
    orderlist_qr = []
    if request.session['role'] == '2':
        x = connection.cursor()
        x.execute("call distinct_orders_qr()")
        orderlist_qr = x.fetchall()
    return render(request,"bincode.html",{"list": orderlist_qr})

def orderdetails(request,odrid):
    pickassign()
    orderlist_qr = []
    prod_list = []
    date_show = None
    cus_name = None
    addr = None
    if request.session['role'] == '2':
        x = connection.cursor()
        x.execute("call distinct_orders_qr()")
        orderlist_qr = x.fetchall()
        k = connection.cursor()
        k.execute("call prod_details_by_oid('" + odrid + "')")
        prod_list = k.fetchall()
        t = orderlist.objects.filter(orderId=odrid)
        date_show = t[0].date
        cus_name = t[0].customer_name
        addr = t[0].address_city
    return render(request, "bincode.html", {"list": orderlist_qr, "prod_list": prod_list, "odrid": odrid, "date":date_show, "name": cus_name, "address": addr})

def qrgeneration(request):
    pickassign()
    if request.session['role'] == '2':
        oid = request.POST.get('oid')
        xyz = connection.cursor()
        xyz.execute("call update_qr('" + oid + "')")
        pros = connection.cursor()
        pros.execute("call fetch_pro_in_oid('" + oid + "')")
        prolist = pros.fetchall()
        for i in prolist:
            n = connection.cursor()     # qr generated orders-table: orderlist i[0] - product, i[1] - quantity, i[2] - row,i[3] - rack,i[4] - shelf
            n.execute("call check_prod_in_pickerlist('" + str(i[2]) + "')")
            pickerlist = n.fetchall()
            if len(pickerlist) > 0:
                flag = 0
                qty = 0
                pick_id = None
                pickerid = None
                prodid = None
                for j in pickerlist:
                    if j[2] == i[0]:    # picklist_assignment: j[0] - pickid, j[1] - picker_id,j[2] - product id
                        flag = 0        # , j[3] - quantity
                        prodid = j[2]
                        qty = j[3]
                        pick_id = j[0]
                        pickerid = j[1]
                        break
                    else:
                        pick_id = j[0]
                        pickerid = j[1]
                        flag = 1
                        pass
                if flag == 0:
                    tot_qty = int(i[1])+int(qty)
                    aj = connection.cursor()
                    aj.execute("call add_qty_to_pickerlist('" + str(pick_id) + "','" + str(pickerid) + "','" + str(prodid) + "','" + str(tot_qty) + "')")
                else:
                    tr = connection.cursor()
                    tr.execute("call insert_prod_live_pick('" + str(pick_id) + "','" + str(pickerid) + "','" + str(i[0]) + "','" + str(i[2]) + "','" + str(i[3]) + "','" + str(i[4]) + "','" + str(i[1]) + "')")
            else:
                k = connection.cursor()
                k.execute("call check_prod_in_picklist('" + str(i[2]) + "')")
                x = k.fetchall()
                if len(x) > 0:
                    flags = 0
                    quanty = 0
                    pick_ids = None
                    prodids = None
                    for m in x:
                        if m[1] == i[0]:    # picklist_pending: m[0] - pickid, m[1] - product id, m[2] - quantity
                            flags = 0
                            prodids = m[1]
                            quanty = m[2]
                            pick_ids = m[0]
                            break
                        else:
                            pick_ids = m[0]
                            flags = 1
                            pass
                    if flags == 0:
                        added_qty = int(quanty)+int(i[1])
                        print(added_qty)
                        kr = connection.cursor()
                        kr.execute("call add_qty_to_picklist_pending('" + str(pick_ids) + "','" + str(oid) + "','" + str(prodids) + "','" + str(added_qty) + "')")
                    else:
                        mn = connection.cursor()
                        mn.execute("call insert_prod_pending_pick('" + str(pick_ids) + "','" + str(oid) + "','" + str(i[0]) + "','" + str(i[2]) + "','" + str(i[3]) + "','" + str(i[4]) + "','" + str(i[1]) + "')")
                else:
                    gen_id = connection.cursor()
                    gen_id.execute("call pickid()")
                    r = connection.cursor()
                    r.execute("call fetch_id_for_pick()")
                    fetched_id = r.fetchall()
                    p = fetched_id[0][0]
                    l = "pick"
                    generated_id = l + str(p)
                    a = connection.cursor()
                    a.execute("call picklist_generate('" + str(oid) + "','" + str(i[0]) + "','" + str(i[2]) + "','" + str(i[3]) + "','" + str(i[4]) + "','" + str(i[1]) + "','" + generated_id + "')")
                    reset_id = connection.cursor()
                    reset_id.execute("call pickid1()")
        zy = connection.cursor()
        zy.execute("call change_order_status('" + str(oid) + "')")
        s = oid
        url = pyqrcode.create(s)
        url.svg("static\\myqr.svg", scale=8)
        url.png('static\\myqr.png', scale=6)
        return render(request, 'qrprint.html',{"oid":oid})
    else:
        return redirect('main_login:login')

def activity_status(request):
    pickassign()
    pickers = []
    orders = []
    picklist = []
    if request.session['role'] == '2':
        mn = connection.cursor()
        mn.execute("call distinct_orders()")
        orders = mn.fetchall()
        nm = connection.cursor()
        nm.execute("call distinct_pickers()")
        pickers = nm.fetchall()
        mm = connection.cursor()
        mm.execute("call distinct_picklist()")
        picklist = mm.fetchall()
    else:
        return redirect('main_login:login')
    return render(request,"activity_status.html",{"orders":orders,"pickers":pickers,"picklist":picklist})

def orderwise_pl(request,odrid):
    pickassign()
    pickers = []
    orders = []
    picklist = []
    products = []
    if request.session['role'] == '2':
        mn = connection.cursor()
        mn.execute("call distinct_orders()")
        orders = mn.fetchall()
        nm = connection.cursor()
        nm.execute("call distinct_pickers()")
        pickers = nm.fetchall()
        mm = connection.cursor()
        mm.execute("call distinct_picklist()")
        picklist = mm.fetchall()
        nn = connection.cursor()
        nn.execute("call prod_details_by_oid('" + odrid + "')")
        products = nn.fetchall()
    else:
        return redirect('main_login:login')

    return render(request, "activity_status.html", {"orders": orders, "pickers": pickers, "picklist": picklist,"products":products})

def pickerwise_pl(request,pickerid):
    pickassign()
    pickers = []
    orders = []
    picklist = []
    products = []
    if request.session['role'] == '2':
        mn = connection.cursor()
        mn.execute("call distinct_orders()")
        orders = mn.fetchall()
        nm = connection.cursor()
        nm.execute("call distinct_pickers()")
        pickers = nm.fetchall()
        mm = connection.cursor()
        mm.execute("call distinct_picklist()")
        picklist = mm.fetchall()
        nn = connection.cursor()
        nn.execute("call prod_details_by_pickerid('" + str(pickerid) + "')")
        products = nn.fetchall()
    else:
        return redirect('main_login:login')
    return render(request, "pickerwise_list.html",
                  {"orders": orders, "pickers": pickers, "picklist": picklist, "products": products})

def pickwise_pl(request,pickid):
    pickassign()
    pickers = []
    orders = []
    picklist = []
    products = []
    if request.session['role'] == '2':
        mn = connection.cursor()
        mn.execute("call distinct_orders()")
        orders = mn.fetchall()
        nm = connection.cursor()
        nm.execute("call distinct_pickers()")
        pickers = nm.fetchall()
        mm = connection.cursor()
        mm.execute("call distinct_picklist()")
        picklist = mm.fetchall()
        nn = connection.cursor()
        nn.execute("call prod_details_by_pickid('" + str(pickid) + "')")
        products = nn.fetchall()
    else:
        return redirect('main_login:login')

    return render(request, "picklistwise_list.html",
                  {"orders": orders, "pickers": pickers, "picklist": picklist, "products": products})


def planogram(request):
    pickassign()
    prod_list = []
    if request.session['role'] == '2':
        aa = connection.cursor()
        aa.execute("call planogram()")
        prod_list = aa.fetchall()
    else:
        return redirect('main_login:login')
    return render(request,"planogram.html",{"prod_list":prod_list})

def addpro(request):
    pickassign()
    if request.session['role'] == '2':
        if request.method == 'POST':
            proname = request.POST.get("prod")
            batch = request.POST.get("batch")
            qty = request.POST.get("qty")
            row = request.POST.get("row")
            rack = request.POST.get("rack")
            shelf = request.POST.get("shelf")
            sv = product_master(product=proname, Batch=batch, row=row, rack=rack, shelf=shelf, stock_qty=qty)
            sv.save()
            return redirect('supervisor:planogram')
    else:
        return redirect('main_login:login')
    return render(request,"planogram.html")

def picklist_reassign(request):
    pickassign()
    drp_inactive = []
    drp_active = []
    if request.session['role'] == '2':
        ab = connection.cursor()
        ab.execute("call active_picker()")
        drp_active = ab.fetchall()
        ba = connection.cursor()
        ba.execute("call free_picker()")
        drp_inactive = ba.fetchall()
    else:
        return redirect('main_login:login')
    return render(request,"pick_reassign.html",{"drp_inactive":drp_inactive,"drp_active":drp_active})

def reassign(request):
    pickassign()
    if request.session['role'] == '2':
        if request.method == 'POST':
            free = request.POST.get('inactive')
            working = request.POST.get('active')
            bb = connection.cursor()
            bb.execute("call change_picker('" + str(working) + "','" + str(free) + "')")
            bc = connection.cursor()
            bc.execute("call lets_work('" + str(free) + "')")
            cb = connection.cursor()
            cb.execute("call im_injured('" + str(working) + "')")
            return redirect('supervisor:picklist_reassign')
        else:
            return redirect('main_login:login')

def logout(request):
    pickassign()
    if request.session['role'] == '2':
        userid = request.session['user_id']
        cc = connection.cursor()
        cc.execute("call logout('" + str(userid) + "')")
        try:
            del request.session['user']
            del request.session['role']
        except KeyError:
            return redirect('main_login:login')
        return redirect('main_login:login')









def pickassign():
    try:
        a = connection.cursor()
        a.execute("call picker_for_assignment()")
        free_pickers = a.fetchall()
        if len(free_pickers) > 0:
            picker_id = free_pickers[0][0]
            b = connection.cursor()
            b.execute("call distinct_pending_picks()")
            k = b.fetchall()
            pickid = k[0][0]
            c = connection.cursor()
            c.execute("call pending_picks('" + str(pickid) + "')")
            pending_picklist = c.fetchall()
            r = 9       #     9 for not accepting picklist
            try:
                for i in pending_picklist:
                    aa = connection.cursor()
                    aa.execute("call picklist_assignment('" + str(pickid) + "','" + str(picker_id) + "','" + str(i[1]) + "','" + str(i[2]) + "','" + str(i[3]) + "','" + str(i[4]) + "','" + str(i[5]) + "','" + str(r) + "')")
                ab = connection.cursor()
                ab.execute("call change_pending_status('" + str(pickid) + "')")
                ba = connection.cursor()
                ba.execute("call assigned_user_update('" + str(picker_id) + "')")
            except:
                pass
        else:
            pass
    except:
        pass