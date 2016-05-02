from basePackages import *

def superpage_addr_search(rows):
    return_data = {}
    output_match_data = []
    output_noMatch_data = []
    base_url = 'http://wp.superpages.com/results.php?ReportType=34&'
    addr2 = ''
    if len(rows[4])>1: addr2 = ',' + rows[4]
    full_address = (rows[3] + addr2).strip().replace(' ','+')
    url_data = {
        'qa': full_address,
        'qc': rows[5].replace(' ','+'),
        'qst': full_address,
        'qi': 0,
        'qk': 100,
        'qs': rows[6]
    }
    url = base_url + urlencode(url_data).replace('%2B','+')
    data = BeautifulSoup(urlopen(url),"lxml")
    results = data.find('table','wp_singleresulttable')
    if results is not None:
        name = results.find('h1','name').text.strip()
        name1=name.split()[-1]
        streetAddress = results.find('span',{'itemprop':'streetAddress'}).text
        addressLocality = results.find('span',{'itemprop':'addressLocality'}).text
        addressRegion = results.find('span',{'itemprop':'addressRegion'}).text
        postalCode = results.find('span',{'itemprop':'postalCode'}).text
        phone = results.find('div','phone').text.strip()
        if ((rows[1].lower()) == (name1.lower())):
                output_match_data.append([rows[0], name, streetAddress, mergeLocality(addressLocality, addressRegion, postalCode), phone])
        else:
            output_noMatch_data.append([rows[0], name, streetAddress, mergeLocality(addressLocality, addressRegion, postalCode), phone])
    else:
        results = data.find('table','wp_multiresultstable')
        if results is not None:
            records = results.findAll('td',{'itemtype': 'http://schema.org/Person'})
            for record1 in records:
                name = record1.find('a','listing-header').text
                name1= name.split()[-1]
                streetAddress = record1.find('span',{'itemprop':'streetAddress'}).text
                addressLocality = record1.find('span',{'itemprop':'addressLocality'}).text
                addressRegion = record1.find('span',{'itemprop':'addressRegion'}).text
                postalCode = record1.find('span',{'itemprop':'postalCode'}).text
                phone = record1.find('span','listing-phone').text
                if ((rows[1].lower()) == (name1.lower())):
                    output_match_data.append([rows[0], name, streetAddress, mergeLocality(addressLocality, addressRegion, postalCode), phone])
                else:
                    output_noMatch_data.append  ([rows[0], name, streetAddress, mergeLocality(addressLocality, addressRegion, postalCode), phone])
    return_data['last_name_match'] = output_match_data
    return_data['no_last_name_match'] = output_noMatch_data
    return return_data
