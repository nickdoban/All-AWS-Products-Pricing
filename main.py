# Steps:
# 1. Inputs
# 2. Download and compare the contents of onlineOffer and onlocalOffer index.json files
# 3. Download each ("currentVersionUrl") offer file and convert to DFs. Save all DFs into a dict
# 4. compare the json offer files between publicationDates

import json, glob, os, pandas as pd, time
from ClassesFuns import checkGet_and_loads, send_email
# read config file
try: dict_config = json.loads( open( 'config_inputs.json' ).read() )
except Exception as e:
    print( '\nERROR: {}'.format(str(e) ))
    exit()
# Step 1.
emailFrom = dict_config['emailFrom']
password = dict_config['password']
emailSubject = dict_config['emailSubject']
emailTo = ['email-1', 'email-2']
url_offer = dict_config['url_offer']
file_offer = 'offer'
# where to save: path & file_name
path_savedOffers = dict_config['path_savedOffers']
file_name = '-offer.json'
# Step 2.
# get the most recent saved offer file as a string: path, file name and extension
list_of_files = glob.glob(path_savedOffers + '*.[Jj][Ss][Oo][Nn]')
latest_file = max(list_of_files, key = os.path.getctime)
# read the saved offer json files
onlocalOffer = json.loads( open( latest_file ).read() )

# download index.json: call the class: 1. 200 check offer_init; 2. store offer json file
call_class_offer = checkGet_and_loads()
call_class_offer.get(url_offer, file_offer)
onlineOffer = call_class_offer.loads()

# Check if keys of onlocal and online json files are the same; send email if not
if list( onlocalOffer.keys() ) != list( onlineOffer.keys() ):
    emailBody = ''' Sending email. Keys of downloaded json file and the one saved on local machine are not equivalent. '''
    send_email(fromaddr = emailFrom, pwd = password, toaddr = emailTo, Subject = emailSubject, body = emailBody)
else: pass
    # print('Not sending email. Keys of downloaded json file and the one saved on local machine are equivalent.')

# if the already saved file is equivalent with the downloaded one then do nothing;
# otherwise, save the downloaded file in the same directory and use it (to compare with the downloaded json) next time when this script will run
if onlocalOffer == onlineOffer:
    print('offer files are equivalent. Not saving the json file')
    pass # do nothing
else:
    # send email to gmail because offer files (online and onlocal) are different
    print('Sending emails. offer files not equivalent. Saving the new version of the file.')
    # save the offer dictionary in a json file with timestamp in filename
    with open(path_savedOffers + time.strftime('%d%b%Y-%HH%MM%SS') + file_name, 'w') as f:
        # what data to save to json
        json.dump(onlineOffer, f, indent = 4)
# check if keys in index.json are the same between onlocalOffer and onlineOffer files; send email if not
# check formatVersion, disclaimer, publicationDate
def check_and_email(j1, j2, param):
    if j1[param] != j2[param]:
        print( 'Sending email. {} in both files is not equivalent.'.format(param) )
        emailBody = ' The downloaded json file is different from the one saved on local machine. The difference is in %s. Previous %s is %s and the new one is %s '.format( param, param, j1[param], j2[param] )
        send_email(fromaddr = emailFrom, pwd = password, toaddr = emailTo, Subject = emailSubject, body = emailBody)
    else: pass
        # print( 'Not sending email. {} in both files is equivalent.'.format(param) )
# call the Fun
for param in list( filter( lambda i: i != 'offers', onlocalOffer.keys() ) ):
    check_and_email(j1 = onlocalOffer, j2 = onlineOffer, param = param)
    print('\n')
# Check number of offers and list of offers
if list( onlocalOffer['offers'].keys() ) != list( onlineOffer['offers'].keys() ):
    print(' Sending email. List of offers in both files is not the same. ')
    emailBody = ' 1. Number of offers in the saved file is {} and in the downlaoded file is {}. '.format( len(list(onlocalOffer['offers'].keys())), len(list(onlineOffer['offers'].keys())) )
    more_emailBody1 = ' \n\n 2. List of offers in the saved json offer file is {} \n\n and in the downloaded file is {}. '.format( list(onlocalOffer['offers'].keys()), list(onlineOffer['offers'].keys()) )
    more_emailBody2 = ' \n\n 3. Offers in the saved file and not in the downloaded file: {} '.format( list( set(list(onlocalOffer['offers'].keys())) - set(list(onlineOffer['offers'].keys())) ) )
    more_emailBody3 = ' \n Offers in the downloaded file and not in the saved file: {} '.format( list( set(list(onlineOffer['offers'].keys())) - set(list(onlocalOffer['offers'].keys())) ) )
    send_email(fromaddr = emailFrom, pwd = password, toaddr = emailTo, Subject = emailSubject, body = emailBody + more_emailBody1 + more_emailBody2 + more_emailBody3)
