from operator import ge
from model import EarthJoyModel
from flask import Flask,render_template,request,session,redirect,url_for,jsonify
from views import *
from flask_mail import Mail, Message
from flask_socketio import SocketIO, join_room, leave_room
import paypalrestsdk


app = Flask(__name__)
app.config.from_object("config")
socketio = SocketIO(app)
app.config['DEBUG'] = True
app.config['TESTING'] = False
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
#app.config['MAIL_DEBUG'] = True                              # default app.debug
app.config['MAIL_USERNAME'] = 'imhraza023@gmail.com'
app.config['MAIL_PASSWORD'] = 'qxwsafbsctqznzix'
app.config['MAIL_DEFAULT_SENDER'] = ('Earth Joy','imhraza023@gmail.com')
app.config['MAIL_MAX_EMAILS'] = None
#app.config['MAIL_SUPPRESS_SEND'] = False                     # default app.testing
app.config['MAIL_ASCII_ATTACHMENTS'] = False

mail = Mail(app)

def getModel():
    return EarthJoyModel(app.config["HOST"],app.config["USER"],app.config["PASSWORD"], app.config["DATABASE"])

MODEL = getModel()

paypalrestsdk.configure({
  "mode": "sandbox", # sandbox or live
  "client_id": "Aaav4BrNVhIpBhgxcLTE01WAP8nsvTPwULzt6vlReaUM-XZrnPqJYEsendGOyK-G8znq5aNIXghfb56-",
  "client_secret": "EJGdXcEzFjMQmTYk0PAteA9QhzjVn2-LJk1IbJM3bDYU3NMqlSZdr6Wdtrqs5o1QbFO0vmzWnD9xg3Qa" })

@app.route('/')
def homepage():
    elec=MODEL.getElectronics(1,0)
    hap=MODEL.getHomeAppliances(1,0)
    hlth=MODEL.getHealth(1,0)
    grs=MODEL.getGroceries(1,0)
    fashon=MODEL.getFashon(1,0)
    am=MODEL.getAutomobile(1,0)
    email = session.get("bemail")
    cid =  MODEL.getCartId(email)
    cdata = MODEL.getCartProduct(cid)
    return render_template('buyers/index.html', elec=elec,hap=hap, hlth=hlth,grs=grs,fashon=fashon,am=am,cdata=cdata)

@app.route('/cart')
def cart():
    email = session.get("bemail")
    if email == None:
        return render_template("buyers/register.html", error=True , errormsg="You must have to sign up first.")
    else:
        cid =  MODEL.getCartId(email) 
        data = MODEL.getCartProduct(cid)
        cdata=data
        gTotal = MODEL.getSumPrice(cid)
        return render_template('buyers/cart.html',data=data,cdata=cdata,gTotal=gTotal)
    
@app.route("/addToCart" , methods=["GET"])
def addToCart():
    email = session.get("bemail")
    cid =  MODEL.getCartId(email)
    pid = int(request.args.get("data").rsplit(",")[0])
    pqnt = int(request.args.get("data").rsplit(",")[1])
    result=MODEL.addToCart(cid,pid,pqnt)
    MODEL.deleteFromStock(pid,pqnt)
    return result

@app.route("/deleteFromCart" , methods=["GET"])
def deleteFromCart():
    cpid  = int(request.args.get("data").rsplit(",")[0])
    pid = int(request.args.get("data").rsplit(",")[1])
    pqnt = int(request.args.get("data").rsplit(",")[2])
    result=MODEL.deleteFromCart(cpid)
    email = session.get("bemail")
    cid =  MODEL.getCartId(email)
    data = MODEL.getCartProduct(cid)
    MODEL.addToStock(pid,pqnt)
    return jsonify(data)


@app.route('/checkout')
def checkout():
    email = session.get("bemail")
    cid =  MODEL.getCartId(email)
    cdata = MODEL.getCartProduct(cid)
    gTotal = MODEL.getSumPrice(cid)
    return render_template('buyers/checkout.html',cdata=cdata,gTotal=gTotal)



@app.route("/signup")
def signupform():
    email = session.get("bemail")
    cid =  MODEL.getCartId(email)
    cdata = MODEL.getCartProduct(cid)
    categories = MODEL.getCategories()
    return render_template("buyers/register.html",cdata=cdata,categories=categories)

@app.route("/registerBuyer", methods=["POST"])
def signup():
    email = request.form["email"]
    pswrd = request.form["pwd"]
    name = request.form["name"]
    gender = request.form["gender"]
    dob = request.form["dob"]
    #request.files
    image = request.files["image"]
    newFileName = str(int(MODEL.getBuyerMaxID())+1)+"."+ image.filename.split('.')[1]
    image.save(f"static\\buyerImages\\{newFileName}")
    buy=Buyers(email,pswrd,name,gender,dob,newFileName)
    exist=MODEL.checkUserExist(buy)
    if not exist:
        insert=MODEL.insertBuyer(buy)
        if insert:
            MODEL.createCart(MODEL.getBuyerMaxID())
            email = session.get("bemail")
            cid =  MODEL.getCartId(email)
            cdata = MODEL.getCartProduct(cid)
            return render_template("buyers/login.html",cdata=cdata)
        else:
            return render_template("buyers/register.html", error=True , errormsg="Some error in signup")
    else:
        return render_template("buyers/register.html",error=True,errormsg="Email already exist")

@app.route("/about-us")
def aboutus():
    email = session.get("bemail")
    cid =  MODEL.getCartId(email)
    cdata = MODEL.getCartProduct(cid)
    return render_template("buyers/aboutus.html",cdata=cdata)

@app.route("/contactus", methods=["POST"])
def contact():
    email = session.get("bemail")
    cid =  MODEL.getCartId(email)
    cdata = MODEL.getCartProduct(cid)
    name = request.form["name"]
    email = request.form["email"]
    subject = request.form["subject"]
    message = request.form["message"]
    msg = Message(subject, sender =  (name, 'imhraza023@gmail.com') , recipients = ['imhraza023@gmail.com'])
    msg.html = "<h3>"+message+"<h3>"
    mail.send(msg)
    return render_template("buyers/contactus2.html",cdata=cdata,messsage="Your Message has been sent!")


@app.route("/faq")
def faq():
    email = session.get("bemail")
    cid =  MODEL.getCartId(email)
    cdata = MODEL.getCartProduct(cid)
    return render_template("buyers/faq.html",cdata=cdata)

@app.route("/contact-us")
def contactus():
    email = session.get("bemail")
    cid =  MODEL.getCartId(email)
    cdata = MODEL.getCartProduct(cid)
    return render_template("buyers/contactus.html",cdata=cdata)
    
