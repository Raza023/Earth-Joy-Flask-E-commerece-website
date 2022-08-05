from http.client import NotConnected
import pymysql
from views import *

class EarthJoyModel:
    def __init__(self,host,user,password,database):
        self.host=host
        self.user=user
        self.password=password
        self.database=database
        self.connection=None
        try:
            self.connection=pymysql.connect(host=self.host, user=self.user,password=self.password,database=self.database)
        except Exception as e:
            print("There is error in connection",str(e))

    def __del__(self):
        if self.connection!=None:
            self.connection.close()

    def getSearchedProduct(self,value):
        cursor = None
        try:
            if self.connection != None:
                cursor = self.connection.cursor()
                query = "SELECT * FROM products where pAppStatus = 1 and pblockStatus = 0 and (pType LIKE %s or pName LIKE %s)"
                args = ("%"+value+"%","%"+value+"%")
                cursor.execute(query, args)
                check = cursor.fetchall()
                if check != None:
                    return check
                else:
                    check=[]
                    return check
        except Exception as e:
            print("Error in getElectronics()", str(e))
        finally:
            if cursor != None:
                cursor.close()
    
    def getCartId(self,email):
        cursor = None
        try:
            if self.connection != None:
                cursor = self.connection.cursor()
                query = "select cart.cartId from cart, buyer where cart.byrid = buyer.buyerId and buyer.buyerEmail = %s"
                args = (email)
                cursor.execute(query, args)
                check = cursor.fetchone()
                if check != None:
                    return check[0]
                else:
                    check=[]
                    return check
        except Exception as e:
            print("Error in getCartProduct()", str(e))
        finally:
            if cursor != None:
                cursor.close()
    
    def addToCart(self,cid,pid,pqnt):
        cursor = None
        try:
            if self.connection != None:
                cursor = self.connection.cursor()
                query = "insert into cartproduct(cid,productId,prdQuantity) value(%s,%s,%s)"
                args = (cid,pid,pqnt)
                cursor.execute(query, args)
                self.connection.commit()
                return True
            else:
                return False
        except Exception as e:
            print("Error in addToCart()", str(e))
            return False
        finally:
            if cursor != None:
                cursor.close()

                
    def deleteFromCart(self,cpid):
        cursor = None
        try:
            if self.connection != None:
                cursor = self.connection.cursor()
                query = "delete from cartproduct where cpid=%s"
                args = (cpid)
                cursor.execute(query, args)
                self.connection.commit()
                return "1"
            else:
                return False
        except Exception as e:
            print("Error in addToCart()", str(e))
            return False
        finally:
            if cursor != None:
                cursor.close()

    def deleteFromStock(self,pid,pqnt):
        cursor = None
        try:
            if self.connection != None:
                cursor = self.connection.cursor()
                query = "update products set pStock = pStock-%s where productId=%s"
                args = (pqnt,pid)
                cursor.execute(query, args)
                self.connection.commit()
                return True
            else:
                return False
        except Exception as e:
            print("Error in deleteFromStock()", str(e))
            return False
        finally:
            if cursor != None:
                cursor.close()

    def addToStock(self,pid,pqnt):
        cursor = None
        try:
            if self.connection != None:
                cursor = self.connection.cursor()
                query = "update products set pStock = pStock+%s where productId=%s"
                args = (pqnt,pid)
                cursor.execute(query, args)
                self.connection.commit()
                return True
            else:
                return False
        except Exception as e:
            print("Error in addToStock()", str(e))
            return False
        finally:
            if cursor != None:
                cursor.close()
    
    def getCartProduct(self,cid):
        cursor = None
        try:
            if self.connection != None:
                cursor = self.connection.cursor()
                query = "select products.pImages, products.pName, products.pPrice, cartproduct.prdQuantity,cartproduct.cpid, products.pPrice*cartproduct.prdQuantity as total, products.productId from products, cartproduct where products.productId = cartproduct.productId and cartproduct.cid=%s"
                args = (cid)
                cursor.execute(query, args)
                check = cursor.fetchall()
                if check != None:
                    return check
                else:
                    check=[]
                    return check
        except Exception as e:
            print("Error in getCartProduct()", str(e))
        finally:
            if cursor != None:
                cursor.close()
    
    def getSumPrice(self,cid):
        cursor = None
        try:
            if self.connection != None:
                cursor = self.connection.cursor()
                query = "select sum(products.pPrice*cartproduct.prdQuantity) as total from products, cartproduct where products.productId = cartproduct.productId and cartproduct.cid=%s"
                args = (cid)
                cursor.execute(query, args)
                check = cursor.fetchone()
                if check != None:
                    return check[0]
                else:
                    check=[]
                    return check
        except Exception as e:
            print("Error in getSumPrice()", str(e))
        finally:
            if cursor != None:
                cursor.close()

    
    def updateCheckStatus(self,cid):
        cursor=None
        try:
            if self.connection!=None:
                cursor = self.connection.cursor()
                query = "uodate cart set ChkOutStatus = 1 where cartId = %s"
                args = (cid)
                cursor.execute(query, args)
                self.connection.commit()
                return True
            else:
                return False
        except Exception as e:
            print("Exception in updateCheckStatus. ", str(e))
            return False
        finally:
            if cursor!=None:
                cursor.close()
    
    def insertCheckout(self,cid,d,a,s):
        cursor = None
        try:
            if self.connection!=None:
                cursor = self.connection.cursor()
                query = "insert into checkout (cartId,cartDate,address,deliveryStatus) values (%s,%s,%s,%s)"
                args = (cid,d,a,s)
                cursor.execute(query, args)
                self.connection.commit()
                return True
            else:
                return False
        except Exception as e:
            print("Exception in insertCheckout. ", str(e))
            return False
        finally:
            if cursor!=None:
                cursor.close()

    def createCart(self,bid):
        cursor = None
        try:
            if self.connection!=None:
                cursor = self.connection.cursor()
                query = "insert into cart (cartId, byrid, ChkOutStatus) values (%s,%s,%s)"
                args = (bid,bid,0)
                cursor.execute(query, args)
                self.connection.commit()
                return True
            else:
                return False
        except Exception as e:
            print("Exception in insertUser. ", str(e))
            return False
        finally:
            if cursor!=None:
                cursor.close()
    
    def getBuyerMaxID(self):
        cursor = None
        try:
            if self.connection != None:
                cursor = self.connection.cursor()
                cursor.execute("select max(buyerId) from buyer")
                return cursor.fetchone()[0]
        except Exception as e:
            print("Exception in getProductMaxID", str(e))
        finally:
            if cursor != None:
                cursor.close()
                
    def getSellerMaxID(self):
        cursor = None
        try:
            if self.connection != None:
                cursor = self.connection.cursor()
                cursor.execute("select max(sellerid) from seller")
                return cursor.fetchone()[0]
        except Exception as e:
            print("Exception in getProductMaxID", str(e))
        finally:
            if cursor != None:
                cursor.close()
    
    def checkUserExist(self, user):
        cursor = None
        try:
            if self.connection!=None:
                cursor = self.connection.cursor()
                cursor.execute("select buyerEmail from buyer")
                emailList = cursor.fetchall()
                # print(emailList)
                for e in emailList:
                    if user.email == e[0]:
                        return True
                return False
        except Exception as e:
            print("Exception in checkUserExist",str(e))
        finally:
            if cursor!=None:
                cursor.close()

    def insertBuyer(self,user):
        cursor = None
        try:
            if self.connection!=None:
                cursor = self.connection.cursor()
                query = "insert into buyer (buyerName,buyerEmail,buyerGender,buyerDOB, buyerPswd,buyerPic) values (%s,%s,%s,%s,%s,%s)"
                args = ( user.name, user.email,user.gender,user.dob, user.pswrd,user.pic)
                cursor.execute(query, args)
                self.connection.commit()
                return True
            else:
                return False
        except Exception as e:
            print("Exception in insertUser. ", str(e))
            return False
        finally:
            if cursor!=None:
                cursor.close()

    def loginBuyer(self, user):
        cursor = None
        try:
            if self.connection != None:
                cursor = self.connection.cursor()
                query = "Select buyerEmail,buyerPswd from buyer where buyerEmail=%s and buyerPswd=%s"
                args = (user.email, user.pswrd)
                cursor.execute(query, args)
                record = cursor.fetchone()
                if record[0] == user.email and record[1] == user.pswrd:
                    return True
                else:
                    return False
            else:
                return False
        except Exception as e:
            return False
            print("Exception in loginBuyer()", str(e))
        finally:
            if cursor != None:
                cursor.close()
    
    def loginSeller(self, user):
        cursor = None
        try:
            if self.connection != None:
                cursor = self.connection.cursor()
                query = "Select sellerEmail,sellerPswd from seller where sellerEmail=%s and sellerPswd=%s"
                args = (user.email, user.pswrd)
                cursor.execute(query, args)
                record = cursor.fetchone()
                if record[0] == user.email and record[1] == user.pswrd:
                    return True
                else:
                    return False
            else:
                return False
        except Exception as e:
            return False
            print("Exception in loginBuyer()", str(e))
        finally:
            if cursor != None:
                cursor.close()
            
    def getElectronics(self, aps,bls):
        cursor = None
        try:
            if self.connection != None:
                cursor = self.connection.cursor()
                query = "SELECT pName,pDescription,pPrice,pStock,pImages,products.sellerId,pClick,productId FROM products ,seller where pAppStatus = %s and pblockStatus=%s and seller.blockStatus=0 and seller.sellerId = products.sellerId  and (pType='Phones' or pType='Tablets' or pType='Laptops' or pType='Desktop' or pType='Cameras & Drones' or pType='Smart Watches' or pType='Gaming Consoles')"
                args = (aps,bls)
                cursor.execute(query, args)
                check = cursor.fetchall()
                if check != None:
                    return check
                else:
                    check=[]
                    return check
        except Exception as e:
            print("Error in getElectronics()", str(e))
        finally:
            if cursor != None:
                cursor.close()

    def getHomeAppliances(self, aps,bls):
        cursor = None
        try:
            if self.connection != None:
                cursor = self.connection.cursor()    
                query = "SELECT pName,pDescription,pPrice,pStock,pImages,products.sellerId,pClick,productId FROM products ,seller where pAppStatus = %s and pblockStatus=%s and seller.blockStatus=0 and seller.sellerId = products.sellerId  and (pType='Smart TV' or pType='Home Audio' or pType='Kitchen Appliances' or pType='Cooling & Heating' or pType='Floor Care' or pType='Generators' or pType='Washers & Dryers')"
                args = (aps,bls)
                cursor.execute(query, args)
                check = cursor.fetchall()
                if check != None:
                    return check
                else:
                    check=[]
                    return check
        except Exception as e:
            print("Error in getHomeAppliances()", str(e))
        finally:
            if cursor != None:
                cursor.close()

    def getHealth(self, aps,bls):
        cursor = None
        try:
            if self.connection != None:
                cursor = self.connection.cursor()
                query = "SELECT pName,pDescription,pPrice,pStock,pImages,products.sellerId,pClick,productId FROM products ,seller where pAppStatus = %s and pblockStatus=%s and seller.blockStatus=0 and seller.sellerId = products.sellerId  and (pType='Fragrances' or pType='Hair Care' or pType='Mens Care' or pType='Skin Care' or pType='Makeup' or pType='Medical Supplies' or pType='Beauty Tools')"
                args = (aps,bls)
                cursor.execute(query, args)
                check = cursor.fetchall()
                if check != None:
                    return check
                else:
                    check=[]
                    return check
        except Exception as e:
            print("Error in getHealth()", str(e))
        finally:
            if cursor != None:
                cursor.close()

    def getGroceries(self, aps,bls):
        cursor = None
        try:
            if self.connection != None:
                cursor = self.connection.cursor()
                query = "SELECT pName,pDescription,pPrice,pStock,pImages,products.sellerId,pClick,productId FROM products ,seller where pAppStatus = %s and pblockStatus=%s and seller.blockStatus=0 and seller.sellerId = products.sellerId  and (pType='Bevarages' or pType='Fresh Products' or pType='Snacks' or pType='Food Staples' or pType='Dairy & Chilled' or pType='Frozen Food')"
                args = (aps,bls)
                cursor.execute(query, args)
                check = cursor.fetchall()
                if check != None:
                    return check
                else:
                    check=[]
                    return check
        except Exception as e:
            print("Error in getGroceries()", str(e))
        finally:
            if cursor != None:
                cursor.close()

    def getFashon(self, aps,bls):
        cursor = None
        try:
            if self.connection != None:
                cursor = self.connection.cursor()
                query = "SELECT pName,pDescription,pPrice,pStock,pImages,products.sellerId,pClick,productId FROM products ,seller where pAppStatus = %s and pblockStatus=%s and seller.blockStatus=0 and seller.sellerId = products.sellerId  and (pType='Mens Fashon' or pType='Womens Fashon' or pType='Winter Clothing' or pType='Summer Clothing' or pType='Inner Wear' or pType='Shoes')"
                args = (aps,bls)
                cursor.execute(query, args)
                check = cursor.fetchall()
                if check != None:
                    return check
                else:
                    check=[]
                    return check
        except Exception as e:
            print("Error in getFashon()", str(e))
        finally:
            if cursor != None:
                cursor.close()

    def getAutomobile(self, aps,bls):
        cursor = None
        try:
            if self.connection != None:
                cursor = self.connection.cursor()
                query = "SELECT pName,pDescription,pPrice,pStock,pImages,products.sellerId,pClick,productId FROM products ,seller where pAppStatus = %s and pblockStatus=%s and seller.blockStatus=0 and seller.sellerId = products.sellerId  and (pType='Accessories' or pType='Motorcycles' or pType='Cars' or pType='Rikshas' or pType='Loaders' or pType='Sports Bikes' or pType='Helmets' or pType='Riding Gears')"
                args = (aps,bls)
                cursor.execute(query, args)
                check = cursor.fetchall()
                if check != None:
                    return check
                else:
                    check=[]
                    return check
        except Exception as e:
            print("Error in getAutomobile()", str(e))
        finally:
            if cursor != None:
                cursor.close()

                
    
    def getOneProduct(self, pid):
        cursor = None
        try:
            if self.connection != None:
                cursor = self.connection.cursor()
                query = "SELECT * FROM products where productId = %s and pAppStatus = 1 and pblockStatus=0"
                args = (pid)
                cursor.execute(query, args)
                check = cursor.fetchall()
                if check != None:
                    return check
                else:
                    check=[]
                    return check
        except Exception as e:
            print("Error in getAutomobile()", str(e))
        finally:
            if cursor != None:
                cursor.close()

    def getRelatedProducts(self, pid):
        cursor = None
        try:
            if self.connection != None:
                cursor = self.connection.cursor()
                query = "SELECT pType FROM products where productId = %s and pAppStatus = 1 and pblockStatus=0"
                args = (pid)
                cursor.execute(query, args)
                check = cursor.fetchone()
                query = "SELECT * FROM products where pType = %s and pAppStatus = 1 and pblockStatus=0"
                args = (check[0])
                cursor.execute(query, args)
                check = cursor.fetchall()
                if check != None:
                    return check
                else:
                    check=[]
                    return check
        except Exception as e:
            print("Error in getRelatedProducts()", str(e))
        finally:
            if cursor != None:
                cursor.close()
    
    def getPhones(self):
        cursor = None
        try:
            if self.connection != None:
                cursor = self.connection.cursor()
                query = "SELECT * FROM products where pType='Phones' and pAppStatus = 1 and pblockStatus=0"
                cursor.execute(query)
                check = cursor.fetchall()
                if check != None:
                    return check
                else:
                    check=[]
                    return check
        except Exception as e:
            print("Error in getPhones()", str(e))
        finally:
            if cursor != None:
                cursor.close()

    def getTablets(self):
        cursor = None
        try:
            if self.connection != None:
                cursor = self.connection.cursor()
                query = "SELECT * FROM products where pType='Tablets' and pAppStatus = 1 and pblockStatus=0"
                cursor.execute(query)
                check = cursor.fetchall()
                if check != None:
                    return check
                else:
                    check=[]
                    return check
        except Exception as e:
            print("Error in getTablets()", str(e))
        finally:
            if cursor != None:
                cursor.close()

    def getLaptops(self):
        cursor = None
        try:
            if self.connection != None:
                cursor = self.connection.cursor()
                query = "SELECT * FROM products where pType='Laptops' and pAppStatus = 1 and pblockStatus=0"
                cursor.execute(query)
                check = cursor.fetchall()
                if check != None:
                    return check
                else:
                    check=[]
                    return check
        except Exception as e:
            print("Error in getLaptops()", str(e))
        finally:
            if cursor != None:
                cursor.close()
    
    def getDesktop(self):
        cursor = None
        try:
            if self.connection != None:
                cursor = self.connection.cursor()
                query = "SELECT * FROM products where pType='Desktop' and pAppStatus = 1 and pblockStatus=0"
                cursor.execute(query)
                check = cursor.fetchall()
                if check != None:
                    return check
                else:
                    check=[]
                    return check
        except Exception as e:
            print("Error in getDesktop()", str(e))
        finally:
            if cursor != None:
                cursor.close()

    def getCamDrones(self):
        cursor = None
        try:
            if self.connection != None:
                cursor = self.connection.cursor()
                query = "SELECT * FROM products where pType='Cameras & Drones' and pAppStatus = 1 and pblockStatus=0"
                cursor.execute(query)
                check = cursor.fetchall()
                if check != None:
                    return check
                else:
                    check=[]
                    return check
        except Exception as e:
            print("Error in getCamDrones()", str(e))
        finally:
            if cursor != None:
                cursor.close()

    def getSmartWatches(self):
        cursor = None
        try:
            if self.connection != None:
                cursor = self.connection.cursor()
                query = "SELECT * FROM products where pType='Smart Watches' and pAppStatus = 1 and pblockStatus=0"
                cursor.execute(query)
                check = cursor.fetchall()
                if check != None:
                    return check
                else:
                    check=[]
                    return check
        except Exception as e:
            print("Error in getSmartWatches()", str(e))
        finally:
            if cursor != None:
                cursor.close()

    def getGamingConsloes(self):
        cursor = None
        try:
            if self.connection != None:
                cursor = self.connection.cursor()
                query = "SELECT * FROM products where pType='Gaming Consoles' and pAppStatus = 1 and pblockStatus=0"
                cursor.execute(query)
                check = cursor.fetchall()
                if check != None:
                    return check
                else:
                    check=[]
                    return check
        except Exception as e:
            print("Error in getGamingConsloes()", str(e))
        finally:
            if cursor != None:
                cursor.close()
    
    def getSmartTV(self):
        cursor = None
        try:
            if self.connection != None:
                cursor = self.connection.cursor()
                query = "SELECT * FROM products where pType='Smart TV' and pAppStatus = 1 and pblockStatus=0"
                cursor.execute(query)
                check = cursor.fetchall()
                if check != None:
                    return check
                else:
                    check=[]
                    return check
        except Exception as e:
            print("Error in getSmartTV()", str(e))
        finally:
            if cursor != None:
                cursor.close()

    def getHomeAudio(self):
        cursor = None
        try:
            if self.connection != None:
                cursor = self.connection.cursor()
                query = "SELECT * FROM products where pType='Home Audio' and pAppStatus = 1 and pblockStatus=0"
                cursor.execute(query)
                check = cursor.fetchall()
                if check != None:
                    return check
                else:
                    check=[]
                    return check
        except Exception as e:
            print("Error in getHomeAudio()", str(e))
        finally:
            if cursor != None:
                cursor.close()

    def getKitchenAppliances(self):
        cursor = None
        try:
            if self.connection != None:
                cursor = self.connection.cursor()
                query = "SELECT * FROM products where pType='Kitchen Appliances' and pAppStatus = 1 and pblockStatus=0"
                cursor.execute(query)
                check = cursor.fetchall()
                if check != None:
                    return check
                else:
                    check=[]
                    return check
        except Exception as e:
            print("Error in getKitchenAppliances()", str(e))
        finally:
            if cursor != None:
                cursor.close()

    def getCoolingAndHeating(self):
        cursor = None
        try:
            if self.connection != None:
                cursor = self.connection.cursor()
                query = "SELECT * FROM products where pType='Cooling & Heating' and pAppStatus = 1 and pblockStatus=0"
                cursor.execute(query)
                check = cursor.fetchall()
                if check != None:
                    return check
                else:
                    check=[]
                    return check
        except Exception as e:
            print("Error in getCoolingAndHeating()", str(e))
        finally:
            if cursor != None:
                cursor.close()

    def getFloorCare(self):
        cursor = None
        try:
            if self.connection != None:
                cursor = self.connection.cursor()
                query = "SELECT * FROM products where pType='Floor Care' and pAppStatus = 1 and pblockStatus=0"
                cursor.execute(query)
                check = cursor.fetchall()
                if check != None:
                    return check
                else:
                    check=[]
                    return check
        except Exception as e:
            print("Error in getFloorCare()", str(e))
        finally:
            if cursor != None:
                cursor.close()

    def getGenerators(self):
        cursor = None
        try:
            if self.connection != None:
                cursor = self.connection.cursor()
                query = "SELECT * FROM products where pType='Generatos' and pAppStatus = 1 and pblockStatus=0"
                cursor.execute(query)
                check = cursor.fetchall()
                if check != None:
                    return check
                else:
                    check=[]
                    return check
        except Exception as e:
            print("Error in getGenerators()", str(e))
        finally:
            if cursor != None:
                cursor.close()

    def getWashersDryers(self):
        cursor = None
        try:
            if self.connection != None:
                cursor = self.connection.cursor()
                query = "SELECT * FROM products where pType='Washers & Dryers' and pAppStatus = 1 and pblockStatus=0"
                cursor.execute(query)
                check = cursor.fetchall()
                if check != None:
                    return check
                else:
                    check=[]
                    return check
        except Exception as e:
            print("Error in getWashersDryers()", str(e))
        finally:
            if cursor != None:
                cursor.close()

    def getFragrances(self):
        cursor = None
        try:
            if self.connection != None:
                cursor = self.connection.cursor()
                query = "SELECT * FROM products where pType='Fragrances' and pAppStatus = 1 and pblockStatus=0"
                cursor.execute(query)
                check = cursor.fetchall()
                if check != None:
                    return check
                else:
                    check=[]
                    return check
        except Exception as e:
            print("Error in getFragrances()", str(e))
        finally:
            if cursor != None:
                cursor.close()
    
    def getHairCare(self):
        cursor = None
        try:
            if self.connection != None:
                cursor = self.connection.cursor()
                query = "SELECT * FROM products where pType='Hair Care' and pAppStatus = 1 and pblockStatus=0"
                cursor.execute(query)
                check = cursor.fetchall()
                if check != None:
                    return check
                else:
                    check=[]
                    return check
        except Exception as e:
            print("Error in getHairCare()", str(e))
        finally:
            if cursor != None:
                cursor.close()

    def getMensCare(self):
        cursor = None
        try:
            if self.connection != None:
                cursor = self.connection.cursor()
                query = "SELECT * FROM products where pType='Mens Care' and pAppStatus = 1 and pblockStatus=0"
                cursor.execute(query)
                check = cursor.fetchall()
                if check != None:
                    return check
                else:
                    check=[]
                    return check
        except Exception as e:
            print("Error in getMensCare()", str(e))
        finally:
            if cursor != None:
                cursor.close()
    
    def getSkinCare(self):
        cursor = None
        try:
            if self.connection != None:
                cursor = self.connection.cursor()
                query = "SELECT * FROM products where pType='Skin Care' and pAppStatus = 1 and pblockStatus=0"
                cursor.execute(query)
                check = cursor.fetchall()
                if check != None:
                    return check
                else:
                    check=[]
                    return check
        except Exception as e:
            print("Error in getSkinCare()", str(e))
        finally:
            if cursor != None:
                cursor.close()
    
    def getMakeup(self):
        cursor = None
        try:
            if self.connection != None:
                cursor = self.connection.cursor()
                query = "SELECT * FROM products where pType='Makeup' and pAppStatus = 1 and pblockStatus=0"
                cursor.execute(query)
                check = cursor.fetchall()
                if check != None:
                    return check
                else:
                    check=[]
                    return check
        except Exception as e:
            print("Error in getMakeup()", str(e))
        finally:
            if cursor != None:
                cursor.close()
    
    def getMedicalSupplies(self):
        cursor = None
        try:
            if self.connection != None:
                cursor = self.connection.cursor()
                query = "SELECT * FROM products where pType='Medical Supplies' and pAppStatus = 1 and pblockStatus=0"
                cursor.execute(query)
                check = cursor.fetchall()
                if check != None:
                    return check
                else:
                    check=[]
                    return check
        except Exception as e:
            print("Error in getMedicalSupplies()", str(e))
        finally:
            if cursor != None:
                cursor.close()
    
    def getBeautyTools(self):
        cursor = None
        try:
            if self.connection != None:
                cursor = self.connection.cursor()
                query = "SELECT * FROM products where pType='Beauty Tools' and pAppStatus = 1 and pblockStatus=0"
                cursor.execute(query)
                check = cursor.fetchall()
                if check != None:
                    return check
                else:
                    check=[]
                    return check
        except Exception as e:
            print("Error in getBeautyTools()", str(e))
        finally:
            if cursor != None:
                cursor.close()
    
    def getBevarages(self):
        cursor = None
        try:
            if self.connection != None:
                cursor = self.connection.cursor()
                query = "SELECT * FROM products where pType='Bevarages' and pAppStatus = 1 and pblockStatus=0"
                cursor.execute(query)
                check = cursor.fetchall()
                if check != None:
                    return check
                else:
                    check=[]
                    return check
        except Exception as e:
            print("Error in getBevarages()", str(e))
        finally:
            if cursor != None:
                cursor.close()
    
    def getFreshProducts(self):
        cursor = None
        try:
            if self.connection != None:
                cursor = self.connection.cursor()
                query = "SELECT * FROM products where pType='Fresh Products' and pAppStatus = 1 and pblockStatus=0"
                cursor.execute(query)
                check = cursor.fetchall()
                if check != None:
                    return check
                else:
                    check=[]
                    return check
        except Exception as e:
            print("Error in getFreshProducts()", str(e))
        finally:
            if cursor != None:
                cursor.close()
    
    def getSnacks(self):
        cursor = None
        try:
            if self.connection != None:
                cursor = self.connection.cursor()
                query = "SELECT * FROM products where pType='Snacks' and pAppStatus = 1 and pblockStatus=0"
                cursor.execute(query)
                check = cursor.fetchall()
                if check != None:
                    return check
                else:
                    check=[]
                    return check
        except Exception as e:
            print("Error in getSnacks()", str(e))
        finally:
            if cursor != None:
                cursor.close()
    
    def getFoodStaples(self):
        cursor = None
        try:
            if self.connection != None:
                cursor = self.connection.cursor()
                query = "SELECT * FROM products where pType='Food Staples' and pAppStatus = 1 and pblockStatus=0"
                cursor.execute(query)
                check = cursor.fetchall()
                if check != None:
                    return check
                else:
                    check=[]
                    return check
        except Exception as e:
            print("Error in getFoodStaples()", str(e))
        finally:
            if cursor != None:
                cursor.close()
    
    def getDairyChilled(self):
        cursor = None
        try:
            if self.connection != None:
                cursor = self.connection.cursor()
                query = "SELECT * FROM products where pType='Dairy & Chilled' and pAppStatus = 1 and pblockStatus=0"
                cursor.execute(query)
                check = cursor.fetchall()
                if check != None:
                    return check
                else:
                    check=[]
                    return check
        except Exception as e:
            print("Error in getDairyChilled()", str(e))
        finally:
            if cursor != None:
                cursor.close()
    
    def getFrozenFood(self):
        cursor = None
        try:
            if self.connection != None:
                cursor = self.connection.cursor()
                query = "SELECT * FROM products where pType='Frozen Food' and pAppStatus = 1 and pblockStatus=0"
                cursor.execute(query)
                check = cursor.fetchall()
                if check != None:
                    return check
                else:
                    check=[]
                    return check
        except Exception as e:
            print("Error in getFrozenFood()", str(e))
        finally:
            if cursor != None:
                cursor.close()
    
    def getMensFashon(self):
        cursor = None
        try:
            if self.connection != None:
                cursor = self.connection.cursor()
                query = "SELECT * FROM products where pType='Mens Fashon' and pAppStatus = 1 and pblockStatus=0"
                cursor.execute(query)
                check = cursor.fetchall()
                if check != None:
                    return check
                else:
                    check=[]
                    return check
        except Exception as e:
            print("Error in getMensFashon()", str(e))
        finally:
            if cursor != None:
                cursor.close()

    def getWomensFashon(self):
        cursor = None
        try:
            if self.connection != None:
                cursor = self.connection.cursor()
                query = "SELECT * FROM products where pType='Womens Fashon' and pAppStatus = 1 and pblockStatus=0"
                cursor.execute(query)
                check = cursor.fetchall()
                if check != None:
                    return check
                else:
                    check=[]
                    return check
        except Exception as e:
            print("Error in getWomensFashon()", str(e))
        finally:
            if cursor != None:
                cursor.close()
    
    def getWinterClothing(self):
        cursor = None
        try:
            if self.connection != None:
                cursor = self.connection.cursor()
                query = "SELECT * FROM products where pType='Winter Clothing' and pAppStatus = 1 and pblockStatus=0"
                cursor.execute(query)
                check = cursor.fetchall()
                if check != None:
                    return check
                else:
                    check=[]
                    return check
        except Exception as e:
            print("Error in getWinterClothing()", str(e))
        finally:
            if cursor != None:
                cursor.close()
    
    def getSummerClothing(self):
        cursor = None
        try:
            if self.connection != None:
                cursor = self.connection.cursor()
                query = "SELECT * FROM products where pType='Summer Clothing' and pAppStatus = 1 and pblockStatus=0"
                cursor.execute(query)
                check = cursor.fetchall()
                if check != None:
                    return check
                else:
                    check=[]
                    return check
        except Exception as e:
            print("Error in getSummerClothing()", str(e))
        finally:
            if cursor != None:
                cursor.close()
    
    def getInnerWear(self):
        cursor = None
        try:
            if self.connection != None:
                cursor = self.connection.cursor()
                query = "SELECT * FROM products where pType='Inner Wear' and pAppStatus = 1 and pblockStatus=0"
                cursor.execute(query)
                check = cursor.fetchall()
                if check != None:
                    return check
                else:
                    check=[]
                    return check
        except Exception as e:
            print("Error in getInnerWear()", str(e))
        finally:
            if cursor != None:
                cursor.close()
    
    def getShoes(self):
        cursor = None
        try:
            if self.connection != None:
                cursor = self.connection.cursor()
                query = "SELECT * FROM products where pType='Shoes' and pAppStatus = 1 and pblockStatus=0"
                cursor.execute(query)
                check = cursor.fetchall()
                if check != None:
                    return check
                else:
                    check=[]
                    return check
        except Exception as e:
            print("Error in getShoes()", str(e))
        finally:
            if cursor != None:
                cursor.close()

    def getAccessories(self):
        cursor = None
        try:
            if self.connection != None:
                cursor = self.connection.cursor()
                query = "SELECT * FROM products where pType='Accessories' and pAppStatus = 1 and pblockStatus=0"
                cursor.execute(query)
                check = cursor.fetchall()
                if check != None:
                    return check
                else:
                    check=[]
                    return check
        except Exception as e:
            print("Error in getAccessories()", str(e))
        finally:
            if cursor != None:
                cursor.close()
    
    def getMotorcycles(self):
        cursor = None
        try:
            if self.connection != None:
                cursor = self.connection.cursor()
                query = "SELECT * FROM products where pType='Motorcycles' and pAppStatus = 1 and pblockStatus=0"
                cursor.execute(query)
                check = cursor.fetchall()
                if check != None:
                    return check
                else:
                    check=[]
                    return check
        except Exception as e:
            print("Error in getMotorcycles()", str(e))
        finally:
            if cursor != None:
                cursor.close()
    
    def getCars(self):
        cursor = None
        try:
            if self.connection != None:
                cursor = self.connection.cursor()
                query = "SELECT * FROM products where pType='Cars' and pAppStatus = 1 and pblockStatus=0"
                cursor.execute(query)
                check = cursor.fetchall()
                if check != None:
                    return check
                else:
                    check=[]
                    return check
        except Exception as e:
            print("Error in getCars()", str(e))
        finally:
            if cursor != None:
                cursor.close()
    
    def getRikshas(self):
        cursor = None
        try:
            if self.connection != None:
                cursor = self.connection.cursor()
                query = "SELECT * FROM products where pType='Rikshas' and pAppStatus = 1 and pblockStatus=0"
                cursor.execute(query)
                check = cursor.fetchall()
                if check != None:
                    return check
                else:
                    check=[]
                    return check
        except Exception as e:
            print("Error in getRikshas()", str(e))
        finally:
            if cursor != None:
                cursor.close()

    def getLoaders(self):
        cursor = None
        try:
            if self.connection != None:
                cursor = self.connection.cursor()
                query = "SELECT * FROM products where pType='Loaders' and pAppStatus = 1 and pblockStatus=0"
                cursor.execute(query)
                check = cursor.fetchall()
                if check != None:
                    return check
                else:
                    check=[]
                    return check
        except Exception as e:
            print("Error in getLoaders()", str(e))
        finally:
            if cursor != None:
                cursor.close()
    
    def getSportsBike(self):
        cursor = None
        try:
            if self.connection != None:
                cursor = self.connection.cursor()
                query = "SELECT * FROM products where pType='Sports Bikes' and pAppStatus = 1 and pblockStatus=0"
                cursor.execute(query)
                check = cursor.fetchall()
                if check != None:
                    return check
                else:
                    check=[]
                    return check
        except Exception as e:
            print("Error in getSportsBike()", str(e))
        finally:
            if cursor != None:
                cursor.close()
    
    def getHelmets(self):
        cursor = None
        try:
            if self.connection != None:
                cursor = self.connection.cursor()
                query = "SELECT * FROM products where pType='Helmets' and pAppStatus = 1 and pblockStatus=0"
                cursor.execute(query)
                check = cursor.fetchall()
                if check != None:
                    return check
                else:
                    check=[]
                    return check
        except Exception as e:
            print("Error in getHelmets()", str(e))
        finally:
            if cursor != None:
                cursor.close()
    
    def getRidingGears(self):
        cursor = None
        try:
            if self.connection != None:
                cursor = self.connection.cursor()
                query = "SELECT * FROM products where pType='Riding Gears' and pAppStatus = 1 and pblockStatus=0"
                cursor.execute(query)
                check = cursor.fetchall()
                if check != None:
                    return check
                else:
                    check=[]
                    return check
        except Exception as e:
            print("Error in getRidingGears()", str(e))
        finally:
            if cursor != None:
                cursor.close()
                
                            
    # admin MODEL
    
    



    
    
    
    




    

    
    
    def insertSeller(self,name,email,pswrd,gender,address,category,newFileName):
        cursor = None
        try:
            if self.connection != None:
                cursor = self.connection.cursor()
                query = "insert into seller (sellerName,sellerEmail,sellerPswd,sellerGender,sellerAddress,sellerCategory,sellerPic) values (%s,%s,%s,%s,%s,%s,%s)"
                args = (name,email,pswrd,gender,address,category,newFileName)
                cursor.execute(query, args)
                self.connection.commit()
        except Exception as e:
            print("Exception in insertSeller", str(e))
        finally:
            if cursor != None:
                cursor.close()
        # next






    def loginAdmin(self, admin):
        cursor = None
        try:
            if self.connection != None:
                cursor = self.connection.cursor()
                print(admin.email,admin.pswrd)
                cursor.execute("select adminEmail, adminPswd from admin where adminEmail=%s and adminPswd=%s",(admin.email,admin.pswrd))
                user = cursor.fetchone()
                if user:
                    return True
                return False
        except Exception as e:
            print("Exception in loginAdmin", str(e))
        finally:
            if cursor != None:
                cursor.close()


    def getAdminId(self, admin):
        cursor = None
        try:
            if self.connection != None:
                cursor = self.connection.cursor()
                query = "select adminId from admin where adminEmail = %s;"
                args = (admin.email)
                cursor.execute(query, args)
                check = cursor.fetchone()
                return check
        except Exception as e:
            print("Error in getadmiinId()", str(e))
        finally:
            if cursor != None:
                cursor.close()

    def getSellers(self, status):
        cursor = None
        try:
            if self.connection != None:
                cursor = self.connection.cursor()
                query = "select sellerName, sellerEmail, sellerPswd , sellerGender , sellerAddress , sellerCategory , AppStatus , sellerPic , admin.adminName , sellerId from seller, admin where AppStatus = %s and blockStatus = 0 and seller.adminId = admin.adminId"
                args = (status)
                cursor.execute(query, args)
                check = cursor.fetchall()
                return check
        except Exception as e:
            print("Error in getSellers()", str(e))
        finally:
            if cursor != None:
                cursor.close()

    def getnewSellers(self, status, adminid):
        cursor = None
        try:
            if self.connection != None:
                cursor = self.connection.cursor()
                query = "select sellerName, sellerEmail, sellerPswd , sellerGender , sellerAddress , sellerCategory , AppStatus , sellerPic , admin.adminName , sellerId from seller, admin where AppStatus = %s and blockStatus = 0 and seller.adminId = admin.adminId"
                args = (status)
                cursor.execute(query, args)
                check = cursor.fetchall()
                return check
        except Exception as e:
            print("Error in getSellers()", str(e))
        finally:
            if cursor != None:
                cursor.close()

    def getBlockedSellers(self, status):
        cursor = None
        try:
            if self.connection != None:
                cursor = self.connection.cursor()
                query = "select sellerName, sellerEmail, sellerPswd , sellerGender , sellerAddress , sellerCategory , AppStatus , sellerPic , admin.adminName from seller, admin where AppStatus = 1 and blockStatus = %s and seller.adminId = admin.adminId"
                args = (status)
                cursor.execute(query, args)
                check = cursor.fetchall()
                return check
        except Exception as e:
            print("Error in getBlockedSellers()", str(e))
        finally:
            if cursor != None:
                cursor.close()

    def getSellerDetails(self,sEmail,status):
        cursor = None
        try:
            if self.connection != None:
                cursor = self.connection.cursor()
                query = "select sellerName, sellerEmail, sellerPswd , sellerGender , sellerAddress , sellerCategory , AppStatus , sellerPic , admin.adminName,sellerId from seller, admin where sellerEmail = %s and AppStatus = %s and seller.adminId = admin.adminId"
                args = (sEmail,status)
                cursor.execute(query, args)
                check = cursor.fetchone()
                return check
        except Exception as e:
            print("Error in getSellerDetails()", str(e))
        finally:
            if cursor != None:
                cursor.close()

    def getnewSellerDetails(self,sEmail,status):
        cursor = None
        try:
            if self.connection != None:
                cursor = self.connection.cursor()
                query = "select sellerName, sellerEmail, sellerPswd , sellerGender , sellerAddress , sellerCategory , AppStatus , sellerPic , admin.adminName,sellerId from seller, admin where sellerEmail = %s and AppStatus = %s"
                args = (sEmail,status)
                cursor.execute(query, args)
                check = cursor.fetchone()
                return check
        except Exception as e:
            print("Error in getSellerDetails()", str(e))
        finally:
            if cursor != None:
                cursor.close()

    def approveSeller(self,sEmail, adminid):
        cursor = None
        try:
            if self.connection != None:
                cursor = self.connection.cursor()
                query = "update seller set AppStatus = 1, adminId = %s where sellerEmail= %s;"
                args = (adminid, sEmail)
                cursor.execute(query, args)
                self.connection.commit()
                return True
            else:
                return False
        except Exception as e:
            print("Error in approveSeller()", str(e))
            return False
        finally:
            if cursor != None:
                cursor.close()


    def deleteAllFromCart(self,cid):
        cursor = None
        try:
            if self.connection!=None:
                cursor = self.connection.cursor()
                query = "delete from cartproduct where cid=%s"
                args = (cid)
                cursor.execute(query, args)
                self.connection.commit()
                return True
            else:
                return False
        except Exception as e:
            print("Exception in deleteAllFromCart. ", str(e))
            return False
        finally:
            if cursor!=None:
                cursor.close()


    def rejectSeller(self,sEmail):
        cursor = None
        try:
            if self.connection != None:
                cursor = self.connection.cursor()
                query = "delete from seller where sellerEmail= %s;"
                args = (sEmail)
                cursor.execute(query, args)
                self.connection.commit()
                return True
            else:
                return False
        except Exception as e:
            print("Error in rejectSeller()", str(e))
            return False
        finally:
            if cursor != None:
                cursor.close()

    def blockSeller(self,sellerID):
        cursor = None
        try:
            if self.connection != None:
                cursor = self.connection.cursor()
                query = "update seller set blockStatus = 1 where sellerEmail = %s;"
                args = (sellerID)
                cursor.execute(query, args)
                self.connection.commit()
                return True
            else:
                return False
        except Exception as e:
            print("Error in blockSeller()", str(e))
            return False
        finally:
            if cursor != None:
                cursor.close()

    def unblockSeller(self,sEmail):
        cursor = None
        try:
            if self.connection != None:
                cursor = self.connection.cursor()
                query = "update seller set blockStatus = 0 where sellerEmail= %s;"
                args = (sEmail)
                cursor.execute(query, args)
                self.connection.commit()
                return True
            else:
                return False
        except Exception as e:
            print("Error in blockSeller()", str(e))
            return False
        finally:
            if cursor != None:
                cursor.close()

    def getProducts(self, status):
        cursor = None
        try:
            if self.connection != None:
                cursor = self.connection.cursor()
                query = "select pName,categories.categoryName,subcategories.subcategory,pDescription,pPrice,pStock,pMainTag,pImages,seller.sellerName,seller.sellerEmail,products.productId from products,seller,categories,subcategories where categories.catId=subcategories.catid and pAppStatus=%s and pblockStatus=0 and seller.sellerId = products.sellerId and products.pType = subcategories.subcategory"
                args = (status)
                cursor.execute(query, args)
                check = cursor.fetchall()
                return check
        except Exception as e:
            print("Error in getProducts()", str(e))
        finally:
            if cursor != None:
                cursor.close()

    def getblockProducts(self, status):
        cursor = None
        try:
            if self.connection != None:
                cursor = self.connection.cursor()
                query = "select pName,categories.categoryName,subcategories.subcategory,pDescription,pPrice,pStock,pMainTag,pImages,seller.sellerName,seller.sellerEmail,products.productId from products,seller,categories,subcategories where categories.catId=subcategories.catid and pblockStatus = %s and pAppStatus = 1 and seller.sellerId = products.sellerId and products.pType = subcategories.subcategory"
                args = (status)
                cursor.execute(query, args)
                check = cursor.fetchall()
                return check
        except Exception as e:
            print("Error in getProducts()", str(e))
        finally:
            if cursor != None:
                cursor.close()

    def getProductDetails(self, proId, status):
        cursor = None
        try:
            if self.connection != None:
                cursor = self.connection.cursor()
                query = "select pName,categories.categoryName,subcategories.subcategory,pDescription,pPrice,pStock,pMainTag,pImages,seller.sellerName,seller.sellerEmail,products.productId from products,seller,categories,subcategories where categories.catId=subcategories.catid and productId=%s and pAppStatus=%s and seller.sellerId = products.sellerId and products.pType = subcategories.subcategory"
                args = (proId,status)
                cursor.execute(query, args)
                check = cursor.fetchone()
                return check
        except Exception as e:
            print("Error in getSellerDetails()", str(e))
        finally:
            if cursor != None:
                cursor.close()

    def approveProduct(self,pid):
        cursor = None
        try:
            if self.connection != None:
                cursor = self.connection.cursor()
                query = "update products set pAppStatus = 1 where productId= %s;"
                args = (pid)
                cursor.execute(query, args)
                self.connection.commit()
                return True
            else:
                return False
        except Exception as e:
            print("Error in approveProduct()", str(e))
            return False
        finally:
            if cursor != None:
                cursor.close()

    def deleteProduct(self,pid):
        cursor = None
        try:
            if self.connection != None:
                cursor = self.connection.cursor()
                query = "update products set pblockStatus= 1 where productId=%s;"
                args = (pid)
                cursor.execute(query, args)
                self.connection.commit()
                return True
            else:
                return False
        except Exception as e:
            print("Error in deleteProduct()", str(e))
            return False
        finally:
            if cursor != None:
                cursor.close()

    def unblockProduct(self,pid):
        cursor = None
        try:
            if self.connection != None:
                cursor = self.connection.cursor()
                query = "update products set pblockStatus = 0 where productId=%s;"
                args = (pid)
                cursor.execute(query, args)
                self.connection.commit()
                return True
            else:
                return False
        except Exception as e:
            print("Error in unblockProduct()", str(e))
            return False
        finally:
            if cursor != None:
                cursor.close()

    def checkCategoryExist(self,category):
        cursor=None
        flag=False
        try:
            if self.connection!=None:
                cursor = self.connection.cursor()
                query = "select categoryName from categories where categoryName=%s;"
                args = ((category).lower())
                cursor.execute(query,args)
                if cursor.fetchone():
                    flag = True
        except Exception as e:
            print("Exception in checkCategoryExist: ", str(e))
        finally:
            if cursor!=None:
                cursor.close()
                return flag 
    
    def addNewCategory(self,category):
        cursor = None
        try:
            if self.connection != None:
                cursor = self.connection.cursor()
                query = "insert into categories (categoryName) values (%s)"
                args = (category.lower())
                cursor.execute(query, args)
                self.connection.commit()
        except Exception as e:
            print("Exception in addNewCategory", str(e))
        finally:
            if cursor != None:
                cursor.close()
    
    def getCategories(self):
        try:
            if self.connection != None:
                cursor = self.connection.cursor()
                query = "select * from categories"
                cursor.execute(query)
                check = cursor.fetchall()
                return check
        except Exception as e:
            print("Error in getSellers()", e)
            
    
            
    def getCategoryID(self,category):
        try:
            if self.connection != None:
                cursor = self.connection.cursor()
                query = "select catid from categories where categroyName = %s"
                cursor.execute(query,(category))
                return cursor.fetchone()[0]
        except Exception as e:
            print("Error in getCategoryID()", e)

            
    def addNewSubCategory(self,id,subcategory):
        cursor = None
        try:
            if self.connection != None:
                cursor = self.connection.cursor()
                query = "insert into subcategories (catid,subcategory) values (%s,%s)"
                args = (id,subcategory.lower())
                cursor.execute(query, args)
                self.connection.commit()
        except Exception as e:
            print("Exception in addNewSubCategory", str(e))
        finally:
            if cursor != None:
                cursor.close()
                            
    def checkSubCategoryExist(self,subcategory):
        cursor=None
        flag = False
        try:
            if self.connection!=None:
                cursor = self.connection.cursor()
                query = "select subcategory from subcategories where subcategory=%s;"
                args = ((subcategory).lower())
                cursor.execute(query,args)
                if cursor.fetchone():
                    flag = True
        except Exception as e:
            print("Exception in checkSubCategoryExist: ", str(e))
        finally:
            if cursor!=None:
                cursor.close()
                return flag 
        # next
    def getTotalProductsCount(self):
        cursor=None
        
        try:
            if self.connection!=None:
                cursor = self.connection.cursor()
                query = "select count(*) from products;"
                cursor.execute(query)
                return cursor.fetchone()
        except Exception as e:
            print("Exception in getTotalProductsCount: ", str(e))
        finally:
            if cursor!=None:
                cursor.close()
         
            
    def getProductsCount(self,value):
        cursor=None
        
        try:
            if self.connection!=None:
                cursor = self.connection.cursor()
                query = "select count(*) from products where pAppStatus=%s;"
                cursor.execute(query,(value,))
                return cursor.fetchone()
        except Exception as e:
            print("Exception in getProducts: ", str(e))
        finally:
            if cursor!=None:
                cursor.close()
         
             
            
    def getBuyersCount(self):
        cursor=None
        
        try:
            if self.connection!=None:
                cursor = self.connection.cursor()
                query = "select count(*) from buyer;"
                cursor.execute(query)
                return cursor.fetchone()
        except Exception as e:
            print("Exception in getBuyersCount: ", str(e))
        finally:
            if cursor!=None:
                cursor.close()
        
            
            
    def getAllSellers(self):
        cursor=None
        try:
            if self.connection!=None:
                cursor = self.connection.cursor()
                query = "select count(*) from seller;"
                cursor.execute(query)
                return cursor.fetchone()
        except Exception as e:
            print("Exception in getAllSellers: ", str(e))
        finally:
            if cursor!=None:
                cursor.close()
        
            
            
    def getSellersCount(self,value):
        cursor=None
        try:
            if self.connection!=None:
                cursor = self.connection.cursor()
                query = "select count(*) from seller where AppStatus=%s and blockStatus = 0;"
                cursor.execute(query,(value,))
                return cursor.fetchone()
        except Exception as e:
            print("Exception in getSellers: ", str(e))
        finally:
            if cursor!=None:
                cursor.close()
        
            
            
    def getOrdersCount(self):
        cursor=None
        try:
            if self.connection!=None:
                cursor = self.connection.cursor()
                query = "select count(*) from checkout;"
                cursor.execute(query)
                return cursor.fetchone()
        except Exception as e:
            print("Exception in getSellers: ", str(e))
        finally:
            if cursor!=None:
                cursor.close()
        
    def getOrders(self):
        cursor=None
        try:
            if self.connection!=None:
                cursor = self.connection.cursor()
                query = "select count(*) from checkout ;"
                cursor.execute(query)
                return cursor.fetchone()
        except Exception as e:
            print("Exception in getSellers: ", str(e))
        finally:
            if cursor!=None:
                cursor.close()
    
    
    
    
    
    # search by chatha
    
    def getProbyCate(self,category):
        cursor = None
        try:
            if self.connection != None:
                cursor = self.connection.cursor()
                query = "select pName,categories.categoryName,subcategories.subcategory,pDescription,pPrice,pStock,pMainTag,pImages,seller.sellerName,seller.sellerEmail,products.productId from products,seller,categories,subcategories where categories.catId=subcategories.catid and pAppStatus=1 and pblockStatus=0 and seller.sellerId = products.sellerId and products.pType = subcategories.subcategory and categories.categoryName = %s;" 
                cursor.execute(query,(category))
                return cursor.fetchall()
        except Exception as e:
            print("Exception in getsellerdetail", str(e))
        finally:
            if cursor != None:
                cursor.close()

    
    def getProbySubCate(self,Subcategory):
        cursor = None
        try:
            if self.connection != None:
                cursor = self.connection.cursor()
                query = "select pName,categories.categoryName,subcategories.subcategory,pDescription,pPrice,pStock,pMainTag,pImages,seller.sellerName,seller.sellerEmail,products.productId from products,seller,categories,subcategories where categories.catId=subcategories.catid and pAppStatus=1 and pblockStatus=0 and seller.sellerId = products.sellerId and products.pType = subcategories.subcategory and subcategories.subcategory = %s;" 
                cursor.execute(query,(Subcategory))
                return cursor.fetchall()
        except Exception as e:
            print("Exception in getsellerdetail", str(e))
        finally:
            if cursor != None:
                cursor.close()



    def getAppProbyNameSearch(self,name):
        cursor = None
        try:
            if self.connection != None:
                cursor = self.connection.cursor()
                query = "select pName,categories.categoryName,subcategories.subcategory,pDescription,pPrice,pStock,pMainTag,pImages,seller.sellerName,seller.sellerEmail,products.productId from products,seller,categories,subcategories where categories.catId=subcategories.catid and pAppStatus=1 and pblockStatus=0 and seller.sellerId = products.sellerId and products.pType = subcategories.subcategory and products.pName LIKE %s;" 
                cursor.execute(query,("%"+name+"%"))
                return cursor.fetchall()
        except Exception as e:
            print("Exception in getsellerdetail", str(e))
        finally:
            if cursor != None:
                cursor.close()


    def getExisProbyName(self,name):
        cursor = None
        try:
            if self.connection != None:
                cursor = self.connection.cursor()
                query = "select pName,categories.categoryName,subcategories.subcategory,pDescription,pPrice,pStock,pMainTag,pImages,seller.sellerName,seller.sellerEmail,products.productId from products,seller,categories,subcategories where categories.catId=subcategories.catid and pAppStatus=0 and pblockStatus=0 and seller.sellerId = products.sellerId and products.pType = subcategories.subcategory and products.pName = %s;" 
                cursor.execute(query,(name))
                return cursor.fetchall()
        except Exception as e:
            print("Exception in getsellerdetail", str(e))
        finally:
            if cursor != None:
                cursor.close()


    
    def getNewSellerbyName(self,name):
        cursor = None
        try:
            if self.connection != None:
                cursor = self.connection.cursor()
                query = "select sellerName, sellerEmail, sellerPswd , sellerGender , sellerAddress , sellerCategory , AppStatus , sellerPic , admin.adminName,sellerId from seller, admin where AppStatus = 0 and seller.adminId = admin.adminId and sellerName = %s;" 
                cursor.execute(query,(name))
                return cursor.fetchall()
        except Exception as e:
            print("Exception in getsellerdetail", str(e))
        finally:
            if cursor != None:
                cursor.close()



    def getExisSellerbyName(self,name):
        cursor = None
        try:
            if self.connection != None:
                cursor = self.connection.cursor()
                query = "select sellerName, sellerEmail, sellerPswd , sellerGender , sellerAddress , sellerCategory , AppStatus , sellerPic , admin.adminName,sellerId from seller, admin where AppStatus = 1 and seller.adminId = admin.adminId and sellerName LIKE %s;" 
                cursor.execute(query,("%"+name+"%"))
                return cursor.fetchall()
        except Exception as e:
            print("Exception in getsellerdetail", str(e))
        finally:
            if cursor != None:
                cursor.close()    
    
    
    # seller App
    
    
    def loginSellerS(self, seller):
        cursor = None
        try:
            if self.connection != None:
                cursor = self.connection.cursor()
                cursor.execute("select sellerEmail, sellerPswd,sellerId,sellerName,sellerPic,sellerCategory from seller where AppStatus=1 ")
                emailList = cursor.fetchall()
                for e in emailList:
                    if seller.email == e[0] and seller.password == e[1]:
                        return e
                return False
        except Exception as e:
            print("Exception in loginSeller", str(e))
        finally:
            if cursor != None:
                cursor.close()           
            
    
    def getCategoryId(self,category):
        cursor = None
        try:
            if self.connection != None:
                cursor = self.connection.cursor()
                query = "select catId from categories where categoryName=%s"
                cursor.execute(query,(category))                
                catID = cursor.fetchone()
                print(catID[0])
                return catID[0]
        except Exception as e:
            print("Exception in getCategoryId", str(e))
        finally:
            if cursor != None:
                cursor.close()
                
        
    def getSubCategories(self,catID):
        cursor = None
        try:
            if self.connection != None:
                cursor = self.connection.cursor()
                query = "select subcategory from subcategories where catId=%s"
                cursor.execute(query,(catID))            
                subCategories = cursor.fetchall()
                return subCategories 
        except Exception as e:
            print("Exception in getSubCategories", str(e))
        finally:
            if cursor != None:
                cursor.close()
            
    def addProduct(self,Product):
        cursor = None
        try:
            if self.connection != None:
                cursor = self.connection.cursor()
                query = "insert into products (pName,pType,pDescription,pPrice,pStock,pMainTag,pImages,sellerID) values (%s,%s,%s,%s,%s,%s,%s,%s)"
                args = (Product.name,Product.pType,Product.pDescript,Product.price,Product.stock,Product.mainTag,Product.pImage,Product.sellerId)
                cursor.execute(query, args)
                self.connection.commit()
        except Exception as e:
            print("Exception in addNewCategory", str(e))
        finally:
            if cursor != None:
                cursor.close()
                
    def getProductMaxID(self):
        cursor = None
        try:
            if self.connection != None:
                cursor = self.connection.cursor()
                cursor.execute("select max(productId) from products ")
                return cursor.fetchone()[0]
        except Exception as e:
            print("Exception in getProductMaxID", str(e))
        finally:
            if cursor != None:
                cursor.close()
                
                
    def getSellerProducts(self, sellerid,status):
        cursor = None
        try:
            if self.connection != None:
                cursor = self.connection.cursor()
                query = "select * from products where sellerID=%s and pAppStatus=%s"
                cursor.execute(query,(sellerid,status))
                return cursor.fetchall()
        except Exception as e:
            print("Exception in getApprovedProducts", str(e))
        finally:
            if cursor != None:
                cursor.close()   


    # def deleteProduct(self, pid):
    #     cursor = None
    #     try:
    #         if self.connection != None:
    #             cursor = self.connection.cursor()
    #             query = "delete from products where productId=%s"
    #             cursor.execute(query,(pid))
    #             return cursor.fetchall()
    #     except Exception as e:
    #         print("Exception in getApprovedProducts", str(e))
    #     finally:
    #         if cursor != None:
    #             cursor.close()   

    def getOrdersS(self,sellerID,status):
        cursor = None
        try:
            if self.connection != None:
                cursor = self.connection.cursor()
                query=None
                if status != "Deliverd":
                    query = "select cart.cartID,products.pName, products.pType, cartproduct.prdQuantity, products.pPrice, products.pImages, buyer.buyerName, buyer.buyerEmail, checkout.cartDate, checkout.address from checkout, cart, products, buyer, cartproduct where products.productId = cartproduct.productId and buyer.buyerId = cart.byrid and (checkout.deliveryStatus = 'Picked by courier' or checkout.deliveryStatus = 'Order confirmed' or checkout.deliveryStatus = 'On the way')  and sellerId = %s and cart.cartId = cartproduct.cid and checkout.cartId=cart.cartId and ChkOutStatus = 1" 
                else:
                    query = "select cart.cartID,products.pName, products.pType, cartproduct.prdQuantity, products.pPrice, products.pImages, buyer.buyerName, buyer.buyerEmail, checkout.cartDate, checkout.address from checkout, cart, products, buyer, cartproduct where products.productId = cartproduct.productId and buyer.buyerId = cart.byrid and checkout.deliveryStatus = 'Deliverd'  and sellerId = %s and cart.cartId = cartproduct.cid and checkout.cartId=cart.cartId and ChkOutStatus = 1;"   
                cursor.execute(query,(sellerID))
                return cursor.fetchall()
        except Exception as e:
            print("Exception in getApprovedProducts", str(e))
        finally:
            if cursor != None:
                cursor.close()

    def changeCartStatus(self,cartID,status):
        cursor = None
        try:
            if self.connection != None:
                cursor = self.connection.cursor()
                query = "UPDATE checkout SET deliverystatus = %s WHERE cartID = %s"
                args = (status,cartID)
                cursor.execute(query, args)
                self.connection.commit()
        except Exception as e:
            print("Exception in addNewCategory", str(e))
        finally:
            if cursor != None:
                cursor.close()
                
                
                
    def getProduct(self,pid):
        cursor = None
        try:
            if self.connection != None:
                cursor = self.connection.cursor()
                query = "select * from products where productID=%s"
                cursor.execute(query,(pid))                
                product = cursor.fetchone()
                return product
        except Exception as e:
            print("Exception in getProduct", str(e))
        finally:
            if cursor != None:
                cursor.close()
                
    def updateProduct(self,pid,Product):
        cursor = None
        try:
            if self.connection != None:
                cursor = self.connection.cursor()
                query = "update products set pName = %s, pType=%s,pDescription=%s,pPrice=%s,pStock=%s,pMainTag=%s,pImages=%s,sellerID=%s where productID=%s"
                args = (Product.name,Product.pType,Product.pDescript,Product.price,Product.stock,Product.mainTag,Product.pImage,Product.sellerId,pid)
                cursor.execute(query, args)
                self.connection.commit()
        except Exception as e:
            print("Exception in addNewCategory", str(e))
        finally:
            if cursor != None:
                cursor.close()
                
                
                
    def getMyBuyers(self,sellerID):
        cursor = None
        try:
            if self.connection != None:
                cursor = self.connection.cursor()
                query = "select roomID from messages"
                cursor.execute(query) 
                buyers = []
                for roomID in cursor.fetchall():
                    if roomID[0].split(',')[1]==str(sellerID):
                        buyers.append(roomID[0].split(',')[0])
                return buyers
        except Exception as e:
            print("Exception in getCategoryId", str(e))
        finally:
            if cursor != None:
                cursor.close()
                
    def getBuyer(self,id):
        cursor = None
        try:
            if self.connection != None:
                cursor = self.connection.cursor()
                query = "select buyerID,buyerName,buyerPic from buyer where buyerID=%s"
                cursor.execute(query,(id))                
                return cursor.fetchone()
                
        except Exception as e:
            print("Exception in getBuyer", str(e))
        finally:
            if cursor != None:
                cursor.close()
                

    def getSeller(self,id):
        cursor = None
        try:
            if self.connection != None:
                cursor = self.connection.cursor()
                query = "select sellerID,sellerName,sellerPic from seller where sellerID=%s"
                cursor.execute(query,(id))                
                return cursor.fetchone()
        except Exception as e:
            print("Exception in getSeller", str(e))
        finally:
            if cursor != None:
                cursor.close()
                
                
                
                
    # sellderrrrr
    
    def addMessage(self,roomID,message,datetime,messageby):
        cursor = None
        try:
            if self.connection != None:
                cursor = self.connection.cursor()
                query = "insert into messages (roomID,message,datetime,messageby) values (%s,%s,%s,%s)"
                args = (roomID,message,datetime,messageby)
                cursor.execute(query, args)
                self.connection.commit()
        except Exception as e:
            print("Exception in addMessage", str(e))
        finally:
            if cursor != None:
                cursor.close()
                
                
    def getBuyerName(self,id):
        cursor = None
        try:
            if self.connection != None:
                cursor = self.connection.cursor()
                query = "select buyerName from buyer where buyerid = %s"
                cursor.execute(query,(id))
                
                return cursor.fetchone()[0]    
        except Exception as e:
            print("Exception in getBuyerIDs", str(e))
        finally:
            if cursor != None:
                cursor.close()
                
                
    def getSellerName(self,id):
        cursor = None
        try:
            if self.connection != None:
                cursor = self.connection.cursor()
                query = "select sellerName from seller where sellerid = %s"
                cursor.execute(query,(id))
                return cursor.fetchone()[0]    
        except Exception as e:
            print("Exception in getBuyerIDs", str(e))
        finally:
            if cursor != None:
                cursor.close()
                
                
    def getBuyerName(self,id):
        cursor = None
        try:
            if self.connection != None:
                cursor = self.connection.cursor()
                query = "select buyerName from seller where buyerid = %s"
                cursor.execute(query,(id))
                return cursor.fetchone()[0]    
        except Exception as e:
            print("Exception in getBuyerIDs", str(e))
        finally:
            if cursor != None:
                cursor.close()
                
                
    def getMessages(self,roomID):
        cursor = None
        try:
            if self.connection != None:
                cursor = self.connection.cursor()
                query = "select message,messageby,datetime from messages where roomID = %s"
                cursor.execute(query,(roomID))
                return cursor.fetchall()    
        except Exception as e:
            print("Exception in getMessages()", str(e))
        finally:
            if cursor != None:
                cursor.close()
    
    # new function for dynamic content on sller home
    def getSellerProductsCount(self,id):
        cursor = None
        try:
            if self.connection != None:
                cursor = self.connection.cursor()
                query = "select count(*) from products where sellerid = %s";
                cursor.execute(query,(id))
                return cursor.fetchone()[0]    
        except Exception as e:
            print("Exception in getSellerProductsCount", str(e))
        finally:
            if cursor != None:
                cursor.close()
                  # new function for dynamic content on seller home
    def getSellerPendingApprovedProductsCount(self,id,status):
        cursor = None
        try:
            if self.connection != None:
                cursor = self.connection.cursor()
                query = "select count(*) from products where sellerid = %s and pAppStatus=%s";
                cursor.execute(query,(id,status))
                return cursor.fetchone()[0]    
        except Exception as e:
            print("Exception in getBuyerIDs", str(e))
        finally:
            if cursor != None:
                cursor.close()
    
    
    # search for seller end
    
    
    def getAppProbyName(self,sellerID,name,status):
        cursor = None
        try:
            if self.connection != None:
                cursor = self.connection.cursor()
                query = "select * from products where pAppStatus=%s and proDel=0 and sellerId=%s and products.pName = %s;" 
                cursor.execute(query,(status,sellerID,name))
                return cursor.fetchall()
        except Exception as e:
            print("Exception in getsellerdetail", str(e))
        finally:
            if cursor != None:
                cursor.close()
                
                
    def getMySellers(self,sellerID):
        cursor = None
        try:
            if self.connection != None:
                cursor = self.connection.cursor()
                query = "select roomID from messages"
                cursor.execute(query) 
                sellers = []
                for roomID in cursor.fetchall():
                    if roomID[0].split(',')[0]==str(sellerID):
                        sellers.append(roomID[0].split(',')[1])
                return sellers
        except Exception as e:
            print("Exception in getMySellers", str(e))
        finally:
            if cursor != None:
                cursor.close()
    
    
    def getBuyerInfo(self,email):
        cursor = None
        try:
            if self.connection != None:
                cursor = self.connection.cursor()
                query = "select * from buyers where buyeremail=email"
                cursor.execute(query) 
                return cursor.fetchone()
        except Exception as e:
            print("Exception in getMySellers", str(e))
        finally:
            if cursor != None:
                cursor.close()
                
    