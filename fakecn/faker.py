import re
from datetime import datetime,timedelta
from fakecn.fake import *

class Id():
    def __init__(self,number:str=None):
        self.rand=fake_id
        self.random=self.rand
        self.load(number)

    def load(self,number)->None:
        if number:
            self.str=str(number).upper()
            if len(self)!=18:
                raise ValueError(self.str)
        else:
            self.str=self.rand()
        self.area_id=self.str[0:6]
        self.area_name=area_id2name[self.area_id]
        self.birth=self.str[6:14]
        self.birth_year=self.str[6:10]
        self.birth_month=self.str[10:12]
        self.birth_day=self.str[12:14]
        self.ex_id=self.str[14:16]
        self.sex_id=self.str[16]
        self.check_digit=self.str[17]

    def verify(self,x:str=None)->str:
        if x:
            return Id(x).verify()

        if len(self)!=18:
            return 'Length error'
        if not re.match(r'^\d{17}[\dX]$',self.str):
            return 'Format error'

        if self.area_id not in area_id2name:
            return 'Area error'

        if self.birth_year<'1901' or self.birth_year>'2099':
            return 'Birth year error'

        try:
            datetime.strptime(self.birth_year+self.birth_month+self.birth_day,"%Y%m%d")
        except ValueError:
            return 'Birth date error'

        if self.check_digit!=id_check_digit(self.str[:-1]):
            return 'Check digit error'

        return ''


    def get_age(self,number:str=None)->int:
        if number:
            return Id(number).get_age()
        now=(datetime.now()+timedelta(days=1))
        return now.year-self.birth_year-int(self.birth_month>now.month or(self.birth_month==now.month and self.birth_day>now.day))

    def get_sex(self,number:str=None)->str:
        if number:
            return Id(number).get_sex()
        return ['female','male'][int(self.sex_id)&1]

    def __str__(self)->str:
        return self.str
    def __len__(self)->int:
        return len(self.str)


class Name():
    def __init__(self,name:str=None):
        self.rand=fake_name
        self.random=self.rand
        self.load(name)

    def load(self,name:str)->None:
        if name:
            self.str=str(name)
        else:
            self.str=self.rand()
        if self.str[:2] in name_last and len(self)>2:
            self.last=self.str[:2]
            self.first=self.str[2:]
        else:
            self.last=self.str[0]
            self.first=self.str[1:]

    def verify(self,x:str=None)->str:
        if x:
            return Name(x).verify()
        if len(self)<2 or len(self)>5:
            return 'Length error'
        if re.match(r'[\da-zA-Z_\s]',self.str):
            return 'Format error'
        return ''

    def __str__(self)->str:
        return self.str
    def __len__(self)->int:
        return len(self.str)


class Mobile():
    def __init__(self,mobile_number:str=None):
        self.rand=fake_mobile
        self.random=self.rand
        self.load(mobile_number)

    def load(self,mobile_number)->None:
        if mobile_number:
            self.str=str(mobile_number)
        else:
            self.str=self.rand()
        self.prefix=self.str[:3]
        self.isp=None
        for i in mobile_prefix:
            if self.str[:3] in i:
                self.isp=i
                break

    def verify(self,x:str=None)->str:
        if x:
            return Mobile(x).verify()
        if len(self)!=11:
            return 'Length error'
        if not re.match(r'^1\d{10}$',self.str):
            return 'Format error'
        return ''

    def __str__(self)->str:
        return self.str
    def __len__(self)->int:
        return len(self.str)


class Card():
    def __init__(self,number:str=None):
        self.rand=fake_card
        self.random=self.rand
        self.load(number)

    def load(self,number:str=None)->None:
        if number:
            self.str=str(number)
        else:
            self.str=self.rand()
        self.mian=self.str[:-1]
        self.check_digit=self.str[-1]

    def verify(self,x:str=None)->str:
        if x:
            return Id(x).verify()

        for i in bank_bin:
            if self.str.startswith(i) and len(self)!=int(bank_bin[i][-1]):
                return 'Length error'
        if not re.match(r'^\d+$',self.str):
            return 'Format error'

        if card_check_digit(self.str[:-1])!=self.check_digit:
            return 'Check digit error'

        return ''

    def __str__(self)->str:
        return self.str

    def __len__(self)->str:
        return len(self.str)


class Faker():
    def __init__(self,id:str=None,name:str=None,mobile:str=None,card:str=None):
        self.str=Id(id)
        self.name=Name(name)
        self.mobile=Mobile(mobile)
        self.card=Card(card)

    def load(self,id:str,name:str,mobile:str,card:str=None)->None:
        if id:
            self.str=Id(id)
        if name:
            self.name=Name(name)
        if mobile:
            self.mobile=Mobile(mobile)
        if card:
            self.card=Card(card)
        
    def random(self,id:str=None,name:str=None,mobile:str=None,card:str=None):
        return Faker(id,name,mobile,card)

    def verify(self,x=None)->str:
        if x:
            return x.verify()
        ans=dict()
        x=self.str.verify()
        if x:
            ans['id']=x
        x=self.name.verify()
        if x:
            ans['name']=x
        x=self.mobile.verify()
        if x:
            ans['mobile']=x
        x=self.card.verify()
        if x:
            ans['card']=x
        return ans

    def json(self)->dict:
        return {
            'name':str(self.name),
            'mobile':str(self.mobile),
            'id':str(self.str),
            'addr':self.str.area_name,
            'card':str(self.card)
        }