else: pass
    # print('Not sending email. List of offers in both files is the same.')
# offer file to use; optional since we can use only the latest online json file
useOffer = onlocalOffer if onlocalOffer == onlineOffer else onlineOffer

# Step 3.
# get the list of offer names
offersList = list( useOffer['offers'].keys() )
# Prepare the df_merged; 
df_merged = pd.DataFrame()
dict_DFs = {}
file_region_index = 'json file with region_index'
len_offers = len(offersList)
for offer in offersList: # print( offer )
    df_products, df_terms_priceDims = pd.DataFrame(), pd.DataFrame()
    print('\n{}: GETTING "{}"; #{} out of {}'.format(time.strftime('%d%b%Y %H:%M:%S:'), offer, offersList.index(offer) + 1, len_offers))
    try: url_region_index = 'https://pricing.us-east-1.amazonaws.com' + useOffer['offers'][offer]['currentRegionIndexUrl']
    except Exception as e: print( 'ERROR: {}'.format(str(e)) )
    # call the class for region_index: 1. 200 check; 2. get region_index json file
    call_class_offer.get(url_region_index, file_region_index)
    json_region_index = call_class_offer.loads()
    # get list of regions
    for kk1, vv1 in json_region_index['regions'].items(): # print('{}: {}'.format(kk1, vv1))
        region = kk1
        url_region = vv1['currentVersionUrl']
        # df_products and df_terms    
        print('{}: GETTING {}'.format(time.strftime('%d%b%Y %H:%M:%S:'), url_region))
        call_class_offer.get('https://pricing.us-east-1.amazonaws.com{}'.format(url_region), url_region)
        json_index = call_class_offer.loads()
        # df_products
        list_products = list( json_index['products'].keys() )
        for prod in list_products: # print(prod)
            sku = json_index['products'][prod]['sku']
            # if dict key 'productFamily' doesn't exist return ''
            productFamily = json_index['products'][prod].get('productFamily', '')
            df_prod = pd.io.json.json_normalize( json_index['products'][prod]['attributes'] )
            df_prod['sku'] = sku
            df_prod['productFamily'] = productFamily
            df_prod['region'] = region
            # append to df; for some reason there are duplicates
            df_products = df_products.append(df_prod, ignore_index=True)
            df_products.drop_duplicates(inplace = True)
        # df_terms
        for kk2, vv2 in json_index['terms']['OnDemand'].items(): # print( '{}: {}'.format(kk2, vv2) )
            sku = kk2
            # list of SKUs and offerTermCodes
            sku_oTC = list(vv2.keys())[0]
            effectiveDate = vv2[ sku_oTC ]['effectiveDate']
            # if dict key 'Restriction' doesn't exist return ''
            termAttributes = vv2[sku_oTC]['termAttributes'].get('Restriction', '')
            # get the 'priceDimensions' into df
            for kk3, vv3 in vv2[sku_oTC]['priceDimensions'].items(): # print('{}: {}'.format(kk3, vv3))
                df_terms_priceDim = pd.io.json.json_normalize( vv3 )
                # convert lists to elemets here rather than later to avoid 'MemoryError'
                df_terms_priceDim['appliesTo'] = df_terms_priceDim['appliesTo'].apply(lambda x: ', '.join(x))
                df_terms_priceDim['sku'] = sku
                df_terms_priceDim['sku_oTC'] = sku_oTC
                df_terms_priceDim['effectiveDate'] = effectiveDate
                df_terms_priceDim['termAttributes'] = termAttributes
                # append to df; for some reason there are duplicates
                df_terms_priceDims = df_terms_priceDims.append(df_terms_priceDim, ignore_index=True)
                df_terms_priceDims.drop_duplicates(inplace = True)
    # merge df_products with df_terms_priceDims and append to the dict_DFs
    df_merged = pd.merge(df_products, df_terms_priceDims, on = ['sku'] )
    dict_DFs[offer] = df_merged

# Step 4.


print('{}: Done\n'.format(time.strftime('%d%b%Y %H:%M:%S:')))
# maybe email when script is finished