@app.route("/payments", methods=["POST"])
def payments():
    email = session.get("bemail")
    if email !=None:
        cid =  MODEL.getCartId(email)
        cdata = MODEL.getCartProduct(cid)
        set = MODEL.updateCheckStatus(cid)
        pemail = request.form["email"]
        date = request.form["date"]
        country = request.form["country"]
        zipcode = request.form["zipcode"]
        state = request.form["state"]
        address = request.form["address"]
        city = request.form["city"]
        deliveryStatus="Order Confirmed"
        bAddress = city+','+zipcode+','+address+','+state+','+country
        insert=MODEL.insertCheckout(cid,date,bAddress,deliveryStatus)
        if insert:
            #MODEL.deleteAllFromCart(cid)
            return render_template("buyers/payment.html",cdata=cdata,msg="Your order has been placed!")
        else:
            return render_template("buyers/payment.html",cdata=cdata,msg="There was an error in placing your order!")
    else:
        elec=MODEL.getElectronics(1,0)
        hap=MODEL.getHomeAppliances(1,0)
        hlth=MODEL.getHealth(1,0)
        grs=MODEL.getGroceries(1,0)
        fashon=MODEL.getFashon(1,0)
        am=MODEL.getAutomobile(1,0)
        email = session.get("bemail")
        cid =  MODEL.getCartId(email)
        cdata = MODEL.getCartProduct(cid)
        return render_template("buyers/index.html" , log= "You must have to login first.", email=email,elec=elec,hap=hap, hlth=hlth,grs=grs,fashon=fashon,am=am,cdata=cdata)
    
@app.route('/registerSeller',methods=["post"])
def registerSeller():
    email = request.form["email"]
    pswrd = request.form["pwd"]
    name = request.form["name"]
    gender = request.form["gender"]
    category = request.form["category"]
    image = request.files["image"]
    address=request.form["address"]
    newFileName = str(int(MODEL.getSellerMaxID())+1)+"."+ image.filename.split('.')[1]
    image.save(f"static\\sellerImages\\{newFileName}")
    MODEL.insertSeller(name,email,pswrd,gender,address,category,newFileName)
    elec=MODEL.getElectronics(1,0)
    hap=MODEL.getHomeAppliances(1,0)
    hlth=MODEL.getHealth(1,0)
    grs=MODEL.getGroceries(1,0)
    fashon=MODEL.getFashon(1,0)
    am=MODEL.getAutomobile(1,0)
    email = session.get("bemail")
    cid =  MODEL.getCartId(email)
    cdata = MODEL.getCartProduct(cid)
    return render_template("buyers/index.html" , log= "Your request to join Earthjoy as a seller has been submitted. You will get a confirmation email in a while.", email=email,elec=elec,hap=hap, hlth=hlth,grs=grs,fashon=fashon,am=am,cdata=cdata)
    
@app.route("/signin")
def signin():
    email = session.get("bemail")
    cid =  MODEL.getCartId(email)
    cdata = MODEL.getCartProduct(cid)
    return render_template("buyers/login.html",cdata=cdata)


@app.route("/buyerEnd", methods=["POST"])
def buyerEnd():
    email=request.form["email"]
    pwd=request.form["pwd"]
    user=User(email,pwd)
    if MODEL.loginBuyer(user):
        # buyer = getBuyerInfo(email)
        # session["id"],session["username"],session["buyerpic"] = buyer[0],buyer[1],buyer[6]
        session["bemail"] = email
        session["bpwd"] = pwd
        elec=MODEL.getElectronics(1,0)
        hap=MODEL.getHomeAppliances(1,0)
        hlth=MODEL.getHealth(1,0)
        grs=MODEL.getGroceries(1,0)
        fashon=MODEL.getFashon(1,0)
        am=MODEL.getAutomobile(1,0)
        email = session.get("bemail")
        cid =  MODEL.getCartId(email)
        cdata = MODEL.getCartProduct(cid)
        return render_template("buyers/index.html" , log= "You have logged in successfully!", email=email,elec=elec,hap=hap, hlth=hlth,grs=grs,fashon=fashon,am=am,cdata=cdata)
    else:
        email = session.get("bemail")
        cid =  MODEL.getCartId(email)
        cdata = MODEL.getCartProduct(cid)
        return render_template("buyers/login.html", error=True,errormsg="Email or password invalid",cdata=cdata)

@app.route("/sellerEnd", methods=["POST"])
def sellerEnd():
    email=request.form["email"]
    pwd=request.form["pwd"]
    user=User(email,pwd)
    if MODEL.loginSeller(user):
        session["semail"] = email
        session["spwd"] = pwd
        elec=MODEL.getElectronics(1,0)
        hap=MODEL.getHomeAppliances(1,0)
        hlth=MODEL.getHealth(1,0)
        grs=MODEL.getGroceries(1,0)
        fashon=MODEL.getFashon(1,0)
        am=MODEL.getAutomobile(1,0)
        return render_template("seller/sellerHome.html" , log= "You have logged in successfully!", email=email, elec=elec,hap=hap, hlth=hlth,grs=grs,fashon=fashon,am=am)
    else:
        return render_template("buyers/login.html", error=True,errormsg="Email or password invalid")

@app.route("/logout")
def logout():
    session.clear()
    return render_template("buyers/login.html")


@app.route('/SearchedProduct',methods=["POST"])
def SearchedProduct():
    value = request.form["value"]
    prod=MODEL.getSearchedProduct(value)
    email = session.get("bemail")
    cid =  MODEL.getCartId(email)
    cdata = MODEL.getCartProduct(cid)
    return render_template('buyers/search.html', prod=prod,cdata=cdata)

@app.route('/productDetails',methods=["POST"])
def productDetails():
    pid = request.form["pid"]
    print(pid)
    prod = MODEL.getOneProduct(pid)
    relpro = MODEL.getRelatedProducts(pid)
    email = session.get("bemail")
    if email == None:
        cid =  MODEL.getCartId(email)
        cdata = MODEL.getCartProduct(cid)
        return render_template('buyers/productDetail.html',prod=prod,relpro=relpro,error=True,errormsg="You must have to login first to add products in cart.",cdata=cdata)
    else:
        email = session.get("bemail")
        cid =  MODEL.getCartId(email)
        cdata = MODEL.getCartProduct(cid)
        return render_template('buyers/productDetail.html',prod=prod,relpro=relpro,error=False,errormsg=None,cdata=cdata)


@app.route('/ElectronicsDevices')
def ElectronicsDevices():
    elec=MODEL.getElectronics(1,0)
    email = session.get("bemail")
    cid =  MODEL.getCartId(email)
    cdata = MODEL.getCartProduct(cid)
    return render_template('buyers/category.html', elec=elec,cat="Electronics Devices",cdata=cdata)

@app.route('/HomeAppliances')
def HomeAppliances():
    elec=MODEL.getHomeAppliances(1,0)
    email = session.get("bemail")
    cid =  MODEL.getCartId(email)
    cdata = MODEL.getCartProduct(cid)
    return render_template('buyers/category.html', elec=elec ,cat="Home Appliances",cdata=cdata)

