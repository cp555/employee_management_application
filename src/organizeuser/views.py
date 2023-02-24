from django.shortcuts import render
import os
from django.shortcuts import render, redirect, HttpResponse
from importlib import import_module
from training.db import *
from time import gmtime, strftime, localtime


# def ou_page(request):
# 	## overall page
# 	context = {}
# 	HTML = "organizeuser/list.html"
# 	return render(request,HTML,context)


def account_page(request):
	if "user" not in request.session:
		return redirect("login")
	class_name = "Account"
	urls = request.build_absolute_uri()
	mark_index = urls.find('?')
	dictionary = {}
	if mark_index != -1:
		after = urls.split("?")[-1]
		from_get = after.split("&")
		for pairs in from_get:
			if "=" not in pairs:
				continue
			key = pairs.split("=")[0]
			value = pairs.split("=")[1]
			dictionary[key] = value    
	for key,value in request.POST.items():
		dictionary[key] = value
	print("dictionary is:      " + str(dictionary))
	method = dictionary["$ACTION"]
	obj = import_module('organizeuser.modules.account')
	c = getattr(obj,class_name)
	obj = c(request,dictionary)
	mtd = getattr(obj,method)
	request,HTML,context = mtd()
	if HTML == None:
		return redirect('account.do?$ACTION=list')
	if HTML == "home":
		return render(request,"training/home.html",{})
	elif HTML == "XHR":
		return context
	return render(request,HTML,context)

def resource_access(rolecode,resourcecode):
	sql = "Select * from ou_resource where resourcecode = %s"
	target = fetch_one(sql,(resourcecode))
	access_type = target["accesstype"]
	if access_type == "L":
		if rolecode == "anonymous":
			return "N"
		else :
			return "Y"
	elif access_type == "A":
		return "Y"
	else:
		sql2 = "Select * from ou_roleresource where rolecode = %s && resourcecode = %s"
		target2 = fetch_one(sql2,(rolecode,resourcecode))
		return target2["rightflag"]

######################################################### role resource roleresource######################################################
def userrole_view(request):
	if "user" not in request.session:
		return redirect("login")
	return _render(request, "Userrole", 'organizeuser.modules.userrole')

def role_view(request):
	if "user" not in request.session:
		return redirect("login")
	return _render(request, "Role", 'organizeuser.modules.role')

def resource_view(request):
	if "user" not in request.session:
		return redirect("login")
	return _render(request, "Resource", 'organizeuser.modules.resource')
	
def roleresource_view(request):
	if "user" not in request.session:
		return redirect("login")
	return _render(request, "Roleresource", 'organizeuser.modules.roleresource')

def _render(request, class_name, module_name):
    url = request.build_absolute_uri() # gets the url as a string from request
    info = {}

    # stores the data got from request.POST in info
    for key, value in request.POST.items():
        v = request.POST.getlist(key)
        if v is not None:
            s = ""
            for item in v:
                if s != "":
                    s += ','
                s += item
            info[key] = s
            continue
        info[key] = value

    # if url contains '?'
    if url.find('?') != -1:
        action = url.split("?")[-1]
        action = action.split("&")
        for pairs in action:
            if "=" not in pairs:
                continue
            data = pairs.split("=")
            key = data[0]
            value = data[1]
            info[key] = value  

    if "$ACTION" in info:
        method_name = info["$ACTION"]
    else:
        method_name = "list"

    c = getattr(import_module(module_name), class_name)
    obj = c(info)
    method = getattr(obj, method_name)
    html, context = method()
    if html is not None: 
        return render(request, html, context)
    return redirect(class_name.lower() + ".do?$ACTION=list")

#################################################################  dept  ######################################################################

def dept_view(request):
	if "user" not in request.session:
		return redirect("login")
	urls = request.build_absolute_uri()
	mark_index = urls.find('?')
	dictionary = {}
	if mark_index != -1:
		after = urls.split("?")[-1]
		from_get = after.split("&")
		for pairs in from_get:
			if "=" not in pairs:
				continue
			key = pairs.split("=")[0]
			value = pairs.split("=")[1]
			dictionary[key] = value    
	for key,value in request.POST.items():
		dictionary[key] = value
	
	action = dictionary["$ACTION"]

	clsname = 'Dept'
	method = action

	obj = import_module('organizeuser.modules.dept')
	c = getattr(obj,clsname)
	obj = c(request, dictionary)
	mtd = getattr(obj,method)
	request,HTML,context = mtd()

	if HTML == None:
		return redirect('/ou/dept.do?$ACTION=list&refresh=yes&pathcode='+context)

	return render(request,HTML,context)

