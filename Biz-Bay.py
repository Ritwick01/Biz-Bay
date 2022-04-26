import streamlit as st
import pandas as pd
from db import *


def main():
	"""Biz - Bay"""

	st.title("Biz-Bay")

	menu = ["Home","Login","SignUp","Back-End","Third-Party Vendors"]
	choice = st.sidebar.selectbox("Menu",menu)

	if choice == "Home":
		st.subheader("Home")
		result = viewalldata()
		db = pd.DataFrame(result, columns=["Title", "Description", "Price", "Status", "Date"])
		db.loc[db["Status"] == 0, "Status"] = "Sold"
		db.loc[db["Status"] == 1, "Status"] = "Available"
		st.dataframe(db)

	elif choice == "Login":

		username = st.sidebar.text_input("User Name")
		password = st.sidebar.text_input("Password",type='password')
		if st.sidebar.checkbox("Login"):			

			result = login_user(username,password)
			if result:
				st.success("Logged In as {}".format(username))
				menu2 = ["Buyer", "Seller"]
				task = st.selectbox("Task",menu2)

				if task == "Buyer":
					menu3 = ["View Ad List", "View Watchlist", "Search"]
					buyer_task = st.selectbox("Actions",menu3)

					if buyer_task == "View Ad List":
						result = viewavaildata()
						db = pd.DataFrame(result, columns=["Title", "Date", "Price", "Category"])
						st.dataframe(db)

					elif buyer_task == "View Watchlist":
						result = viewwatchlist(username)
						db = pd.DataFrame(result, columns=["Title", "Description", "Status", "Price"])
						db.loc[db["Status"] == 0, "Status"] = "Sold"
						db.loc[db["Status"] == 1, "Status"] = "Available"
						st.dataframe(db)
					
					elif buyer_task == "Search":
						search = st.text_input("Search for products")
						result = search_ad(search)
						db = pd.DataFrame(result, columns=["Title", "Price"])
						st.dataframe(db)

						bookmark = st.text_input("Add to WatchList")
						if st.button("Add to Watchlist"):
							res = add_to_watchlist(bookmark, username)
							if (len(res) == 0):
								st.success("Successfully added to your WatchList")
							else:
								st.warning(res)

				elif task == "Seller":
					menu3 = ["Your Ads", "Post New Ad", "Update your Ads", "Delete Ad"]
					seller_task = st.selectbox("Actions",menu3)
					menu4 = ["Cars", "Electronics", "Songs", "Clothes", "Books", "Plants", "Movies", "Services"]
					cat_dict = {"Cars" : 1, "Electronics" : 2, "Songs" : 3, "Clothes" : 4, "Books" : 5, "Plants" : 6, "Movies" : 7, "Services" : 8}

					if seller_task == "Post New Ad":
						new_adtitle = st.text_input("Title")
						new_addesciption = st.text_input("Description")
						new_price = st.text_input("Price")
						new_status = 1
						new_category = st.selectbox("Category",menu4)
						new_date = st.date_input("Date of Creation")
						new_pic = st.text_input("Picture URL")

						if st.button("Post"):
							res = post_newad(new_adtitle,new_addesciption,new_price,cat_dict[new_category],new_status,new_date,new_pic,username)
							if (len(res) == 0):
								st.success("Successfully posted your Ad")
							else:
								st.warning(res)

					elif seller_task == "Your Ads":
						result = sellads(username)
						db = pd.DataFrame(result, columns=["Title", "Description", "Status", "Price"])
						db.loc[db["Status"] == 0, "Status"] = "Sold"
						db.loc[db["Status"] == 1, "Status"] = "Available"
						st.dataframe(db)
						
					elif seller_task == "Update your Ads":
						result = sellads(username)
						lst = [i[0] for i in result]
						edit_task = st.selectbox("Select Ad to Update", lst)
						task_assigned = get_task(edit_task)

						if (len(task_assigned) != 0):
							old_adtitle = task_assigned[0][3]
							new_adtitle = st.text_input("Title")
							new_addesciption = st.text_input("Description")
							new_price = st.text_input("Price")
							new_status = st.selectbox("Status", ["Available", "Sold"])
							new_category = st.selectbox("Category",menu4)
							new_pic = st.text_input("Picture URL")
							if st.button("Update your Ad"):
								msg = update_ad(old_adtitle,new_adtitle,new_addesciption,new_price,new_status,cat_dict[new_category],new_pic)
								if (len(msg) == 0):
									st.success("Successfully updated your Ad")
								else:
									st.warning(msg)
							
					elif seller_task == "Delete Ad":
						result = sellads(username)
						lst = [i[0] for i in result]
						delete_task = st.selectbox("Select Ad to Delete", lst)
						task_assigned = get_task(delete_task)
						if (len(task_assigned) != 0):
							old_adtitle = task_assigned[0][3]
							if st.button("Confirm to Delete"):
								delete_ad(old_adtitle)
								st.success("Successfully Deleted the Ad")
				
			else:
				st.warning("Incorrect Username/Password")


	elif choice == "SignUp":
		st.subheader("Create New Account")
		new_user = st.text_input("Username")
		new_password = st.text_input("Password",type='password')
		new_email = st.text_input("Email")
		new_age = st.text_input("Age")
		new_phoneno = st.text_input("Phone Number")


		if st.button("Signup"):
			res = add_userdata(new_user,new_password,new_email,new_age,new_phoneno)
			if (len(res) == 0):
				st.success("You have successfully created a valid Account")
				st.info("Go to Login Menu to login")
			else:
				st.warning(res)

	elif choice == "Back-End":
		menu = ["View Best Sellers", "Average Sale across Categories", "Ads Posted Category-Wise", "View Best Sellers Category-Wise", "Most Watchlisted Ad", "Region-Wise Total Sales", "Region-Wise Average Sales", "Users who are both buyers and sellers"]
		task = st.selectbox("Task",menu)
		if (task == "View Best Sellers"):
			result = viewbestsellers()
			db = pd.DataFrame(result, columns=["Seller Name", "Rating", "Rank"])
			db["Rating"] = db["Rating"].astype(float)
			st.dataframe(db)

		elif (task == "Average Sale across Categories"):
			result = avgsalecat()
			db = pd.DataFrame(result, columns=["Category", "Price"])
			db["Price"] = db["Price"].astype(float)
			st.dataframe(db)

		elif (task == "Ads Posted Category-Wise"):
			result = countadscat()
			db = pd.DataFrame(result, columns=["Category", "Number of Ads Posted"])
			st.dataframe(db)

		elif (task == "View Best Sellers Category-Wise"):
			result = viewbestsellerscat()
			db = pd.DataFrame(result, columns=["Seller Name", "Rating", "Category", "Rank"])
			db["Rating"] = db["Rating"].astype(float)
			st.dataframe(db)

		elif (task == "Most Watchlisted Ad"):
			result = mostwatchlad()
			db = pd.DataFrame(result, columns=["Ads", "Number of Buyer"])
			st.dataframe(db)

		elif (task == "Region-Wise Total Sales"):
			result = regiontotsales()
			db = pd.DataFrame(result, columns=["SellerID", "PaymentType", "Region", "Price", "Region-wise Total Sales"])
			st.dataframe(db)

		elif (task == "Region-Wise Average Sales"):
			result = regionavgsales()
			db = pd.DataFrame(result, columns=["SellerID", "PaymentType", "Region", "Price", "Region-wise Average Sales"])
			db["Region-wise Average Sales"] = db["Region-wise Average Sales"].astype(float)
			st.dataframe(db)

		elif (task == "Users who are both buyers and sellers"):
			result = viewbsuser()
			db = pd.DataFrame(result, columns=["Name", "User-ID", "Buyer-ID", "Seller-ID"])
			st.dataframe(db)
		
	elif choice == "Third-Party Vendors":
		menu = ["View User Data", "Average Rating across Categories"]
		task = st.selectbox("Task", menu)
		if (task == "View User Data"):
			result = viewuserinfo()
			db = pd.DataFrame(result, columns=["Name", "Email-ID", "Age"])
			st.dataframe(db)

		elif (task == "Average Rating across Categories"):
			result = avgratcat()
			db = pd.DataFrame(result, columns=["Category", "Average Rating"])
			db["Average Rating"] = db["Average Rating"].astype(float)
			st.dataframe(db)

if __name__ == '__main__':
	main()