@app.route('/HealthAndBeauty')
def HealthAndBeauty():
    elec=MODEL.getHealth(1,0)
    email = session.get("bemail")
    cid =  MODEL.getCartId(email)
    cdata = MODEL.getCartProduct(cid)
    return render_template('buyers/category.html', elec=elec,cat="Health & Beauty",cdata=cdata)

@app.route('/Groceries')
def Groceries():
    elec=MODEL.getGroceries(1,0)
    email = session.get("bemail")
    cid =  MODEL.getCartId(email)
    cdata = MODEL.getCartProduct(cid)
    return render_template('buyers/category.html', elec=elec,cat="Groceries",cdata=cdata)

@app.route('/Fashon')
def Fashon():
    elec=MODEL.getFashon(1,0)
    email = session.get("bemail")
    cid =  MODEL.getCartId(email)
    cdata = MODEL.getCartProduct(cid)
    return render_template('buyers/category.html', elec=elec,cat="Fashon",cdata=cdata)

@app.route('/AutoMobile')
def AutoMobile():
    elec=MODEL.getAutomobile(1,0)
    email = session.get("bemail")
    cid =  MODEL.getCartId(email)
    cdata = MODEL.getCartProduct(cid)
    return render_template('buyers/category.html', elec=elec,cat="Automobile",cdata=cdata)

@app.route('/Phones')
def Phones():
    prod=MODEL.getPhones()
    email = session.get("bemail")
    cid =  MODEL.getCartId(email)
    cdata = MODEL.getCartProduct(cid)
    return render_template('buyers/products.html',prod=prod,cat="Electronics Devices",product="Phones",catpath="/ElectronicsDevices",cdata=cdata)

@app.route('/Tablets')
def Tablets():
    prod=MODEL.getTablets()
    email = session.get("bemail")
    cid =  MODEL.getCartId(email)
    cdata = MODEL.getCartProduct(cid)
    return render_template('buyers/products.html',prod=prod,cat="Electronics Devices",product="Tablets",catpath="/ElectronicsDevices",cdata=cdata)

@app.route('/Laptops')
def LapTops():
    prod=MODEL.getLaptops()
    email = session.get("bemail")
    cid =  MODEL.getCartId(email)
    cdata = MODEL.getCartProduct(cid)
    return render_template('buyers/products.html',prod=prod,cat="Electronics Devices",product="Laptops",catpath="/ElectronicsDevices",cdata=cdata)

@app.route('/Desktop')
def Desktop():
    prod=MODEL.getDesktop()
    email = session.get("bemail")
    cid =  MODEL.getCartId(email)
    cdata = MODEL.getCartProduct(cid)
    return render_template('buyers/products.html',prod=prod,cat="Electronics Devices",product="Desktop",catpath="/ElectronicsDevices",cdata=cdata)

@app.route('/CamerasAndDrones')
def CamerasAndDrones():
    prod=MODEL.getCamDrones()
    email = session.get("bemail")
    cid =  MODEL.getCartId(email)
    cdata = MODEL.getCartProduct(cid)
    return render_template('buyers/products.html',prod=prod ,cat="Electronics Devices",product="Cameras & Drones",catpath="/ElectronicsDevices",cdata=cdata)

@app.route('/SmartWatches')
def SmartWatches():
    prod=MODEL.getSmartWatches()
    email = session.get("bemail")
    cid =  MODEL.getCartId(email)
    cdata = MODEL.getCartProduct(cid)
    return render_template('buyers/products.html',prod=prod,cat="Electronics Devices",product="Smart Watches",catpath="/ElectronicsDevices",cdata=cdata)

@app.route('/GamingConsoles')
def GamingConsoles():
    prod=MODEL.getGamingConsloes()
    email = session.get("bemail")
    cid =  MODEL.getCartId(email)
    cdata = MODEL.getCartProduct(cid)
    return render_template('buyers/products.html',prod=prod,cat="Electronics Devices",product="Gaming Consoles",catpath="/ElectronicsDevices",cdata=cdata)

@app.route('/SmartTV')
def SmartTV():
    prod=MODEL.getSmartTV()
    email = session.get("bemail")
    cid =  MODEL.getCartId(email)
    cdata = MODEL.getCartProduct(cid)
    return render_template('buyers/products.html',prod=prod,cat="Home Appliances",product="Smart TV",catpath="/HomeAppliances",cdata=cdata)

@app.route('/HomeAudio')
def HomeAudio():
    prod=MODEL.getHomeAudio()
    email = session.get("bemail")
    cid =  MODEL.getCartId(email)
    cdata = MODEL.getCartProduct(cid)
    return render_template('buyers/products.html',prod=prod,cat="Home Appliances",product="Home Audio",catpath="/HomeAppliances",cdata=cdata)

@app.route('/KitchenAppliances')
def KitchenAppliances():
    prod=MODEL.getKitchenAppliances()
    email = session.get("bemail")
    cid =  MODEL.getCartId(email)
    cdata = MODEL.getCartProduct(cid)
    return render_template('buyers/products.html',prod=prod,cat="Home Appliances",product="Kitchen Appliances",catpath="/HomeAppliances",cdata=cdata)

@app.route('/CoolingAndHeating')
def CoolingAndHeating():
    prod=MODEL.getCoolingAndHeating()
    email = session.get("bemail")
    cid =  MODEL.getCartId(email)
    cdata = MODEL.getCartProduct(cid)
    return render_template('buyers/products.html',prod=prod,cat="Home Appliances",product="Cooling & Heating",catpath="/HomeAppliances",cdata=cdata)

@app.route('/FloorCare')
def FloorCare():
    prod=MODEL.getFloorCare()
    email = session.get("bemail")
    cid =  MODEL.getCartId(email)
    cdata = MODEL.getCartProduct(cid)
    return render_template('buyers/products.html',prod=prod,cat="Home Appliances",product="Floor Care",catpath="/HomeAppliances",cdata=cdata)

@app.route('/Generators')
def Generators():
    prod=MODEL.getGenerators()
    email = session.get("bemail")
    cid =  MODEL.getCartId(email)
    cdata = MODEL.getCartProduct(cid)
    return render_template('buyers/products.html',prod=prod,cat="Home Appliances",product="Generators",catpath="/HomeAppliances",cdata=cdata)

@app.route('/WashersAndDryers')
def WashersAndDryers():
    prod=MODEL.getWashersDryers()
    email = session.get("bemail")
    cid =  MODEL.getCartId(email)
    cdata = MODEL.getCartProduct(cid)
    return render_template('buyers/products.html',prod=prod,cat="Home Appliances",product="Washers & Dryers",catpath="/HomeAppliances",cdata=cdata)

@app.route('/Fragrances')
def Fragrances():
    prod=MODEL.getFragrances()
    email = session.get("bemail")
    cid =  MODEL.getCartId(email)
    cdata = MODEL.getCartProduct(cid)
    return render_template('buyers/products.html',prod=prod,cat="Health & Beauty",product="Fragrances",catpath="/HealthAndBeauty",cdata=cdata)

