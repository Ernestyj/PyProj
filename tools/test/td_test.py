# -*- coding: utf-8 -*-
import os
from tools.td_tools import Teradata
from tools import JsonConf

root_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
conf = JsonConf().get_json_conf(path= root_path + '/conf.json')
conf_td = conf['teradata']

tera = Teradata(host=conf_td['jackal_host'], user_name=conf_td['username'], password=conf_td['password'])
df = tera.query(query_string='''select * from pp_oap_sing_jyang2_t.test;''')
print(df)