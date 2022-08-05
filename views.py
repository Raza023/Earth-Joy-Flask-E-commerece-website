class Admin:
    def __init__(self, email,pswrd):
        self.email = email
        self.pswrd = pswrd

class User:
    def __init__(self, email,pswrd):
        self.email = email
        self.pswrd = pswrd
        
class Buyers:
    def __init__(self, email,pswrd,name,gender,dob,pic):
        self.email = email
        self.pswrd = pswrd
        self.name = name
        self.gender = gender
        self.dob = dob
        self.pic = pic        
        
        
        
class Seller:
    def __init__(self,email,password):
        self.email , self.password =email,password

class Product:
    def __init__(self,name,pType,pDescript,price,stock,mainTag,pImage,sellerId):
        self.name = name
        self.pType = pType
        self.pDescript=pDescript
        self.price = price
        self.stock = stock
        self.mainTag = mainTag
        self.pImage = pImage
        self.sellerId=sellerId
        