@app.route('/HairCare')
def HairCare():
    email = session.get("bemail")
    cid =  MODEL.getCartId(email)
    cdata = MODEL.getCartProduct(cid)
    prod=MODEL.getHairCare()
    return render_template('buyers/products.html',prod=prod,cat="Health & Beauty",product="Hair Care",catpath="/HealthAndBeauty",cdata=cdata)


@app.route('/MensCare')
def MensCare():
    prod=MODEL.getMensCare()
    email = session.get("bemail")
    cid =  MODEL.getCartId(email)
    cdata = MODEL.getCartProduct(cid)
    return render_template('buyers/products.html',prod=prod,cat="Health & Beauty",product="Mens Care",catpath="/HealthAndBeauty",cdata=cdata)

@app.route('/SkinCare')
def SkinCare():
    prod=MODEL.getSkinCare()
    email = session.get("bemail")
    cid =  MODEL.getCartId(email)
    cdata = MODEL.getCartProduct(cid)
    return render_template('buyers/products.html',prod=prod,cat="Health & Beauty",product="Skin Care",catpath="/HealthAndBeauty",cdata=cdata)

@app.route('/Makeup')
def Makeup():
    prod=MODEL.getMakeup()
    email = session.get("bemail")
    cid =  MODEL.getCartId(email)
    cdata = MODEL.getCartProduct(cid)
    return render_template('buyers/products.html',prod=prod,cat="Health & Beauty",product="Makeup",catpath="/HealthAndBeauty",cdata=cdata)

@app.route('/MedicalSupplies')
def MedicalSupplies():
    prod=MODEL.getMedicalSupplies()
    email = session.get("bemail")
    cid =  MODEL.getCartId(email)
    cdata = MODEL.getCartProduct(cid)
    return render_template('buyers/products.html',prod=prod,cat="Health & Beauty",product="Medical Supplies",catpath="/HealthAndBeauty",cdata=cdata)

@app.route('/BeautyTools')
def BeautyTools():
    prod=MODEL.getBeautyTools()
    email = session.get("bemail")
    cid =  MODEL.getCartId(email)
    cdata = MODEL.getCartProduct(cid)
    return render_template('buyers/products.html',prod=prod,cat="Health & Beauty",product="Beauty Tools",catpath="/HealthAndBeauty",cdata=cdata)

@app.route('/Bevarages')
def Bevarages():
    prod=MODEL.getBevarages()
    email = session.get("bemail")
    cid =  MODEL.getCartId(email)
    cdata = MODEL.getCartProduct(cid)
    return render_template('buyers/products.html',prod=prod,cat="Groceries",product="Bevarages",catpath="/Groceries",cdata=cdata)

@app.route('/FreshProducts')
def FreshProducts():
    email = session.get("bemail")
    cid =  MODEL.getCartId(email)
    cdata = MODEL.getCartProduct(cid)
    prod=MODEL.getFreshProducts()
    return render_template('buyers/products.html',prod=prod,cat="Groceries",product="Fresh Products",catpath="/Groceries",cdata=cdata)

@app.route('/Snacks')
def Snacks():
    prod=MODEL.getSnacks()
    email = session.get("bemail")
    cid =  MODEL.getCartId(email)
    cdata = MODEL.getCartProduct(cid)
    return render_template('buyers/products.html',prod=prod,cat="Groceries",product="Snacks",catpath="/Groceries",cdata=cdata)

@app.route('/FoodStaples')
def FoodStaples():
    prod=MODEL.getFoodStaples()
    email = session.get("bemail")
    cid =  MODEL.getCartId(email)
    cdata = MODEL.getCartProduct(cid)
    return render_template('buyers/products.html',prod=prod,cat="Groceries",product="Food Staples",catpath="/Groceries",cdata=cdata)

@app.route('/DairyAndChilled')
def DairyAndChilled():
    prod=MODEL.getDairyChilled()
    email = session.get("bemail")
    cid =  MODEL.getCartId(email)
    cdata = MODEL.getCartProduct(cid)
    return render_template('buyers/products.html',prod=prod,cat="Groceries",product="Dairy & Chilled",catpath="/Groceries",cdata=cdata)

@app.route('/FrozenFood')
def FrozenFood():
    prod=MODEL.getFrozenFood()
    email = session.get("bemail")
    cid =  MODEL.getCartId(email)
    cdata = MODEL.getCartProduct(cid)
    return render_template('buyers/products.html',prod=prod,cat="Groceries",product="Frozen Food",catpath="/Groceries",cdata=cdata)

@app.route('/MensFashon')
def MensFashon():
    prod=MODEL.getMensFashon()
    email = session.get("bemail")
    cid =  MODEL.getCartId(email)
    cdata = MODEL.getCartProduct(cid)
    return render_template('buyers/products.html',prod=prod,cat="Fashon",product="Mens Fashon",catpath="/Fashon",cdata=cdata)

@app.route('/WomensFashon')
def WomensFashon():
    email = session.get("bemail")
    cid =  MODEL.getCartId(email)
    cdata = MODEL.getCartProduct(cid)
    prod=MODEL.getWomensFashon()
    return render_template('buyers/products.html',prod=prod,cat="Fashon",product="Womens Fashon",catpath="/Fashon",cdata=cdata)

@app.route('/WinterClothing')
def WinterClothing():
    email = session.get("bemail")
    cid =  MODEL.getCartId(email)
    cdata = MODEL.getCartProduct(cid)
    prod=MODEL.getWinterClothing()
    return render_template('buyers/products.html',prod=prod,cat="Fashon",product="Winter Clothing",catpath="/Fashon",cdata=cdata)

@app.route('/SummerClothing')
def SummerClothing():
    prod=MODEL.getSummerClothing()
    email = session.get("bemail")
    cid =  MODEL.getCartId(email)
    cdata = MODEL.getCartProduct(cid)
    return render_template('buyers/products.html',prod=prod,cat="Fashon",product="Summer Clothing",catpath="/Fashon",cdata=cdata)

@app.route('/InnerWear')
def InnerWear():
    email = session.get("bemail")
    cid =  MODEL.getCartId(email)
    cdata = MODEL.getCartProduct(cid)
    prod=MODEL.getInnerWear()
    return render_template('buyers/products.html',prod=prod,cat="Fashon",product="Inner Wear",catpath="/Fashon",cdata=cdata)

@app.route('/Shoes')
def Shoes():
    prod=MODEL.getShoes()
    email = session.get("bemail")
    cid =  MODEL.getCartId(email)
    cdata = MODEL.getCartProduct(cid)
    return render_template('buyers/products.html',prod=prod,cat="Fashon",product="Shoes",catpath="/Fashon",cdata=cdata)

@app.route('/Accessories')
def Accessories():
    prod=MODEL.getAccessories()
    email = session.get("bemail")
    cid =  MODEL.getCartId(email)
    cdata = MODEL.getCartProduct(cid)
    return render_template('buyers/products.html',prod=prod,cat="Automobile",product="Accessories",catpath="/AutoMobile",cdata=cdata)

