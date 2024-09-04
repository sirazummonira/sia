from typing_extensions import Self
from monseigneur.core.browser.pages import HTMLPage, JsonPage, pagination, Page
from monseigneur.core.browser.elements import ItemElement, ListElement, method, DictElement
from monseigneur.core.browser.filters.html import Link, AbsoluteLink
from monseigneur.core.browser.filters.json import Dict
from monseigneur.core.browser.filters.standard import CleanText, Regexp, CleanDecimal, Currency, DateTime, Env, Field, Currency as CleanCurrency, CleanDate
from monseigneur.modules.public.sia.alchemy.tables import Members, Offices
from Crypto.Cipher import AES
from base64 import b64decode
import re

import json

class ListPage(HTMLPage):

    ENCODING = 'UTF8'

    def build_doc(self, content):

        self.html_doc = HTMLPage.build_doc(self, content)

        add_content = CleanText('//script[contains(text(), "__REDIAL_PROPS__")]')(self.html_doc)

        add_content = add_content.replace('window.__REDIAL_PROPS__ =', '')
        add_content = json.loads(add_content)

        for content in add_content:
            if content != None:
                self.doc = content
                return self.doc

class MemberListPage(HTMLPage):
    @method
    class iter_members(ListElement):
        item_xpath = '//table//tr[not(contains(@class,"header"))]'
        class get_members(ItemElement):
            klass = Members
            def obj_member_id(self):
                #return self.page.url
                #member_id = re.findall(r'(\d+)', indv_url)[0]
                url = 'https://www.sia.ch'+(self.xpath('./td[1]/a/@href')[0])
                return re.findall(r'(\d+)', url)[0]
            def obj_url(self):
                #return self.page.url
                #member_id = re.findall(r'(\d+)', indv_url)[0]
                return 'https://www.sia.ch'+(self.xpath('./td[1]/a/@href')[0])
            def obj_zipcode(self):
                zip = self.xpath('./td[4]/text()')
                if zip:
                    return zip[0]
                else:
                    return
            def obj_city(self):
                city = self.xpath('./td[5]/text()')
                if city:
                    return city[0]
                else:
                    return

            def obj_language(self):
                #print(self.obj_zipcode())
                if self.obj_zipcode():
                    if (self.page.browser.df['ZIP_CODE'].eq(int(self.obj_zipcode()))).any():
                        lang = self.page.browser.df.loc[self.page.browser.df['ZIP_CODE'] == int(self.obj_zipcode())].LANGUAGE.item() #get lang by comparing zip with excel
                    else:
                        lang = 'FR'
                else:
                    lang = 'FR'
                return lang

def pad(data, ks):
            pad_len = (ks - (len(data) % ks)) % ks 
            return data + (b'\x00' * pad_len)

def kdf(pwd, keySize): 
    if keySize != 16 and keySize != 24 and keySize != 32:
        raise ValueError("Wrong keysize") 
    keyPadded = pwd[:keySize] if len(pwd) >= keySize else pad(pwd, keySize)
    aes = AES.new(key=keyPadded, mode=AES.MODE_ECB) 
    key = aes.encrypt(keyPadded[:16])
    if keySize > 16:
        key = (key + key)[:keySize]
    return key

def clean_list(list2clean):
    clean_list = []
    #clean full address
    for element in list2clean:
        clean_list.append(element.strip())
    return list(filter(lambda e: e != '', clean_list))

