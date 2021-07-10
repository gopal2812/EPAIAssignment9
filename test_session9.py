from session9 import *
import session9 as session9
from datetime import datetime, date
import pytest
from io import StringIO
import sys
import time
import inspect
import os
import re
from faker import Faker
from decimal import Decimal

fake = Faker()

README_CONTENT_CHECK_FOR = [
    "calc_time",
    "oldest_person_in_namedtuple",
    "average_age_in_namedtuple",
    "average_coords_in_namedtuple",
    "max_bloodgroup_in_namedtuple",
    "oldest_person_dict",
    "average_age_dict",
    "average_coords_dict",
    "max_bloodgroup_dict",
    "symbol",
    "stock_market"
]

def test_readme_exists():
    assert os.path.isfile("README.md"), "README.md file missing!"

def test_readme_contents():
    readme = open("README.md", "r")
    readme_words = readme.read().split()
    readme.close()
    assert len(readme_words) >= 500, "Make your README.md file interesting! Add atleast 500 words"

def test_readme_proper_description():
    READMELOOKSGOOD = True
    f = open("README.md", "r", encoding="utf-8")
    content = f.read()
    f.close()
    for c in README_CONTENT_CHECK_FOR:
        if c not in content:
            print(c)
            READMELOOKSGOOD = False
            pass
    assert READMELOOKSGOOD == True, "You have not described all the functions/class well in your README.md file"

def test_readme_file_for_formatting():
    f = open("README.md", "r", encoding="utf-8")
    content = f.read()
    f.close()
    assert content.count("#") >= 10

def test_function_name_had_cap_letter():
    functions = inspect.getmembers(session9, inspect.isfunction)
    for function in functions:
        assert len(re.findall('([A-Z])', function[0])) == 0, "You have used Capital letter(s) in your function names"


Profile = namedtuple('Profile', fake.profile().keys())
named_tuples = [Profile('AP','GH', '200-000-222','Texas',(Decimal('-46.204908'), Decimal('-168.530504')), 'O+','www.ddd.com','GP','KS', 'M','qqq','s@dys.com', date(1968, 1, 25)),
                Profile('PQ','GCB','000-000-000','Austin',(Decimal('75.9842075'), Decimal('-17.257017')), 'B+','www.www.www','WD','JB','F','AAA','sdg', date(1921, 10, 25)),
                Profile('QR','DFG','000-111-000','AX',(Decimal('-43.994425'), Decimal('107.105065')),'O-','sss','IS','AC','F','SSS','GHF',date(1993, 3, 20)),
                Profile('RT','DD','000-222-333','DS',(Decimal('-6.979771'), Decimal('-51.459563')),'O+','www','DG','CD','F','SDF','DFT',date(1981, 3, 28)),
                Profile('TE','BL','000-333-444','SW',(Decimal('-7.1557865'), Decimal('142.414900')), 'A+','ert','MR','BS','M','SWQ','dfr',date(1934, 11, 12))
                ]


# Question1 Test cases


def test_q1_number_of_nt_profiles():
    assert len(init_profiles_using_namedtuple(100)) == 100 ,'Please create 100 profiles'

def test_q1_average_age_nt():
    assert average_age_in_namedtuple(named_tuples)[1] == 61.2, "PLease check the average age function"

def test_q1_oldest_person_nt():
    assert oldest_person_in_namedtuple(named_tuples)[1] == 99, "PLease check the oldest age function"

def test_q1_average_coords_nt():
    assert average_coords_in_namedtuple(named_tuples)[1] == (Decimal('-5.6701366'), Decimal('2.4545762')), "PLease check the avg coord function"

def test_q1_max_bloodgroup_nt():
    assert max_bloodgroup_in_namedtuple(named_tuples)[1] == 'O+', "Please check the max blood group function"

# Question 2 Test cases

fk_Profile_dict = namedtupletodict(named_tuples)

def test_q2_type_of_value():
    assert type(fk_Profile_dict) == dict,'Please check the namedtuple to dictionary conversion function'

def test_q2_average_age_dict():
    assert average_age_dict(fk_Profile_dict)[1] == 61.2, "PLease check the average age function"

def test_q2_oldest_person_dict():
    assert oldest_person_dict(fk_Profile_dict)[1] == 99, "PLease check the oldest age function"

def test_q2_average_coords_dict():
    assert average_coords_dict(fk_Profile_dict)[1] == (Decimal('-5.6701366'), Decimal('2.4545762')), "PLease check the avg coord function"

def test_q2_max_bloodgroup_dict():
    assert max_bloodgroup_dict(fk_Profile_dict)[1] == 'O+', "Please check the max blood group function"

def test_q2_fastest_nt_dict():
    fk_Profile_nt = init_profiles_using_namedtuple(10000)
    fk_Profile_dict = namedtupletodict(fk_Profile_nt)
    assert time_for_named_tuple(fk_Profile_nt, 100) < time_for_dict(fk_Profile_dict, 100), 'How can dict be faster than named tuple CHECK!!'

# Question 3
N = 100
stVals = stock_market(N)

def test_q3_number_profiles():
    assert len(stock_market(100)[0]) == 100, 'Not enough profiles'

def test_q3_doc_string():
    assert stock_market.__doc__ != None, 'Please provide a doc string'

def test_q3_annotations():
    assert stock_market.__annotations__ != None, 'Please provide appropriate annotations'

def test_q3_unique_symbol():
    symbols = len(set([x.symbol for x in stVals[0]]))
    assert symbols == N, 'Duplicate Symbols found'

def test_q3_return_namedt():
    assert type(stVals[0][0]) != tuple, 'Check the function'

def test_q3_normalized_wts():
    wts_sum = sum([x.company_weight for x in stVals[0]])
    assert wts_sum >= 0.9, 'Normalize the weights'

def test_q3_close_gt_zero():
    close = [x.close for x in stVals[0]]
    min_close = min(close)
    assert min_close >= 0 , 'min close should be greater than zero'

def test_q3_high_gt_zero():
    high = [x.high for x in stVals[0]]
    min_high = min(high)
    assert min_high >= 0 , 'min high should be greater than zero'

def test_q3_open_gt_zero():
    open = [x.open for x in stVals[0]]
    min_open = min(open)
    assert min_open >= 0 , 'min open should be greater than zero'

def test_q3_highd_lowd():
    assert stVals[2] >= stVals[3], 'How can highest be less than lowest'

def test_q3_docstring_namedtuple():
    assert stVals[0][1].__doc__ != None, 'No docstring for the tuple'

def test_q3_docstring_symbol():
    assert symbol.__doc__ != None, 'Doc string missing'

def test_q3_string_annotations():
    assert symbol.__annotations__ != None, 'Provide annotattions'