@app.route('/Motorcycles')
def Motorcycles():
    email = session.get("bemail")
    cid =  MODEL.getCartId(email)
    cdata = MODEL.getCartProduct(cid)
    prod=MODEL.getMotorcycles()
    return render_template('buyers/products.html',prod=prod,cat="Automobile",product="Motorcycles",catpath="/AutoMobile",cdata=cdata)

@app.route('/Cars')
def Cars():
    prod=MODEL.getCars()
    email = session.get("bemail")
    cid =  MODEL.getCartId(email)
    cdata = MODEL.getCartProduct(cid)
    return render_template('buyers/products.html',prod=prod,cat="Automobile",product="Cars",catpath="/AutoMobile",cdata=cdata)

@app.route('/Rikshas')
def Rikshas():
    prod=MODEL.getRikshas()
    email = session.get("bemail")
    cid =  MODEL.getCartId(email)
    cdata = MODEL.getCartProduct(cid)
    return render_template('buyers/products.html',prod=prod,cat="Automobile",product="Rikshas",catpath="/AutoMobile",cdata=cdata)

@app.route('/Loaders')
def Loaders():
    email = session.get("bemail")
    cid =  MODEL.getCartId(email)
    cdata = MODEL.getCartProduct(cid)
    prod=MODEL.getLoaders()
    return render_template('buyers/products.html',prod=prod,cat="Automobile",product="Loaders",catpath="/AutoMobile",cdata=cdata)

@app.route('/SportsBikes')
def SportsBikes():
    email = session.get("bemail")
    cid =  MODEL.getCartId(email)
    cdata = MODEL.getCartProduct(cid)
    prod=MODEL.getSportsBike()
    return render_template('buyers/products.html',prod=prod,cat="Automobile",product="Sports Bikes",catpath="/AutoMobile",cdata=cdata)

@app.route('/Helmets')
def Helmets():
    prod=MODEL.getHelmets()
    email = session.get("bemail")
    cid =  MODEL.getCartId(email)
    cdata = MODEL.getCartProduct(cid)
    return render_template('buyers/products.html',prod=prod,cat="Automobile",product="Helmets",catpath="/AutoMobile",cdata=cdata)

@app.route('/RidingGears')
def RidingGears():
    prod=MODEL.getRidingGears()
    email = session.get("bemail")
    cid =  MODEL.getCartId(email)
    cdata = MODEL.getCartProduct(cid)
    return render_template('buyers/products.html',prod=prod,cat="Automobile",product="Riding Gears",catpath="/AutoMobile",cdata=cdata)


# @seller

@app.route('/sellerHome')
def home():
    return render_template('seller/sellerHome.html',seller = (session["name"],session["pic"],session["category"]),orders=(len(cartsfunc("Deliverd")),len(cartsfunc("Order Confirmd"))),sellerInfo=(MODEL.getSellerProductsCount(session["id"]),MODEL.getSellerPendingApprovedProductsCount(session["id"], 1),MODEL.getSellerPendingApprovedProductsCount(session["id"], 0)))


@app.route('/sellerloginInAction',methods=["post"])
def loginInAction():
    email = request.form["email"]
    password = request.form["password"]
    seller = MODEL.loginSellerS(Seller(email, password))
    if seller:
        session["email"],session["password"],session["id"],session["name"],session["pic"],session["category"] = seller[0],seller[1],seller[2],seller[3],seller[4],seller[5]
        print(seller[5])
        print(session["category"])
        return render_template('seller/sellerHome.html',orders=(len(cartsfunc("Deliverd")),len(cartsfunc("Order Confirmd"))),seller = (session["name"],session["pic"],session["category"]),sellerInfo=(MODEL.getSellerProductsCount(session["id"]),MODEL.getSellerPendingApprovedProductsCount(session["id"], 1),MODEL.getSellerPendingApprovedProductsCount(session["id"], 0)))
    else:
        return render_template('buyers/login.html',error=True,errormsg="Email or password invalid")

@app.route('/addNewProduct')
def addNewProduct():
    print(session["category"])
    return render_template('seller/addNewProduct.html',sellerInfo=(MODEL.getSellerProductsCount(session["id"]),MODEL.getSellerPendingApprovedProductsCount(session["id"], 1),MODEL.getSellerPendingApprovedProductsCount(session["id"], 0)),subCategories=MODEL.getSubCategories(MODEL.getCategoryId(session["category"])),seller = (session["name"],session["pic"],session["category"]))

@app.route('/addProductInAction' ,methods=["post"])
def addProductInAction():
    name = request.form["name"]
    price = float(request.form["price"])
    stock = int(request.form["stock"])
    description = request.form["details"]
    category = request.form["category"]
    tag = request.form["tag"]
    image = request.files["image"]
    sid = int(session["id"])
    newFileName = str(int(MODEL.getProductMaxID())+1)+"."+ image.filename.split('.')[1]
    image.save(f"static\\productImages\\{newFileName}")
    MODEL.addProduct(Product(name,category,description,price,stock,tag,newFileName,sid))
    return render_template('seller/sellerHome.html',orders=(len(cartsfunc("Deliverd")),len(cartsfunc("Order Confirmd"))),seller = (session["name"],session["pic"],session["category"]),sellerInfo=(MODEL.getSellerProductsCount(session["id"]),MODEL.getSellerPendingApprovedProductsCount(session["id"], 1),MODEL.getSellerPendingApprovedProductsCount(session["id"], 0)))


# @app.route('/myChat')
# def myChat():
#     buyerRecords = []
#     if(MODEL.getMyBuyers(session["id"])):
#         for buyer in set(MODEL.getMyBuyers(session["id"])):
#             buyerRecords.append(MODEL.getBuyer(buyer))
#     return render_template("seller/chatMain.html",seller = (session["name"],session["pic"],session["category"]),buyers=buyerRecords,msg="MY BUYERS",sellerInfo=(MODEL.getSellerProductsCount(session["id"]),MODEL.getSellerPendingApprovedProductsCount(session["id"], 1),MODEL.getSellerPendingApprovedProductsCount(session["id"], 0)))







@app.route('/approvedProducts')
def approvedProducts():
    return render_template("seller/approvedProducts.html",seller = (session["name"],session["pic"],session["category"]),approvedProducts=MODEL.getSellerProducts(session["id"], 1),sellerInfo=(MODEL.getSellerProductsCount(session["id"]),MODEL.getSellerPendingApprovedProductsCount(session["id"], 1),MODEL.getSellerPendingApprovedProductsCount(session["id"], 0)))

