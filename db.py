import mysql.connector
mydb = mysql.connector.connect(host="localhost",user="root",passwd="password", database="testing")
mycursor = mydb.cursor()

def add_userdata(username,password,email_address,age,phone_no):
	try:
		mycursor.execute("INSERT INTO User(Name,EmailID,Age,Password,PhoneNo) VALUES(%s,%s,%s,%s,%s)", (username, email_address,age,password,phone_no))
		mydb.commit()
	except mysql.connector.Error as err:
		return err.msg
	q = f"Select UserID from User where User.Name = '{username}';"
	mycursor.execute(q)
	res = mycursor.fetchall()
	q = f"INSERT INTO Buyer(UserID) VALUES('{(int)(res[0][0])}');"
	mycursor.execute(q)
	mydb.commit()
	return ""

def login_user(username,password):
    q = f"SELECT * from User WHERE Name = '{username}' and Password = '{password}';"
    mycursor.execute(q)
    data = mycursor.fetchall()
    return data

def viewalldata():
    mycursor.execute("Select Ads_Title,Ads_Desciption,Price,Status,Date from Ads;")
    data = mycursor.fetchall()
    return data

def viewavaildata():
    mycursor.execute("select Ads_Title, Date, Price, CategoryName from Ads, Category where Ads.CategoryID = Category.CategoryID and Status = 1 order by Date DESC;")
    data = mycursor.fetchall()
    return data

def viewwatchlist(username):
    q = f"select Ads_Title,Ads_Desciption,Ads.Status,Price from Ads, WatchList where Ads.Ads_ID = WatchList.Ads_ID and WatchList.BuyerID = (select BuyerID from Buyer, User where Buyer.UserID = User.UserID and User.Name = '{username}');"
    mycursor.execute(q)
    data = mycursor.fetchall()
    return data

def post_newad(title,description,price,category,status,date,url,username):
    q = f"INSERT INTO Ads(Date,Status,Ads_Title,Ads_Desciption,Price,Pictures,CategoryID) VALUES('{date}','{status}','{title}','{description}','{price}','{url}','{category}');"
    try:
        mycursor.execute(q)
        mydb.commit()
    except mysql.connector.Error as err:
        q = f"DELETE FROM Ads WHERE Ads_Title = '{title}';"
        mycursor.execute(q)
        return err.msg
    q1 = f"Select Ads_ID from Ads where Ads.Ads_Title = '{title}';"
    mycursor.execute(q1)
    res1 = mycursor.fetchall()
    q = f"Select Exists(select SellerID from Seller, User where Seller.UserID = User.UserID and User.Name = '{username}');"
    mycursor.execute(q)
    res = mycursor.fetchall()
    print((int)(res[0][0]))
    if (1 == (int)(res[0][0])):
        q = f"select SellerID from Seller, User where Seller.UserID = User.UserID and User.Name = '{username}';"
        mycursor.execute(q)
        res = mycursor.fetchall()
        q = f"INSERT INTO Posts(Ads_ID, SellerID) VALUES ('{(int)(res1[0][0])}','{(int)(res[0][0])}');"
        try:
            mycursor.execute(q)
            mydb.commit()
            return ""
        except mysql.connector.Error as err:
            q = f"DELETE FROM Ads WHERE Ads_Title = '{title}';"
            mycursor.execute(q)
            return err.msg
    else:
        q = f"select UserID from User where User.Name = '{username}';"
        mycursor.execute(q)
        res = mycursor.fetchall()
        q = f"INSERT INTO Seller(UserID,Street,City,region,postalZip) VALUES('{(int)(res[0][0])}','Random','Random','Random',100000);"
        mycursor.execute(q)
        mydb.commit()
        q = f"select SellerID from Seller, User where Seller.UserID = User.UserID and User.Name = '{username}';"
        mycursor.execute(q)
        res = mycursor.fetchall()
        q = f"INSERT INTO Posts(Ads_ID, SellerID) VALUES ('{(int)(res1[0][0])}','{(int)(res[0][0])}');"
        try:
            mycursor.execute(q)
            mydb.commit()
            return ""
        except mysql.connector.Error as err:
            q = f"DELETE FROM Ads WHERE Ads_Title = '{title}';"
            mycursor.execute(q)
            return err.msg
        

def sellads(username):
    q = f"select Ads_Title,Ads_Desciption,Status,Price from Ads,Posts where Ads.Ads_ID = Posts.Ads_ID and Posts.SellerID in (select SellerID from Seller, User where Seller.UserID = User.UserID and User.Name = '{username}');"
    mycursor.execute(q)
    data = mycursor.fetchall()
    return data
    
def get_task(title):
    q = f"select * from Ads where Ads_Title = '{title}'"
    mycursor.execute(q)
    data = mycursor.fetchall()
    return data

