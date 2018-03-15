# -*- coding: utf-8 -*-
from tools import JsonConf
from settings import *

varName_cat_map = {
'IO_v52_proxy_bin': 'true',
'IS_v60_seller_leaf_riskiness': 'true',
'U2_strategy_seller_region': 'true',
'NDYSN_network_operator': 'true',
'IA_v35_ip_ph_geo_worst': 'true',
'IA_v35_ip_conn_type_indicative': 'true',
'NDYSN_time_zone_name': 'true',
'TXNOPT_spp_calculated': 'true',
'DYSN_device_OS': 'true',
'IF_v40_ebay_item_kosherness': 'true',
'IO_v52_is_dg': 'true',
'NDYSN_phone_type': 'true',
'NDYSN_device_model': 'true',
'IF_v40_vpn_trig': 'true',
'NDYSN_os_type': 'true',
'SN_isTrustedIP': 'true',
'DYSN_app_version': 'true',
'NDYSN_os_version': 'true',
'GEO_DE_TWO_LETTER_COUNTRY': 'true',
'IR_cache_r_v3_ip_ad_dist_3d_worst': 'true',
}

varName_noncat_map = {
'U1_name_email_matched': 'true',
'MDL3_CAM17_V2_GBT_2_SCORE': 'false',
'RS_total_payment_rcvd_num': 'false',
'U1_is_dcc_or_wax_user': 'true',
'MDL3_CAM17_V2_NN_3_SCORE': 'false',
'TXN_is_shadow': 'true',
'IU2_v78_risky_prmry_address': 'true',
'MDL3_CAM17_V2_EMS_SCORE': 'false',
'CC_oldest_active_CC_TOF': 'false',
'MDL3_ATOM17V2_SCORE': 'false',
'CC_num_of_active_CCs': 'false',
'MDL3_ATOM17V2_SEG2_GBT1_SCORE': 'false',
'II_v41_e_age': 'false',
'CC_youngest_active_CC_TOF': 'false',
'TXN_has_cc': 'true',
'TXN_is_braintree': 'true',
'CC_added_in_last_3_days': 'false',
'MDL3_CAM17_V2_NN_1_SCORE': 'false',
'CC_added_in_last_90_days': 'false',
'CC_num_of_currency_matched_CCs': 'false',
'DMT_is_DORMANT_9M': 'true',
'MDL3_CLSN17_score': 'false',
'IU2_v78_risky_ship_address': 'true',
'STR1_strategy_eligible_cc': 'true',
'CC_oldest_CC_TOF': 'false',
'TXN_is_GCMall': 'true',
'TXN_is_wallet': 'true',
'IU_v77_is_copy_paste': 'true',
'TXN2_is_digital_goods': 'true',
'MDL3_ATOM17V2_WAX_GBT1_SCORE': 'false',
'MDL3_ATOM17V2_SEG2_H2O1_SCORE': 'false',
'TXN_is_onetouch': 'true',
'CC_youngest_CC_TOF': 'false',
'SN_isTrusted': 'true',
'DMT_is_DORMANT_12M_AND_NOLOGIN': 'true',
'IU2_v78_cons_ship_address': 'true',
'AD_shipping_TOF': 'false',
'MDL3_N2G17_V1_CC_SCORE': 'false',
'MDL3_ATOM17V2_SEG1_NN2_SCORE': 'false',
'MDL3_ATOM17V2_SEG1_NN1_SCORE': 'false',
'MDL3_CAM17_V2_NN_2_SCORE': 'false',
'MDL2_CLV17_1ST_SEND_SCORE': 'false',
'IU_v73_risky_rcvr': 'true',
'U1_user_group': 'true',
'U1_is_verified': 'true',
'AD_shipping_is_confirmed': 'true',
'TXN_is_PPH': 'true',
'CC_num_of_active_debitCC': 'false',
'MDL3_ATOM17V2_SEG1_SCORE': 'false',
'MDL_CAM15V1_SEG': 'true',
'MDL3_CAM17_V2_GBT_1_SCORE': 'false',
'U1_is_prepaid': 'true',
'IK_v41_cnt_tx_rcvd_last_90_d_rcvr': 'false',
'DMT_is_DORMANT_36M': 'true',
'IU2_v78_rcvr_dvc_link_rest': 'true',
'TXN2_is_billAgr_creation': 'true',
'MDL2_CLV16_TPV_SCORE': 'false',
'DMT_is_DORMANT_36M_AND_NOLOGIN': 'true',
'DMT_is_DORMANT_9M_AND_NOLOGIN': 'true',
'MDL2_UBSM16_score': 'false',
'DMT_is_DORMANT_12M': 'true',
'RS_lifetime_num_of_payments_sent': 'false',
'TXN_is_PPPlus': 'true',
'SN_isTrustedVID': 'true',
}