@app.route('/sellerSearch',methods=["post"])
def sellerSearch():
    category = request.form["choices"]
    keyword = request.form["keyword"]
    if category == "Approved Products":
        print("approved")
        return render_template("seller/approvedProducts.html",seller = (session["name"],session["pic"],session["category"]),approvedProducts=MODEL.getAppProbyName(session["id"],keyword,1),sellerInfo=(MODEL.getSellerProductsCount(session["id"]),MODEL.getSellerPendingApprovedProductsCount(session["id"], 1),MODEL.getSellerPendingApprovedProductsCount(session["id"], 0)))
    else:
        print("non aprroced")
        return render_template("seller/pendingProducts.html",seller = (session["name"],session["pic"],session["category"]),pendingProducts=MODEL.getAppProbyName(session["id"],keyword,0),sellerInfo=(MODEL.getSellerProductsCount(session["id"]),MODEL.getSellerPendingApprovedProductsCount(session["id"], 1),MODEL.getSellerPendingApprovedProductsCount(session["id"], 0)))
        

@app.route('/productDetail/<int:pid>')
def productDetail(pid):
    return render_template('seller/productDetail.html',seller = (session["name"],session["pic"],session["category"]),product = MODEL.getProduct(pid),sellerInfo=(MODEL.getSellerProductsCount(session["id"]),MODEL.getSellerPendingApprovedProductsCount(session["id"], 1),MODEL.getSellerPendingApprovedProductsCount(session["id"], 0)))


@app.route('/pendingProducts')
def pendingProducts():
    return render_template("seller/pendingProducts.html",seller = (session["name"],session["pic"],session["category"]),approvedProducts=MODEL.getSellerProducts(session["id"], 0),sellerInfo=(MODEL.getSellerProductsCount(session["id"]),MODEL.getSellerPendingApprovedProductsCount(session["id"], 1),MODEL.getSellerPendingApprovedProductsCount(session["id"], 0)))


def cartsfunc(status):
    Orders = MODEL.getOrdersS(session["id"],status)
    cartIDs = []
    for order in Orders:
        cartIDs.append(order[0])
    cartIDs = list(set(cartIDs))
    carts = []
    for cartid in cartIDs:
        cart=[]
        total = 0
        for order in Orders:
            order=order+(order[3]*order[4],)
            if order[0] == cartid:
               total+=order[10]
               cart.append(order)
        cart.append(total)
        carts.append(cart)
    return carts

@app.route('/newOrders')
def newOrders():
    carts = cartsfunc("Order confirmed")
    print(carts)
    return render_template('seller/newOrders.html',seller = (session["name"],session["pic"],session["category"]),carts=carts,sellerInfo=(MODEL.getSellerProductsCount(session["id"]),MODEL.getSellerPendingApprovedProductsCount(session["id"], 1),MODEL.getSellerPendingApprovedProductsCount(session["id"], 0)))

@app.route('/deliverdOrders')
def deliverdOrders():
    carts = cartsfunc("Deliverd")
    return render_template('seller/deliverdOrders.html',seller = (session["name"],session["pic"],session["category"]),carts=carts,sellerInfo=(MODEL.getSellerProductsCount(session["id"]),MODEL.getSellerPendingApprovedProductsCount(session["id"], 1),MODEL.getSellerPendingApprovedProductsCount(session["id"], 0)))


@app.route('/cartDetail/<int:cartID>')
def cartDetail(cartID):
    carts = cartsfunc("Order confirmed")
    myCart = None
    for crt in carts:
        if crt[0][0]==cartID:
            myCart = crt
            break
    print(myCart)
    return render_template('seller/viewCart.html',seller = (session["name"],session["pic"],session["category"]), cart=myCart,sellerInfo=(MODEL.getSellerProductsCount(session["id"]),MODEL.getSellerPendingApprovedProductsCount(session["id"], 1),MODEL.getSellerPendingApprovedProductsCount(session["id"], 0)))



@app.route('/changeCartStatus/<int:cartID>',methods=["post"])
def changeCartStatus(cartID):
    status = request.form["deliveryStatus"]
    cart = cartsfunc("Order confirmed")
    MODEL.changeCartStatus(cartID,status)
    return redirect(url_for('newOrders'))


@app.route('/deliverdcartDetail/<int:cartID>')
def deliverdcartDetail(cartID):
    carts = cartsfunc("Deliverd")
    myCart = None
    for crt in carts:
        if crt[0][0]==cartID:
            myCart = crt
            break
    return render_template('seller/viewCart.html',seller = (session["name"],session["pic"],session["category"]), cart=myCart,sellerInfo=(MODEL.getSellerProductsCount(session["id"]),MODEL.getSellerPendingApprovedProductsCount(session["id"], 1),MODEL.getSellerPendingApprovedProductsCount(session["id"], 0)))
    

@app.route('/updateProduct/<int:pid>')
def updateProduct(pid):
    return render_template('seller/updateProductForm.html',product=MODEL.getProduct(pid),seller = (session["name"],session["pic"],session["category"]),subCategories=MODEL.getSubCategories(MODEL.getCategoryId(session["category"])),sellerInfo=(MODEL.getSellerProductsCount(session["id"]),MODEL.getSellerPendingApprovedProductsCount(session["id"], 1),MODEL.getSellerPendingApprovedProductsCount(session["id"], 0)))


@app.route('/upadateInAction/<int:pid>',methods=["post"])
def upadateInAction(pid):
    name = request.form["name"]
    price = float(request.form["price"])
    stock = int(request.form["stock"])
    description = request.form["details"]
    category = request.form["category"]
    tag = request.form["tag"]
    image = request.files["image"]
    sid = int(session["id"])
    newFileName = str(int(MODEL.getProductMaxID())+1)+"."+ image.filename.split('.')[1]
    image.save(f"static\\productImages\\{newFileName}")
    MODEL.updateProduct(pid,Product(name,category,description,price,stock,tag,newFileName,sid))
    return render_template('seller/sellerHome.html',seller = (session["name"],session["pic"],session["category"]),orders=(len(cartsfunc("Deliverd")),len(cartsfunc("Order Confirmd"))),sellerInfo=(MODEL.getSellerProductsCount(session["id"]),MODEL.getSellerPendingApprovedProductsCount(session["id"], 1),MODEL.getSellerPendingApprovedProductsCount(session["id"], 0)))

socketio = SocketIO(app)

@app.route('/buyerChat')
def buyerChat():
    sellerRecords = []
    if(MODEL.getMySellers(session["id"])):
        for seller in set(MODEL.getMySellers(session["id"])):
            sellerRecords.append(MODEL.getSeller(seller))
    return render_template("buyer/chatMain.html",buyer = (session["name"],session["pic"],session["category"]),sellers=sellerRecords,msg="My Sellers")

@app.route('/buyer/<int:buyerID>')
def buyer(buyerID):
    return render_template('seller/baatCheet.html',seller = (session["name"],session["pic"],session["category"]),roomID=f"{buyerID},{session['id']}",username=MODEL.getSellerName(session['id']),messages=MODEL.getMessages(f"{buyerID},{session['id']}"))

@app.route('/seller/<int:sellerID>')
def seller(sellerID):
    return render_template('seller/baatCheet.html',seller = (session["name"],session["pic"],session["category"]),roomID=f"{session['id']},{sellerID}",username=MODEL.getBuyerName(session['id']),messages=MODEL.getMessages(f"{session['id']},{sellerID}"))