class MemberPage(HTMLPage):
    @method
    class get_members_details(ItemElement):
        klass = Members
        def obj_full_address(self):
            #print('Full address:', clean_list(self.xpath('//table//tr[2]/td/text()')))
            full_address = clean_list(self.xpath('//table//tr[2]/td/text()'))
            while(len(full_address)<6):
                        full_address.append('')
            full_address_str = " ".join(full_address)
            return full_address_str
        def obj_gender(self):
            #print('Gender:', clean_list(self.xpath('//table//tr[2]/td/text()'))[0])
            full_address = clean_list(self.xpath('//table//tr[2]/td/text()'))
            while(len(full_address)<6):
                        full_address.append('')
            return full_address[0]
        def obj_name(self):
            #print('Name:', clean_list(self.xpath('//table//tr[2]/td/text()'))[1])
            full_address = clean_list(self.xpath('//table//tr[2]/td/text()'))
            while(len(full_address)<6):
                        full_address.append('')
            if 'Dr.' in full_address[1] or 'Prof.' in full_address[1]:
                #print('Nameeeeee:', full_address[1])
                return full_address[1]+" "+full_address[2]
            else:
                return full_address[1]
        def obj_education(self):
            #print('Education:', clean_list(self.xpath('//table//tr[2]/td/text()'))[2])
            full_address = clean_list(self.xpath('//table//tr[2]/td/text()'))
            while(len(full_address)<6):
                        full_address.append('')
            if 'Dr.' in full_address[1] or 'Prof.' in full_address[1]:
                return full_address[3]
            else:
                return full_address[2]
        def obj_address(self):
            #print('Address:', clean_list(self.xpath('//table//tr[2]/td/text()'))[3])
            full_address = clean_list(self.xpath('//table//tr[2]/td/text()'))
            while(len(full_address)<6):
                        full_address.append('')
            if 'Dr.' in full_address[1] or 'Prof.' in full_address[1]:
                return full_address[4]
            else:
                return full_address[3]
        '''def obj_city(self):
            #print('Gender:', clean_list(self.xpath('//table//tr[2]/td/text()'))[4])
            full_address = clean_list(self.xpath('//table//tr[2]/td/text()'))
            while(len(full_address)<6):
                        full_address.append('')
            if 'Dr.' in full_address[1] or 'Prof.' in full_address[1]:
                #return full_address[5]
                cityzip  = full_address[5][:4]
                if(cityzip.isnumeric()):
                    city = full_address[5].replace(cityzip,"")
                    return city
                else:
                    return full_address[5]
            else:
                #return full_address[4]
                cityzip  = full_address[4][:4]
                if(cityzip.isnumeric()):
                    city = full_address[4].replace(cityzip,"")
                    return city
                else:
                    return full_address[4]'''

        def get_decryption(self):
            data_contact = self.xpath('//@data-contact')
            if data_contact:
                data_contact=data_contact[0]
            else:
                data_contact=''
            data_secret = self.xpath('//@data-secr')
            if data_secret:
                data_secret=data_secret[0]
            else:
                data_secret = ''
            ciphertext = b64decode(data_contact)
            nc = ciphertext[:8]
            data = ciphertext[8:]

            keySize = 32
            pwd = data_secret #from data-secr
            key = kdf(pwd.encode('utf-8'), keySize) 
            aes = AES.new(key=key, mode=AES.MODE_CTR, nonce=nc) 
            res = aes.decrypt(data)
            result = res.decode('utf-8')
            #tel = result[0:13]
            email = re.findall(r'[\w.+-]+@[\w-]+\.[\w.-]+', result)
            if email:
                email = email[0]
            else:
                email=''
            phone_fax=re.findall(r"(\+\d\d\s*\d(?:\d)+)",result)
            if phone_fax and len(phone_fax)==2:
                tel = phone_fax[0]
                fax = phone_fax[1]
            elif phone_fax and len(phone_fax)==1:
                tel = phone_fax[0]
                fax = ''
            else:
                tel = ''
                fax = ''
            website = re.search('_blank">(.*)</a><br />', result)
            if website:
                website = website.group(1)
            else:
                website=''

            return email, tel, fax, website

        def obj_email(self):
            email, tel, fax, website = self.get_decryption()
            return email
        def obj_tel(self):
            email, tel, fax, website = self.get_decryption()
            return tel
        def obj_fax(self):
            email, tel, fax, website = self.get_decryption()
            return fax
        def obj_website(self):
            email, tel, fax, website = self.get_decryption()
            return website

        def obj_job(self):
            job = self.xpath('//table//tr[6]/td[2]//text()')
            if job:
                return clean_list(job)[0]
            else:
                return
        def obj_sector(self):
            sector = self.xpath('//table//tr[7]/td[2]//text()')
            if sector:
                sector = clean_list(sector)
                sector_str = ", ".join(sector)
                return sector_str
            else:
                return
        def obj_group(self):
            group = self.xpath('//table//tr[8]/td[2]//text()')
            if group:
                return clean_list(group)[0]
            else:
                return
        def obj_section(self):
            section = self.xpath('//table//tr[9]/td[2]//text()')
            if section:
                return clean_list(section)[0]
            else:
                return
            


