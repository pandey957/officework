from superpage import superpage_name_search
from peoplefinder import peoplefinder_name_search
from basePackages import *
from addr_superpage import superpage_addr_search

if __name__ == '__main__':
    wrtr_addr_match, wrtr_no_addr_match, wrtr_ln_match_addr, wrtr_no_ln_match_addr = getwriterObj()
    writerHeader(wrtr_addr_match)
    writerHeader(wrtr_no_addr_match)
    writerHeader(wrtr_ln_match_addr)
    writerHeader(wrtr_no_ln_match_addr)
    in_file = 'astra_data.csv'
    urls = open(in_file,'rU')
    urls.readline()
    csv_input = csv.reader(urls)
    for rows in csv_input:
        if ((len(rows[1])<1) & (len(rows[2])<1)) | (len(rows[5])<1) | (len(rows[6])<1):
            continue
        data_superpage = superpage_name_search(rows)
        if data_superpage:
            if data_superpage['status'] == 'addressMatch':
                wrtr_addr_match.writerow(data_superpage['data'])
                continue
        data_peoplefinder = peoplefinder_name_search(rows)
        if data_peoplefinder:
            if data_peoplefinder['status'] == 'addressMatch':
                wrtr_addr_match.writerow(data_peoplefinder['data'])
                continue
            wrtr_no_addr_match.writerows(data_peoplefinder['data'])
        if data_superpage:
            if data_superpage['type'] == 'singleRecord':
                wrtr_no_addr_match.writerow(data_superpage['data'])
            else:
                wrtr_no_addr_match.writerows(data_superpage['data'])
        if len(rows[3])<1:            
            continue
        addr_superpage_data = superpage_addr_search(rows)
        wrtr_ln_match_addr.writerows(addr_superpage_data['last_name_match'])
        wrtr_no_ln_match_addr.writerows(addr_superpage_data['no_last_name_match'])
    outputfile_1.close()
    outputfile_2.close()