def update_ad(old_adtitle,new_adtitle,new_addesciption,new_price,new_status,new_category,new_pic):
    if new_status == "Available":
        new_status = 1
    else:
        new_status = 0
    mycursor.execute("UPDATE Ads SET Ads_Title =%s WHERE Ads_Title =%s ",(new_adtitle,old_adtitle))
    mydb.commit()
    mycursor.execute("UPDATE Ads SET Ads_Desciption =%s WHERE Ads_Title =%s ",(new_addesciption,new_adtitle))
    mydb.commit()
    mycursor.execute("UPDATE Ads SET Status =%s WHERE Ads_Title =%s ",(new_status,new_adtitle))
    mydb.commit()
    mycursor.execute("UPDATE Ads SET Pictures =%s WHERE Ads_Title =%s ",(new_pic,new_adtitle))
    mydb.commit()
    mycursor.execute("UPDATE Ads SET CategoryID =%s WHERE Ads_Title =%s ",(new_category,new_adtitle))
    mydb.commit()
    try:
        mycursor.execute("UPDATE Ads SET Price =%s WHERE Ads_Title =%s ",(new_price,new_adtitle))
        mydb.commit()
    except mysql.connector.Error as err:
        return err.msg
    data = mycursor.fetchall()
    return data

def delete_ad(adtitle):
    q = f"SET FOREIGN_KEY_CHECKS=0;"
    mycursor.execute(q)
    mydb.commit()
    q = f"DELETE FROM Posts WHERE Ads_ID = (select Ads_ID from Ads where Ads_Title = '{adtitle}');"
    mycursor.execute(q)
    mydb.commit()
    q = f"DELETE FROM Ads WHERE Ads_Title = '{adtitle}';"
    mycursor.execute(q)
    mydb.commit()
    q = f"SET FOREIGN_KEY_CHECKS=1;"
    mycursor.execute(q)
    mydb.commit()

def search_ad(keywords):
    q = f"Select Ads_Title, Price from Ads where Ads_Title like '%{keywords}%' and Status = 1;"
    mycursor.execute(q)
    data = mycursor.fetchall()
    return data

def add_to_watchlist(text, user):
    q = f"Select Ads_ID from Ads where Ads_Title = '{text}';"
    mycursor.execute(q)
    res1 = mycursor.fetchall()
    q = f"select Buyer.BuyerID from Buyer inner join User where Buyer.UserID = User.UserID and User.Name = '{user}';"
    mycursor.execute(q)
    res2 = mycursor.fetchall()
    q = f"INSERT into WatchList(BuyerID, Ads_ID) VALUES ('{(int)(res2[0][0])}','{(int)(res1[0][0])}');"
    try:
        mycursor.execute(q)
        mydb.commit()
        return ""
    except mysql.connector.Error as err:
        return err.msg

def viewbestsellers():
    q = f"select Name, AVG(Rating), RANK() OVER (order by AVG(Rating) DESC) AS SellerRank from Review, sellerinfo where Review.SellerID = sellerinfo.SellerID Group By Name;"
    mycursor.execute(q)
    data = mycursor.fetchall()
    return data

def avgsalecat():
    q = f'''with CatPrice(CategorID, Price) as (select CategoryID, avg(Price) from Ads group by CategoryID)
            select CategoryName, Price																
            from CatPrice
            inner join Category ON CatPrice.CategorID = Category.CategoryID;'''
    mycursor.execute(q)
    data = mycursor.fetchall()
    return data

def countadscat():
    q = f'''select CategoryName, count(*) as Number
            from Category, Ads
            where Category.CategoryID = Ads.CategoryID				
            group by CategoryName;'''
    mycursor.execute(q)
    data = mycursor.fetchall()
    return data

def viewbestsellerscat():
    q = f'''select Name, Avg(Rating), CategoryName, RANK() OVER (partition by CategoryName order by Avg(Rating) DESC) AS SellerRank 
            from allinfo, sellerinfo 
            where allinfo.SellerID = sellerinfo.SellerID 
            Group By Name;'''
    mycursor.execute(q)
    data = mycursor.fetchall()
    return data

def mostwatchlad():
    q = f'''select Ads_Title, count(BuyerID) as NumberofBuyers							
            from Ads, WatchList
            where Ads.Ads_ID = WatchList.Ads_ID
            group by Ads_Title
            order by NumberofBuyers DESC;'''
    mycursor.execute(q)
    data = mycursor.fetchall()
    return data

def regiontotsales():
    q = f'''SELECT SellerID, PaymentType, Region, Price, sum(Price) OVER(PARTITION BY Region) as grand_total 
            from payperview;'''
    mycursor.execute(q)
    data = mycursor.fetchall()
    return data

def regionavgsales():
    q = f'''SELECT SellerID, PaymentType, Region, Price, avg(Price) OVER(PARTITION BY Region) as grand_total 
            from payperview;'''
    mycursor.execute(q)
    data = mycursor.fetchall()
    return data

def viewbsuser():
    q = f"select * from bothbuyerseller"
    mycursor.execute(q)
    data = mycursor.fetchall()
    return data

def viewuserinfo():
    q = f"select * from userinfo"
    mycursor.execute(q)
    data = mycursor.fetchall()
    return data

def avgratcat():
	q = f'''select CategoryName as Category, avg(Rating) as Average_Rating
			from Review natural join Ads natural join Category
			where Status = 0		
			group by CategoryID, CategoryName
			order by CategoryID ASC;'''
	mycursor.execute(q)
	data = mycursor.fetchall()
	return data