@socketio.on('send_message')
def handle_send_message_event(data):

    MODEL.addMessage( data['room'], data['message'], data['time'] ,data['username'])
    socketio.emit('receive_message', data, room=data['room'])

@socketio.on('join_room')
def handle_join_room_event(data):
    # app.logger.sellerInfo("{} has joined the room {}".format(data['username'], data['room']))
    join_room(data['room'])
    socketio.emit('join_room_announcement', data, room=data['room'])

@socketio.on('leave_room')
def handle_leave_room_event(data):
    # app.logger.sellerInfo("{} has left the room {}".format(data['username'], data['room']))
    leave_room(data['room'])
    socketio.emit('leave_room_announcement', data, room=data['room'])

@app.route('/sellerlogOut')
def sellerloOut():
    return redirect('/')

# admin

@app.route('/adminLogin')
def adminLogin():
    session.clear()
    return render_template("admin/adminLogin.html")

@app.route('/adminHome')
def adminMain():
    if session.get("aemail")!=None:
        return render_template("admin/adminMain.html",info = [MODEL.getTotalProductsCount(),MODEL.getProductsCount(1),MODEL.getProductsCount(0),MODEL.getBuyersCount(),MODEL.getAllSellers(),MODEL.getSellersCount(0),MODEL.getSellersCount(1) , MODEL.getOrdersCount()])  if session.get("aemail") else redirect("/")
    else:
        return render_template("admin/adminLogin.html")


@app.route('/adminHome' , methods=["post"])
def adminHome():
    email,password = None , None
    admin = None
    if session.get("aemail") == None:
        email = request.form["email"]
        password = request.form["password"]
        admin = Admin(email,password)
    else:
        admin =Admin(session["aemail"],session["apassword"])
    if MODEL.loginAdmin(admin):
        adminid = MODEL.getAdminId(admin)
        print(adminid[0])
        session["aemail"],session["apassword"],session["adminId"] = email,password,adminid
        return render_template("admin/adminMain.html",info = [MODEL.getTotalProductsCount(),MODEL.getProductsCount(1),MODEL.getProductsCount(0),MODEL.getBuyersCount(),MODEL.getAllSellers(),MODEL.getSellersCount(0),MODEL.getSellersCount(1) , MODEL.getOrdersCount()])  if session.get("aemail") else redirect('/')
    else:
        return redirect('adminLogin')

@app.route('/newSellers')
def newSellers():
    adminID = session["adminId"]
    sellers = MODEL.getnewSellers(0, adminID[0])
    return render_template('admin/newSellers.html',sellers=sellers)

@app.route('/newsellerdetails', methods=["POST"])
def newSellerDetails():
    sEmail = request.form["semail"]
    seller = MODEL.getnewSellerDetails(sEmail,0)
    return render_template('admin/newSellerDetails.html',seller=seller)

@app.route('/approvalstatus',methods=["POST"])
def approvalstatus():
    sEmail = request.form["semaila"]
    adminID = session["adminId"]
    status = MODEL.approveSeller(sEmail, adminID[0])
    if status == True:
        msg = Message('Account details', recipients = [sEmail])
        msg.html = "<h2>Your account in Earth joy has been approved :) <br/>Don't reply to this mail.</h2>"
        mail.send(msg)
        #return "Message has been sent!"
        return render_template('admin/sellerStatus.html' , msg="Sellers account has been approved.")
    else:
        return render_template('admin/sellerStatus.html', msg="There is an error in approving account.")


@app.route('/rejectstatus',methods=["POST"])
def rejectstatus():
    sEmail = request.form["semailr"]
    status = MODEL.rejectSeller(sEmail)
    if status == True:
        msg = Message('Account details', recipients = [sEmail])
        msg.html = "<h2>Your account in Earth joy has been rejected because you are not eligible for it. Don't reply to this mail.</h2>"
        mail.send(msg)
        #return "Message has been sent!"
        return render_template('admin/rejectStatus.html' , msg="Sellers account has been rejected.",msg2="And an email has been sent to seller.")
    else:
        return render_template('admin/rejectStatus.html', msg="There is an error in rejecting account.")


@app.route('/existingSellers')
def existingSellers():
    sellers = MODEL.getSellers(1)
    return render_template('admin/existingSellers.html',sellers=sellers)




@app.route('/existingsellerdetails', methods=["POST"])
def existingSellerDetails():
    sEmail = request.form["semail"]
    seller = MODEL.getSellerDetails(sEmail,1)
    return render_template('admin/existingSellerDetails.html',seller=seller)

@app.route('/blockStatus',methods=["POST"])
def blockStatus():
    sEmail = request.form["semailb"]
    print("seller email to block: "  + sEmail)
    status = MODEL.blockSeller(sEmail)
    if status == True:
        msg = Message('Account Details', recipients = [sEmail])
        msg.html = "<h2>Your account in Earth joy online shoping center has been blocked! :( <br/>Don't reply to this mail.</h2>"
        mail.send(msg)
        #return "Message has been sent!"
        return render_template('admin/blockStatus.html' , msg="Sellers account has been blocked.",msg2="And an email has been sent to seller.")
    else:
        return render_template('admin/blockStatus.html', msg="There is an error in blocking account.")



@app.route('/blockedSellers')
def blockedSellers():
    sellers = MODEL.getBlockedSellers(1)
    return render_template('admin/blockedSellers.html',sellers=sellers)

@app.route('/blocksellerdetails', methods=["POST"])
def blocksellerdetails():
    sEmail = request.form["bsemaild"]
    seller = MODEL.getSellerDetails(sEmail,1)
    return render_template('admin/blocksellerdetails.html',seller=seller)

@app.route('/unblockStatus',methods=["POST"])
def unblockStatus():
    sEmail = request.form["semailub"]
    status = MODEL.unblockSeller(sEmail)
    if status == True:
        msg = Message('Account Details', recipients = [sEmail])
        msg.html = "<h2>Your account in Earth joy online shoping center has been unblocked! Hurrah!. Don't reply to this mail.</h2>"
        mail.send(msg)
        return render_template('admin/unblockStatus.html' , msg="Sellers account has been unblocked.",msg2="And an email has been sent to seller.")
    else:
        return render_template('admin/unblockStatus.html', msg="There is an error in unblocking account.")

@app.route('/newProducts')
def newProducts():
    products = MODEL.getProducts(0)
    return render_template('admin/newProducts.html',products=products)  if session.get("aemail") else render_template("admin/adminLogin.html")

@app.route('/newproductdetails', methods=["POST"])
def newproductdetails():
    pid = request.form["pid"]
    product = MODEL.getProductDetails(pid,0)
    return render_template('admin/newproductdetails.html',product=product)

