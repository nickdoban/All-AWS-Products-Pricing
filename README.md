# All-AWS-Products-Pricing
Automatically download AWS products' prices and save them in pandas dataframes in a dictionary

This is more or less WIP mini-project. By default it will download ALL AWS products' prices but you can filter only for your products of interest by replacing 'list_offers' in main.py with your list of AWS products. It saves all new 'index.json' files on your machine so that next time it runs, the downloaded file is compared with the saved one: if they are different an email is sent to 'emailTo' and the new (downloaded) file is saved; otherwise, the file is not saved and the email is not sent.

How to:
1. update the config filewith your info
2. update the 'emailTo' in main.py (can be just one email address)



Future work might include:
1. running the code on a server to show the processed dataframes on a nice dashboard: charts and/or tables (like https://www.ec2instances.info/)
2. limiting to a certain list of AWS products
3. maybe more specific error emails
4. Step 4 in 'main.py'