# #########################################################################  set up ##############################################################
def setup(request):
	## check whether set up 
	check = "Select * from ou_role"
	checkset = fetch_one(check,())
	print(checkset)
	if checkset != None:
		print("already set up")
		context = {"whetherSuccess" : "done"}
		HTML = "organizeuser/setup.html"
		return render(request,HTML,context)
	try:
		sql = "Insert Into ou_account (id,usercode,username,passwd,email,userstatus,deptcode,registeredtime) values (%s,%s,%s,%s,%s,%s,%s,%s)"
		usercode = "admin"
		username = "Administrator"
		passwd = "21232f297a57a5a743894a0e4a801fc3"
		email = "admin@qq.com"
		userstatus = "A"
		deptcode = "Backend"
		registertime = strftime("%Y-%m-%d %H:%M:%S",localtime())
		print(registertime)
		insert(sql,(str(1),usercode,username,passwd,email,userstatus,deptcode,registertime))

		sql2 = "Insert Into ou_role (id,rolecode,rolename) values (%s,%s,%s)"
		insert(sql2,(str(1),"administrator","adm"))
		insert(sql2,(str(2),"normaluser","user"))
		insert(sql2,(str(3),"anonymous","anonymous"))

		sql3 = "Insert Into ou_dept (id,deptcode,pathcode,deptname,deptstatus) values (%s,%s,%s,%s,%s)"
		ids = [1,2,3,4,5]
		deptcode = ["Backend","BackendOne","Frontend","FrontendOne","Testing"]
		pathcode = ["default/Backend","default/Backend/BackendOne","default/Frontend","default/Frontend/FrontendOne","default/Testing"]
		deptname = ["Backend","Backend One","Frontend","Frontend One","Testing"]
		deptstatus = "A"
		for j in range(5):
			insert(sql3,(str(ids[j]),deptcode[j],pathcode[j],deptname[j],deptstatus))

		sql4 = "Insert Into ou_userrole (id,usercode,rolecode) values (%s,%s,%s)"
		insert(sql4,(str(1),"admin","administrator"))
	

		sql5 = "Insert Into ou_resource (id,resourcecode,resourcename,sysname,modelname,actionname,accesstype) values (%s,%s,%s,%s,%s,%s,%s)"
		insert(sql5,(str(1),"training/home/sqlbutton","training/home/sqlbutton","training","home","sqlbutton","A"))
		insert(sql5,(str(2),"training/home/statbutton","training/home/statbutton","training","home","statbutton","A"))
		insert(sql5,(str(3),"training/sql/create","training/sql/create","training","sql","create","R"))
		insert(sql5,(str(4),"training/sql/import","training/sql/import","training","sql","import","R"))
		insert(sql5,(str(5),"training/sql/detail","training/sql/detail","training","sql","detail","R"))
		insert(sql5,(str(6),"training/sql/delete","training/sql/delete","training","sql","delete","R"))
		insert(sql5,(str(7),"training/sql/update","training/sql/update","training","sql","update","R"))

		sql6 = "Insert Into ou_roleresource (id,rolecode,resourcecode,rightflag) values (%s,%s,%s,%s)"
		insert(sql6,(str(1),"administrator","training/sql/create","Y"))
		insert(sql6,(str(2),"normaluser","training/sql/create","N"))
		insert(sql6,(str(3),"anonymous","training/sql/create","N"))
		insert(sql6,(str(4),"administrator","training/sql/import","Y"))
		insert(sql6,(str(5),"normaluser","training/sql/import","N"))
		insert(sql6,(str(6),"anonymous","training/sql/import","N"))
		insert(sql6,(str(7),"administrator","training/sql/detail","Y"))
		insert(sql6,(str(8),"normaluser","training/sql/detail","Y"))
		insert(sql6,(str(9),"anonymous","training/sql/detail","Y"))
		insert(sql6,(str(10),"administrator","training/sql/delete","Y"))
		insert(sql6,(str(11),"normaluser","training/sql/delete","N"))
		insert(sql6,(str(12),"anonymous","training/sql/delete","N"))
		insert(sql6,(str(13),"administrator","training/sql/update","Y"))
		insert(sql6,(str(14),"normaluser","training/sql/update","N"))
		insert(sql6,(str(15),"anonymous","training/sql/update","N"))
		context = {"whetherSuccess" : True}

	except Exception as e:
		print(e)
		context = {"whetherSuccess" : False}
	finally:
		HTML = "organizeuser/setup.html"
		return render(request,HTML,context)


