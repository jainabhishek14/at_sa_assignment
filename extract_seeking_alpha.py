import os
companyName = input("Enter Company Name:")
productName = input("Enter Product Name:")

print("starting...")
os.system("scrapy crawl sa -a companyName="+companyName)
os.system("python3 relevance_checker.py -p "+ productName +" -i " + companyName + ".txt")
