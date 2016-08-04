from basePackages import *

def superpage_name_search(rows):
    return_data = {'type': 'singleRecord', 'status': 'noAddressMatch'}
    base_url = 'http://wp.superpages.com/people/'
    url = base_url + (rows[2]+' '+rows[1]).strip().replace(' ','-')+'/'+rows[5].strip().replace(' ','-')+'-'+rows[6].strip() + '&qk=100'
    response = urlopen(url)
    if url != response.url:
        #print url , 'got redirected to' , response.url
        return
    soup = BeautifulSoup(response.read(),"lxml")
    if soup.find('div','NoResultBar'): return
    multiRecords = soup.find('table','wp_multiresultstable')
    if multiRecords:
        non_match_address = []
        for record in multiRecords.findAll('td','wp_multiresultsrow'):
            gender_m = record.find('img','gender-icon')
            if gender_m:
                gender =  re.findall('\w*.png',gender_m['src'])[0][:1].upper()
                name = record.find('a','listing-header').text
                address = record.find('div','listing-address')
                streetAddress = address.find('span',{'itemprop':'streetAddress'}).text
                addressLocality = address.find('span',{'itemprop':'addressLocality'}).text
                addressRegion = address.find('span',{'itemprop':'addressRegion'}).text
                postalCode = (address.find('span',{'itemprop':'postalCode'}).text)
                phone = record.find('span','listing-phone').text.strip()
                if sm(a=streetAddress.lower(),b=rows[3].lower()).ratio() > cutoffAddressMatch:
                    return_data['status'] = 'addressMatch'
                    return_data['data'] = [rows[0], name, streetAddress, mergeLocality(addressLocality, addressRegion, postalCode), phone, gender]
                    return return_data
                else:
                    non_match_address.append([rows[0], name, streetAddress, mergeLocality(addressLocality, addressRegion, postalCode), phone, gender])
        return_data['type'] = 'multiRecords'
        return_data['data'] = non_match_address
        return return_data
    else:
        gender_icon = soup.find('div','gender-icon')
        if len(gender_icon.findChildren())>0: gender = re.findall('\w*.png',gender_icon.findChildren()[0]['src'])[0][:1].upper()
        else: gender = None
        profile = soup.find('div','profile')
        name = profile.find('h1','name').text.strip()
        address = profile.find('div','address')
        streetAddress = address.find('span',{'itemprop':'streetAddress'}).text
        addressLocality = address.find('span',{'itemprop':'addressLocality'}).text
        addressRegion = address.find('span',{'itemprop':'addressRegion'}).text
        postalCode = address.find('span',{'itemprop':'postalCode'}).text
        phone = profile.find('div','phone').text.strip()
        return_data['data'] = [rows[0], name, streetAddress, mergeLocality(addressLocality, addressRegion, postalCode), phone, gender]
        if sm(a=streetAddress.lower(),b=rows[3].lower()).ratio() > cutoffAddressMatch:
            return_data['status'] = 'addressMatch'
        return return_data