class OfficeListPage(HTMLPage):
    @method
    class iter_offices(ListElement):
        item_xpath = '//table//tr[not(contains(@class,"header"))]'
        class get_offices(ItemElement):
            klass = Offices
            def obj_office_id(self):
                #return self.page.url
                #member_id = re.findall(r'(\d+)', indv_url)[0]
                url = 'https://www.sia.ch'+(self.xpath('./td[1]/a/@href')[0])
                return re.findall(r'(\d+)', url)[0]
            def obj_url(self):
                #return self.page.url
                #member_id = re.findall(r'(\d+)', indv_url)[0]
                return 'https://www.sia.ch'+(self.xpath('./td[1]/a/@href')[0])
            def obj_zipcode(self):
                zip = self.xpath('./td[4]/text()')
                if zip:
                    return zip[0]
                else:
                    return
            def obj_city(self):
                city = self.xpath('./td[5]/text()')
                if city:
                    return city[0]
                else:
                    return

            def obj_language(self):
                #print(self.obj_zipcode())
                if self.obj_zipcode():
                    if (self.page.browser.df['ZIP_CODE'].eq(int(self.obj_zipcode()))).any():
                        lang = self.page.browser.df.loc[self.page.browser.df['ZIP_CODE'] == int(self.obj_zipcode())].LANGUAGE.item() #get lang by comparing zip with excel
                    else:
                        lang = 'FR'
                else:
                    lang = 'FR'
                return lang

class OfficePage(HTMLPage):
    def get_member_list(self):
            joined_members_url = self.doc.xpath('//*[contains(text(),"SIA")]//ancestor::tr/following-sibling::tr[1]//a/@href')
            if joined_members_url:
                joined_members_id = re.findall(r'\/(\d+)\/',joined_members_url[0])
                return joined_members_id
            else:
                return
    @method
    class get_offices_details(ItemElement):
        klass = Offices
        def obj_full_address(self):
            full_address = clean_list(self.xpath('//div/table//tr[2]/td/text()'))
            while(len(full_address)<4):
                        full_address.append('')
            full_address_str = " ".join(full_address)
            return full_address_str
            #return self.xpath('//table//tr[2]/td/text()')
        def obj_name(self):
            full_address = clean_list(self.xpath('//div/table//tr[2]/td/text()'))
            if len(full_address)>1:
                return full_address[0]
            else:
                return
            #return self.xpath('//table//tr[2]/td[1]/text()')[1]
        def obj_address(self):
            full_address = clean_list(self.xpath('//div/table//tr[2]/td/text()'))
            if len(full_address)>1:
                if(len(full_address)<4):
                    while(len(full_address)<4):
                        full_address.append('')
                    return full_address[1]
                else:
                    return full_address[2]
            else:
                return
            #return self.xpath('//table//tr[2]/td[1]/text()')[2]
        '''def obj_city(self):
            full_address = clean_list(self.xpath('//div/table//tr[2]/td/text()'))
            if len(full_address)>1:
                if(len(full_address)<4):
                    while(len(full_address)<4):
                        full_address.append('')
                    return full_address[2]
                else:
                    return full_address[3]
            else:
                return'''
            #return self.xpath('//table//tr[2]/td[1]/text()')[3]

        def get_decryption(self):
            data_contact = self.xpath('//@data-contact')
            if data_contact:
                data_contact=data_contact[0]
            else:
                data_contact=''
            data_secret = self.xpath('//@data-secr')
            if data_secret:
                data_secret=data_secret[0]
            else:
                data_secret = ''
            ciphertext = b64decode(data_contact)
            nc = ciphertext[:8]
            data = ciphertext[8:]

            keySize = 32
            pwd = data_secret #from data-secr
            key = kdf(pwd.encode('utf-8'), keySize) 
            aes = AES.new(key=key, mode=AES.MODE_CTR, nonce=nc) 
            res = aes.decrypt(data)
            result = res.decode('utf-8')
            #tel = result[0:13]
            email = re.findall(r'[\w.+-]+@[\w-]+\.[\w.-]+', result)
            if email:
                email = email[0]
            else:
                email=''
            phone_fax=re.findall(r"(\+\d\d\s*\d(?:\d)+)",result)
            if phone_fax and len(phone_fax)==2:
                tel = phone_fax[0]
                fax = phone_fax[1]
            elif phone_fax and len(phone_fax)==1:
                tel = phone_fax[0]
                fax = ''
            else:
                tel = ''
                fax = ''
            website = re.search('_blank">(.*)</a><br />', result)
            if website:
                website = website.group(1)
            else:
                website=''

            return email, tel, fax, website

        def obj_email(self):
            email, tel, fax, website = self.get_decryption()
            return email
        def obj_tel(self):
            email, tel, fax, website = self.get_decryption()
            return tel
        def obj_fax(self):
            email, tel, fax, website = self.get_decryption()
            return fax
        def obj_website(self):
            email, tel, fax, website = self.get_decryption()
            return website
        def obj_sector(self):
            sector = self.xpath('//tr[6]/td/ul//text()')
            if sector:
                sector = clean_list(sector)
                sector_str = ", ".join(sector)
                return sector_str
            else:
                return

