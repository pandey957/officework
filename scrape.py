from bs4 import BeautifulSoup
from urllib import urlopen, unquote
base_url = 'https://ezbuy.my/category/2647?a=1&isPrime=true'
end_page = 10

def category_links(page_number=0):
    url = base_url + '&page=' + str(page_number)
    data = BeautifulSoup(urlopen(url),'html.parser')
    for item in data.findAll('li','product-item'):
        product_url =  unquote(item.find('h3','text-break').find('a')['href'][20:])
        print product_url
        new_data = BeautifulSoup(urlopen(product_url),'html.parser')
        if new_data.find('div','warning-info '): continue
        title_bs = new_data.find('h3','tb-main-title')
        if title_bs is None:
            title_bs = new_data.find('div','tb-detail-hd')
        title = title_bs.text
        size_color = new_data.findAll('ul','tb-cleafix')
        sizes = []
        colors = []
        for line in size_color[0].findAll('li','J_SKU'):
            sizes.append(line.find('a').find('span').text)
        for line in size_color[1].findAll('li','J_SKU'):
            colors.append(line.find('a').find('span').text)
        body_html = new_data.find('div','tb-des-content')
        variant_pic = []
        for line in new_data.find('ul','tb-pic').findAll('li'):
            variant_pic.append('http:'+line.find('img')['src'])
        print title
    if page_number < end_page:
        category_links(page_number+1)

if __name__ == '__main__':
    category_links()