varName_date_map = {
'IU_v73_risky_rcvr':'2017-08-14',
'IU_v77_is_copy_paste':'2017-07-15',
'IU2_v78_cons_ship_address':'2017-11-01',
'IU2_v78_rcvr_dvc_link_rest':'2017-11-01',
'IU2_v78_risky_prmry_address':'2017-11-01',
'IU2_v78_risky_ship_address':'2017-11-01',
'MDL2_CLV17_1ST_SEND_SCORE':'2017-03-14',
'MDL3_ATOM17V2_SCORE':'2017-09-18',
'MDL3_ATOM17V2_SEG1_NN1_SCORE':'2017-12-16',
'MDL3_ATOM17V2_SEG1_NN2_SCORE':'2017-12-16',
'MDL3_ATOM17V2_SEG1_SCORE':'2017-12-16',
'MDL3_ATOM17V2_SEG2_GBT1_SCORE':'2017-09-19',
'MDL3_ATOM17V2_SEG2_H2O1_SCORE':'2017-09-19',
'MDL3_ATOM17V2_WAX_GBT1_SCORE':'2017-09-19',
'MDL3_CAM17_V2_EMS_SCORE':'2017-08-04',
'MDL3_CAM17_V2_GBT_1_SCORE':'2017-08-04',
'MDL3_CAM17_V2_GBT_2_SCORE':'2017-08-04',
'MDL3_CAM17_V2_NN_1_SCORE':'2017-08-04',
'MDL3_CAM17_V2_NN_2_SCORE':'2017-08-04',
'MDL3_CAM17_V2_NN_3_SCORE':'2017-08-04',
'MDL3_CLSN17_score':'2017-08-04',
'MDL3_N2G17_V1_CC_SCORE':'2017-12-15',
}


def _generateCCVarJson(name, is_categorical, date='2017-04-01'):
    """Post var json sample:
    {
            "name": "MDL2_ATOM_SEG3_S1_score",
            "dc_rule_id": -1,
            "checkpoint": "funding",
            "source": "tt",
            "available_from": "2017-08-01T19:37:57.000000Z",
            "is_categorical": false,
            "type": "float",
            "skip_translation": false,
            "table": "funding/common"
    }
    :return:
    """
    jsonString = """
    "name": "{}",
    "dc_rule_id": -1,
    "checkpoint": "funding",
    "source": "tt",
    "available_from": "{}T20:00:00.000000Z",
    "is_categorical": {},
    "type": "{}",
    "skip_translation": false,
    "table": "funding/common"
    """
    _type = "string" if is_categorical=="true" else "float"
    jsonString = jsonString.format(name, date, is_categorical, _type)
    jsonString = "{" + jsonString + "}"
    return jsonString

def generateCCVarJsons(varName_isCat_map, varName_date_map=None):
    ccVarJsonList = []
    for varName, isCat in varName_isCat_map.iteritems():
        if varName in varName_date_map:
            ccVarJsonList.append(_generateCCVarJson(varName, isCat, varName_date_map[varName]))
        else:
            ccVarJsonList.append(_generateCCVarJson(varName, isCat))
    ccVarJsonsString = ',\n'.join(ccVarJsonList)
    return "[\n"+ccVarJsonsString+"\n]"

def generateCCVarJsonEmpty(num=5):
    ccVarJsonList = []
    for i in range(0, num):
        ccVarJsonList.append(_generateCCVarJson("", ""))
    ccVarJsonsString = ',\n'.join(ccVarJsonList)
    return "[\n" + ccVarJsonsString + "\n]"

def transform_groupvar_string_format(varlist):
    newList = []
    for var in varlist:
        newList.append(var.replace('_', '.', 1))
    return newList


if __name__ == '__main__':
    # ccVarJsonsString_cat = generateCCVarJsons(varName_cat_map, varName_date_map)
    # print ccVarJsonsString_cat
    # ccVarJsonsString_noncat = generateCCVarJsons(varName_noncat_map, varName_date_map)
    # print ccVarJsonsString_noncat

    ccVarJsonsString_empty = generateCCVarJsonEmpty(5)
    print ccVarJsonsString_empty
