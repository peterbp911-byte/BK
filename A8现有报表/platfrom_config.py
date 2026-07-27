# -*- coding: utf-8 -*-
import json
import os
from platform import platform

PLATFROM_CONFIGS = {
'A8': {
    'USERNAME': 'a8sport_SJ',
    'PASSWORD': 'zxc123qwe',
    "google_key":'C47H6MM3BEEVFUN5',
    'LOGIN_PAGE_URL': 'https://admin-tenant.t1game888.com/',
    'session_url': 'https://admin-tenant.t1game888.com/welcome/index',
    'opr_url': 'https://admin-tenant.t1game888.com/liveAdmin/reportQuery/operationsStatisPageList',
    'game_url': 'https://admin-tenant.t1game888.com/liveAdmin/ch/report/game/gameStatisReport',
    'dRe_url': 'https://admin-tenant.t1game888.com/liveAdmin/fyl/agent/depositMemberRecord',
    'kpi_url': 'https://admin-tenant.t1game888.com/liveAdmin/ch/report/daily/platformDailyRevenue',
    'ReRetaintion_url': 'https://admin-tenant.t1game888.com/liveAdmin/retain/userRechargeRetainPageList',  
    'BetRetaintion_url': 'https://admin-tenant.t1game888.com/liveAdmin/retain/userBetRetainPageList'
    },
'T1': {
    'USERNAME': 'T1sport_SJ',
    'PASSWORD': 'zxc123qwe',
    "google_key":'GP62SFBOK7FY56UZ',
    'LOGIN_PAGE_URL': 'https://admin-tenant.t1game888.com/',
    'session_url': 'https://admin-tenant.t1game888.com/welcome/index',
    'opr_url': 'https://admin-tenant.t1game888.com/liveAdmin/reportQuery/operationsStatisPageList',
    'game_url': 'https://admin-tenant.t1game888.com/liveAdmin/ch/report/game/gameStatisReport',
    'dRe_url': 'https://admin-tenant.t1game888.com/liveAdmin/fyl/agent/depositMemberRecord',
    'kpi_url': 'https://admin-tenant.t1game888.com/liveAdmin/ch/report/daily/platformDailyRevenue',
    'ReRetaintion_url': 'https://admin-tenant.t1game888.com/liveAdmin/retain/userRechargeRetainPageList',    
    'BetRetaintion_url': 'https://admin-tenant.t1game888.com/liveAdmin/retain/userBetRetainPageList',
    },
'M9': {
    'USERNAME': 'M9sport_SJ',
    'PASSWORD': 'zxc123qwe',
    "google_key":'EYH7Z7NGFNIIMDLL',
    'LOGIN_PAGE_URL': 'https://admin-tenant.t1game888.com/',
    'session_url': 'https://admin-tenant.t1game888.com/welcome/index',
    'opr_url': 'https://admin-tenant.t1game888.com/liveAdmin/reportQuery/operationsStatisPageList',
    'game_url': 'https://admin-tenant.t1game888.com/liveAdmin/ch/report/game/gameStatisReport',
    'dRe_url': 'https://admin-tenant.t1game888.com/liveAdmin/fyl/agent/depositMemberRecord',
    'kpi_url': 'https://admin-tenant.t1game888.com/liveAdmin/ch/report/daily/platformDailyRevenue',
    'ReRetaintion_url': 'https://admin-tenant.t1game888.com/liveAdmin/retain/userRechargeRetainPageList',    
    'BetRetaintion_url': 'https://admin-tenant.t1game888.com/liveAdmin/retain/userBetRetainPageList',
    }
    
# ,'HY': {
#     'USERNAME': ' Jacky@gmail.com',
#     'PASSWORD': 'aa123321',
#     "haiyue_key":'088345331',

#     'LOGIN_PAGE_URL': 'https://admin-tenant.t1game888.com/',
#     'session_url': 'https://admin-tenant.t1game888.com/welcome/index',
#     'opr_url': 'https://admin-tenant.t1game888.com/liveAdmin/ch/campaign/redemption_codes/new',
#     'game_url': 'https://admin-tenant.t1game888.com/liveAdmin/ch/report/game/gameStatisReport',
#     'dRe_url': 'https://admin-tenant.t1game888.com/liveAdmin/fyl/agent/depositMemberRecord',
#     'kpi_url': 'https://admin-tenant.t1game888.com/liveAdmin/ch/report/daily/platformDailyRevenue',
#     "re_url":'https://admin-tenant.t1game888.com/liveAdmin/ch/campaign/redemption_codes',
#     "wi_url":'https://admin-tenant.t1game888.com/liveAdmin/ch/campaign/redemption_codes',
#     "use_url": 'https://admin-tenant.t1game888.com/liveAdmin/ch/user/userList',  
#     "betR_url": 'https://admin-tenant.t1game888.com/liveAdmin/ch/report/game/gameStatisReport'
#     }


}

def get_platfrom_config(platfrom_name):
    return PLATFROM_CONFIGS.get(platfrom_name)


def get_platfrom_cookies(platfrom_name):
    """从 JSON文件读取平台 Cookie"""
    cookies_file = f"C:/Users/Richa/Desktop/A8现有报表/session/cookies_{platfrom_name}.json"
    if not os.path.exists(cookies_file):
        return None
    
    try:
        with open(cookies_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return None

