from django.contrib import messages
from django.db import connection
from django.shortcuts import render, redirect
from supervisor.models import orderlist


# Create your views here.

def picker_login(request):
    pickassign()
    return render(request,"picker_login.html")

picqrresult = []
xy = None
chumma = []

def picker_view(request):
    pickassign()
    uid = request.session['user_id']
    a = connection.cursor()
    a.execute("call show_picks('" + str(uid) + "')")
    pick = a.fetchall()
    return render(request, "picker_pickerview.html",{"pick":pick})

def pickqr(request,proid):
    pickassign()
    chumma.append(str(proid))
    return render(request, "pickqr.html")


def qrvaluefetch(request):
    pickassign()
    try:
        if 'user' in request.session:
            if request.method == 'POST':
                picqrresult.append(str(request.POST.get('data')))
                print(picqrresult)
            return render(request,"pickqr.html")
        else:
            return redirect('/')
    except:
        return redirect('/')

def test(request):
    try:
        flag = None
        if 'user' in request.session:
            if request.method == 'POST':
                xy = str(picqrresult[-1])
                print(chumma[-1])
                print(xy)
                if chumma[-1] == xy:
                    flag = 1
                else:
                    flag = 0
                if flag == 1:
                    messages.success(request,"Item matched")
                    picqrresult.clear()
                    chumma.clear()
                    uid = request.session['user_id']
                    ad = connection.cursor()
                    ad.execute("call item_picked('" + str(uid) + "','" + str(xy) + "')")

                else:
                    messages.error(request,"Item did not match")
                    pass


                return redirect('picker:picker_view')
        else:
            pickassign()
            return redirect('/')
    except:
        pickassign()
        return redirect('/')


def picker_dashboard(request):
    pickassign()
    uid = request.session['user_id']
    a = connection.cursor()
    a.execute("call pick_in_que('" + str(uid) + "')")
    pick_que = a.fetchall()
    return render(request,"picker_dashboard.html",{"pick_que":pick_que})

def start_pick(request,pickid):
    pickassign()
    aab = connection.cursor()
    aab.execute("call start_pick('" + str(pickid) + "')")
    return redirect('picker:picker_dashboard')

def bincode(request):
    pickassign()
    a = connection.cursor()
    a.execute("call distinct_orders_drop()")
    olist = a.fetchall()
    return render(request,"picker_binscan.html",{"list":olist})

def orderdetails(request,oid):
    pickassign()
    orderlist_qr = []
    prod_list = []
    date_show = None
    cus_name = None
    addr = None
    if request.session['role'] == '3':
        x = connection.cursor()
        x.execute("call distinct_orders_drop()")
        orderlist_qr = x.fetchall()
        t = orderlist.objects.filter(orderId=oid)
        k = connection.cursor()
        k.execute("call orderwise_products_for_drop('" + str(oid) + "')")
        prod_list = k.fetchall()
        date_show = t[0].date
        cus_name = t[0].customer_name
        addr = t[0].address_city
    return render(request, "picker_binscan.html", {"list": orderlist_qr, "prod_list": prod_list, "odrid": oid, "date":date_show, "name": cus_name, "address": addr})


binqrresult = []

def qrverify(request):
    pickassign()
    oid = request.POST.get("oid")
    return render(request,"picker_qr_verify.html")

def binqrvalue(request):
    pickassign()
    if request.method == 'POST':
        binqrresult.append(str(request.POST.get('data')))
        print(binqrresult)
        request.session['oid'] = binqrresult[-1]
        print(request.session['oid'])
    return render(request,"picker_qr_verify.html")

def qrvalidation(request):
    pickassign()
    prod_show = []
    oid = request.session['oid']
    flag = 0
    try:
        #oid = binqrresult[-1]
        uid = request.session['user_id']
        a = connection.cursor()
        a.execute("call pick_drop('" + str(uid) + "','" + str(oid) + "')")
        prod_show = a.fetchall()
        if len(prod_show) == 0:
            flag = 1
            n = connection.cursor()
            n.execute("call pick_increment('" + str(uid) + "')")
    except:
        pass
    return render(request,"picker_barscan.html",{"flag":flag,"prod_show":prod_show,"oid":oid})



def pickdrop(request,proid,oqty,pqty,pname,oid):
    pickassign()
    request.session['prodidx'] = proid
    request.session['order_qtyx'] = oqty
    request.session['oid'] = oid
    pickedqty = pqty
    request.session['pronamex'] = pname
    uid = request.session['user_id']
    x = []
    try:
        x.append(request.POST.get('data'))
        g = x[-1]
        if int(g) == proid:
            pickedqty = int(pickedqty)-1
            b = connection.cursor()
            b.execute("call reduce_picked_qty('" + str(uid) + "','" + str(proid) + "','" + str(pickedqty) + "')")
            if pickedqty == 0 or oqty == 0:
                k = connection.cursor()
                k.execute("call finish_prod('" + str(uid) + "','" + str(proid) + "')")
            request.session['order_qtyx'] = int(oqty)-1
            return render(request, "picker_pickdrop.html",
                          {"prodid": request.session['prodidx'], "odqty": request.session['order_qtyx'],
                           "pro_qty": pickedqty, "proname": request.session['pronamex']})

    except:
        pass
        return render(request, "picker_pickdrop.html",
                  {"prodid": request.session['prodidx'], "odqty": request.session['order_qtyx'], "pro_qty": pqty, "proname": request.session['pronamex']})


    return render(request,"picker_pickdrop.html",{"prodid":request.session['prodidx'],"odqty":request.session['order_qtyx'],"pro_qty":pickedqty,"proname":request.session['pronamex']})








def logout(request):
    pickassign()
    userid = request.session['user_id']
    cc = connection.cursor()
    cc.execute("call logout('" + str(userid) + "')")
    try:
        del request.session['user']
        del request.session['role']
        del request.session['user_id']
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
