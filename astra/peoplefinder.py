from basePackages import *
def peoplefinder_name_search(rows):
    return_data = {'status': 'noAddressMatch'}
    data = rows[6] + '-' + rows[5].replace(' ','%20') + '-' + rows[2] + '-' + rows[1]
    url = 'http://www.peoplefinder.com/people-search/' + data
    soup = BeautifulSoup(urlopen(url),"lxml")
    results = soup.findAll('div','ticklerResultsData')
    if not results:
        return
    non_match_address = []
    for result in results:
        name = result.find('span','ticklerResultsName').find('a').text.strip()
        addr = result.find('div','datumAddr')
        phone = addr.find('span','phoneNumber')
        if phone is None: return
        addr1 = []
        for full_addr in addr.childGenerator():
            addr1.append(full_addr)
        streetAddress = str(addr1[0]).strip()
        locality = str(addr1[2]).strip()
        phone = phone.text.strip()
        if sm(a=streetAddress.lower(),b=rows[3].lower()).ratio() > cutoffAddressMatch:
            return_data['status'] = 'addressMatch'
            return_data['data'] = [rows[0],name,streetAddress, locality, phone]
            return return_data
        non_match_address.append([rows[0],name,streetAddress, locality, phone])
    return_data['data'] = non_match_address
    return return_data