@app.route('/papprovalstatus',methods=["POST"])
def papprovalstatus():
    sEmail = request.form["semaila"]
    pid = request.form["pid"]
    status = MODEL.approveProduct(pid)
    if status == True:
        msg = Message('Product approval details', recipients = [sEmail])
        msg.html = "<h2>Your product in Earth joy has been approved :) <br/>Don't reply to this mail.</h2>"
        mail.send(msg)
        # return "Message has been sent!"
        return render_template('admin/productStatus.html' , msg="Sellers product has been approved.",msg2="And an email has been sent to respective seller.")
    else:
        return render_template('admin/productStatus.html', msg="There is an error in approving sellers product.")

@app.route('/existingProducts')
def existingProducts():
    products = MODEL.getProducts(1)
    return render_template('admin/existingProducts.html',products=products)  if session.get("aemail") else render_template("admin/adminLogin.html")

@app.route('/existingproductdetails', methods=["POST"])
def existingproductdetails():
    pid = request.form["pid"]
    product = MODEL.getProductDetails(pid,1)
    return render_template('admin/existingproductdetails.html',product=product)

@app.route('/deletestatus',methods=["POST"])
def deletestatus():
    sEmail = request.form["semaila"]
    print("email: " + sEmail)
    pid = request.form["pid"]
    print(pid)
    status = MODEL.deleteProduct(pid)
    if status == True:
        msg = Message('Product removed from Earth Joy', recipients = [sEmail])
        msg.html = "<h2>Your product in Earth joy has been Blocked :(<br/>Don't reply to this mail.</h2>"
        mail.send(msg)
        # return "Message has been sent!"
        return render_template('admin/deleteStatus.html' , msg="Sellers product has been blocked.",msg2="And an email has been sent to respective seller.")
    else:
        return render_template('admin/deleteStatus.html', msg="There is an error in blocking sellers product.")

@app.route('/blockProducts')
def blockProducts():
    products = MODEL.getblockProducts(1)
    return render_template('admin/blockedProducts.html',products=products)  if session.get("aemail") else render_template("admin/adminLogin.html")

@app.route('/blockproductdetails', methods=["POST"])
def blockproductdetails():
    pid = request.form["pid"]
    product = MODEL.getProductDetails(pid,1)
    return render_template('admin/blockproductdetails.html',product=product)

@app.route('/unblockstatus',methods=["POST"])
def unblockstatus():
    sEmail = request.form["semaila"]
    pid = request.form["pid"]
    status = MODEL.unblockProduct(pid)
    if status == True:
        msg = Message('Product removed from Earth Joy', recipients = [sEmail])
        msg.html = "<h2>Your product in Earth joy has been unblocked :)<br/>Don't reply to this mail.</h2>"
        mail.send(msg)
        # return "Message has been sent!"
        return render_template('admin/punblockStatus.html' , msg="Sellers product has been unblocked.",msg2="And an email has been sent to respective seller.")
    else:
        return render_template('admin/punblockStatus.html', msg="There is an error in unblocking sellers product.")

@app.route('/addNewCategory')
def addNewCategory():
    return render_template('admin/addNewCategory.html')  if session.get("aemail") else render_template("admin/adminLogin.html")

@app.route('/addNewSubCategory')
def addNewSubCategory():
    return render_template('admin/addNewSubCategory.html', categories = MODEL.getCategories())  if session.get("aemail") else render_template("admin/adminLogin.html")
    

@app.route('/deleteCategory')
def addDeleteCategory():
    return render_template('admin/deleteCategory.html')  if session.get("aemail") else render_template("admin/adminLogin.html")
    

@app.route('/deleteSubCategory')
def addDeleteSubCategory():
    return render_template('admin/deleteSubCategory.html')  if session.get("aemail") else render_template("admin/adminLogin.html")



@app.route('/addNewCategoryInAction',methods = ["post"])
def addNewCategoryInAction():
    category = request.form["category"].lower()
    if MODEL.checkCategoryExist(category):
        return render_template("admin/addNewCategory.html",errorMsg="Category Already Exist")  if session.get("aemail") else render_template("admin/adminLogin.html")
    else:
        MODEL.addNewCategory(category)
        return render_template("admin/addNewCategory.html",successMsg="Category added Successfully")  if session.get("aemail") else render_template("admin/adminLogin.html")


@app.route('/newSubCategoryInAction',methods=["post"])
def newSubCategoryInAction():
    categoryID = request.form["categories"]
    subcategory = request.form["subcategory"]
    if MODEL.checkSubCategoryExist(subcategory):
        return render_template("admin/addNewSubCategory.html",categories = MODEL.getCategories(),errorMsg="This subcategory already exist")  if session.get("aemail") else render_template("admin/adminLogin.html")
    else:
        MODEL.addNewSubCategory(categoryID,subcategory)
        return render_template("admin/addNewSubCategory.html",categories = MODEL.getCategories(),successMsg="Subcategory added successfully") if session.get("aemail") else render_template("admin/adminLogin.html")
    

@app.route('/search',methods=["post"])
def search():
    category = request.form["choices"]
    keyword = request.form["keyword"]

    if category == "New Products":
        return render_template('admin/newProducts.html',products=MODEL.getExisProbyName(keyword))
    elif category == "Existing Products":
        return render_template('admin/existingProducts.html',products=MODEL.getAppProbyNameSearch(keyword))
    elif category == "Category":
        return render_template('admin/existingProducts.html',products=MODEL.getProbyCate(keyword))
    elif category == "Subcategory":
        return render_template('admin/existingProducts.html',products=MODEL.getProbySubCate(keyword))
    elif category == "New Sellers":
        return render_template('admin/newSellers.html',sellers=MODEL.getNewSellerbyName(keyword))
    elif category == "Existing Sellers":
        return render_template('admin/existingSellers.html',sellers=MODEL.getExisSellerbyName(keyword))

    

@app.route('/payment', methods=["POST"])
def payment():
    email = session.get("bemail")
    cid =  MODEL.getCartId(email)
    cdata = MODEL.getCartProduct(cid)
    gTotal = MODEL.getSumPrice(cid)

    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {
            "payment_method": "paypal"},
        "redirect_urls": {
            "return_url": "http://localhost:3000/payment/execute",
            "cancel_url": "http://localhost:3000/userdashboard"},
        "transactions": [{
            "item_list": {
                "items": [{
                    "name": "Total Payment",
                    "sku": "12345",
                    "price": gTotal,
                    "currency": "USD",
                    "quantity": 1}]},
            "amount": {
                "total": gTotal,
                "currency": "USD"},
            "description": "This is the payment transaction description."}]})

    if payment.create():
        print('Payment success!')
    else:
        print(payment.error)

    return jsonify({'paymentID': payment.id})

@app.route('/execute', methods=['POST'])
def execute():
    success = False
    payment = paypalrestsdk.Payment.find(request.form['paymentID'])
    if payment.execute({'payer_id' : request.form['payerID']}):
        print('Execute success!')
        success = True
    else:
        print(payment.error)
    return jsonify({'success' : success})

    
@app.route('/logOut')
def logOut():
    return redirect('/adminLogin')
if __name__=="__main__":
    socketio.run(app,debug=True)