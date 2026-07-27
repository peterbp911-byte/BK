# -*- coding: utf-8 -*-
import json
import os
from platform import platform

PLATFROM_CONFIGS = {
     'novo7': {
   'USERNAME': 'Felix',
    'PASSWORD': 'cee00742',
    'LOGIN_PAGE_URL': 'https://admin-st9zepcva1e0vraronus57s.novo7.games/session/new',
    'SESSION_URL': 'https://admin-st9zepcva1e0vraronus57s.novo7.games/dashboard',
    'REDEMPTION_URL': 'https://admin-st9zepcva1e0vraronus57s.novo7.games/campaign/redemption_codes/new',
    'MESSAGE_URL': 'https://admin-st9zepcva1e0vraronus57s.novo7.games/data_report/sms_backflow/query_json',
    'LE_URL': 'https://admin-st9zepcva1e0vraronus57s.novo7.games/user/layers'
    },
'sp7': {
    'USERNAME': 'Felix',
    'PASSWORD': '895b24d6',
    'LOGIN_PAGE_URL': 'https://admin-sqwtdt1j7whj48jwlkh3cok.sp7.games/session/new',
    'SESSION_URL': 'https://admin-sqwtdt1j7whj48jwlkh3cok.sp7.games/dashboard',
    'REDEMPTION_URL': 'https://admin-sqwtdt1j7whj48jwlkh3cok.sp7.games/campaign/redemption_codes/new',
    'MESSAGE_URL': 'https://admin-sqwtdt1j7whj48jwlkh3cok.sp7.games/data_report/sms_backflow/query_json',
    'LE_URL': 'https://admin-sqwtdt1j7whj48jwlkh3cok.sp7.games/user/layers'
    },
    'b7': {
    'USERNAME': 'Felix',
    'PASSWORD': '5f3c6d9c',
    'LOGIN_PAGE_URL': 'https://admin-sfu7ty3whqxta2iccjcv2r9.b7.games/session/new',
    'SESSION_URL': 'https://admin-sfu7ty3whqxta2iccjcv2r9.b7.games/dashboard',
    'REDEMPTION_URL': 'https://admin-sfu7ty3whqxta2iccjcv2r9.b7.games/campaign/redemption_codes/new',
    'MESSAGE_URL': 'https://admin-sfu7ty3whqxta2iccjcv2r9.b7.games/data_report/sms_backflow/query_json',
    'LE_URL': 'https://admin-sfu7ty3whqxta2iccjcv2r9.b7.games/user/layers'
    },
    '1xspin': {
                'USERNAME': 'Felix',
                'PASSWORD': '4bb5196d',
                'LOGIN_PAGE_URL': 'https://admin.sgo79z11raz9mx1v.1xspin.games/session/new',
                'SESSION_URL': 'https://admin.sgo79z11raz9mx1v.1xspin.games/session/dashboard',
                'REDEMPTION_URL': 'https://admin.sgo79z11raz9mx1v.1xspin.games/campaign/redemption_codes/new',
                'MESSAGE_URL': 'https://admin.sgo79z11raz9mx1v.1xspin.games/data_report/sms_backflow/query_json',
                'LE_URL': 'https://admin.sgo79z11raz9mx1v.1xspin.games/user/layers',
                'FU_URL':'https://admin.sgo79z11raz9mx1v.1xspin.games/data_report/user_funds',
                'TASKS_URL':'https://admin.sgo79z11raz9mx1v.1xspin.games/system/backend_tasks'
            },
            'b777': {
                'USERNAME': 'Felix',
                'PASSWORD': '179167da',
                'LOGIN_PAGE_URL': 'https://admin.st9gs87zt10up8185rbztdh.b777.games/session/new',
                'SESSION_URL': 'https://admin.st9gs87zt10up8185rbztdh.b777.games/dashboard',
                'REDEMPTION_URL': 'https://admin.st9gs87zt10up8185rbztdh.b777.games/campaign/redemption_codes/new',
                'MESSAGE_URL': 'https://admin.st9gs87zt10up8185rbztdh.b777.games/data_report/sms_backflow/query_json',
                'LE_URL': 'https://admin.st9gs87zt10up8185rbztdh.b777.games/user/layers',
                'FU_URL': 'https://admin.st9gs87zt10up8185rbztdh.b777.games/data_report/user_funds',
                'TASKS_URL': 'https://admin.st9gs87zt10up8185rbztdh.b777.games/user/system/backend_tasks'
            },
        'brl77': {
            'USERNAME': 'Felix',
            'PASSWORD': '57b9df98',
            'LOGIN_PAGE_URL': 'https://admin-swaqoduc0h8c31r8qgkxfdw.brl77.games/session/new',
            'SESSION_URL': 'https://admin-swaqoduc0h8c31r8qgkxfdw.brl77.games/dashboard',
            'REDEMPTION_URL': 'https://admin-swaqoduc0h8c31r8qgkxfdw.brl77.games/campaign/redemption_codes/new',
            'MESSAGE_URL': 'https://admin-swaqoduc0h8c31r8qgkxfdw.brl77.games/data_report/sms_backflow/query_json',
            'LE_URL': 'https://admin-swaqoduc0h8c31r8qgkxfdw.brl77.games/user/layers',
            'FU_URL': 'https://admin-swaqoduc0h8c31r8qgkxfdw.brl77.games/data_report/user_funds',
            'TASKS_URL': 'https://admin-swaqoduc0h8c31r8qgkxfdw.brl77.games/system/backend_tasks'
        },
        'spin77': {
            'USERNAME': 'Felix',
            'PASSWORD': '7a570e82',
            'LOGIN_PAGE_URL': 'https://admin.s1e1hccnp9dboel2yrosg7q.spin77.games/session/new',
            'SESSION_URL': 'https://admin.s1e1hccnp9dboel2yrosg7q.spin77.games/dashboard',
            'REDEMPTION_URL': 'https://admin.s1e1hccnp9dboel2yrosg7q.spin77.games/campaign/redemption_codes/new',
            'MESSAGE_URL': 'https://admin.s1e1hccnp9dboel2yrosg7q.spin77.games/data_report/sms_backflow/query_json',
            'LE_URL': 'https://admin.s1e1hccnp9dboel2yrosg7q.spin77.games/user/layers',
            "FU_URL":'https://admin.s1e1hccnp9dboel2yrosg7q.spin77.games/data_report/user_funds',
            'TASKS_URL':'https://admin.s1e1hccnp9dboel2yrosg7q.spin77.games/system/backend_tasks'
        },
        'sp1': {
    'USERNAME': 'Felix',
    'PASSWORD': '777337a5',
    'LOGIN_PAGE_URL': 'https://admin.s98vqr62u9c53vs311734sq.sp1.games/session/new',
    'SESSION_URL': 'https://admin.s98vqr62u9c53vs311734sq.sp1.games/dashboard',
    'REDEMPTION_URL': 'https://admin.s98vqr62u9c53vs311734sq.sp1.games/campaign/redemption_codes/new',
    'MESSAGE_URL': 'https://admin.s98vqr62u9c53vs311734sq.sp1.games/data_report/sms_backflow/query_json',
    'LE_URL': 'https://admin.s98vqr62u9c53vs311734sq.sp1.games/user/layers',
            'FU_URL': 'https://admin.s98vqr62u9c53vs311734sq.sp1.games/data_report/user_funds',
            'TASKS_URL': 'https://admin.s98vqr62u9c53vs311734sq.sp1.games/system/backend_tasks'
    },
    'bx365': {
    'USERNAME': 'hindu',
    'PASSWORD': '2c863a07',
    'LOGIN_PAGE_URL': 'https://admin-sulwxdthyz81v35se82nqvc.bx365.bet/session/new',
    'SESSION_URL': 'https://admin-sulwxdthyz81v35se82nqvc.bx365.bet/dashboard',
    'REDEMPTION_URL': 'https://admin-sulwxdthyz81v35se82nqvc.bx365.bet/campaign/redemption_codes/new',
    'MESSAGE_URL': 'https://admin-sulwxdthyz81v35se82nqvc.bx365.bet/data_report/sms_backflow/query_json',
    'LE_URL': 'https://admin-sulwxdthyz81v35se82nqvc.bx365.bet/user/layers',
    'FU_URL': 'https://admin-sulwxdthyz81v35se82nqvc.bx365.bet/data_report/user_funds',
    'TASKS_URL': 'https://admin-sulwxdthyz81v35se82nqvc.bx365.bet/system/backend_tasks'
    },
    'brplay7': {
    'USERNAME': 'felix',
    'PASSWORD': '1d86be10',
    'LOGIN_PAGE_URL': 'https://admin.spc7pxjvxziax9urv1vx537.brplay7.com/session/new',
    'SESSION_URL': 'https://admin.spc7pxjvxziax9urv1vx537.brplay7.com/dashboard ',
    'REDEMPTION_URL': 'https://admin.spc7pxjvxziax9urv1vx537.brplay7.com/campaign/redemption_codes/new',
    'MESSAGE_URL': 'https://admin.spc7pxjvxziax9urv1vx537.brplay7.com/data_report/sms_backflow/query_json',
    'LE_URL': 'https://admin.spc7pxjvxziax9urv1vx537.brplay7.com/user/layers',
    'FU_URL': 'https://admin.spc7pxjvxziax9urv1vx537.brplay7.com/data_report/user_funds',
    'TASKS_URL': 'https://admin.spc7pxjvxziax9urv1vx537.brplay7.com/system/backend_tasks'
     },
    'brslot': {
    'USERNAME': 'Felix',
    'PASSWORD': '3ff63576',
    'LOGIN_PAGE_URL': 'https://admin-s70webfvq1uq5sbovhxnyos.brslot.games/session/new',
    'SESSION_URL': 'https://admin-s70webfvq1uq5sbovhxnyos.brslot.games/dashboard',
    'REDEMPTION_URL': 'https://admin-s70webfvq1uq5sbovhxnyos.brslot.games/campaign/redemption_codes/new',
    'MESSAGE_URL': 'https://admin-s70webfvq1uq5sbovhxnyos.brslot.games/data_report/sms_backflow/query_json',
    'LE_URL': 'https://admin-s70webfvq1uq5sbovhxnyos.brslot.games/user/layers',
    'FU_URL': 'https://admin-s70webfvq1uq5sbovhxnyos.brslot.games/data_report/user_funds',
    'TASKS_URL': 'https://admin-s70webfvq1uq5sbovhxnyos.brslot.games/system/backend_tasks'
    },
    'gana7': {
    'USERNAME': 'yina',
    'PASSWORD': 'a0753a98',
    'LOGIN_PAGE_URL': 'https://admin.s8wa4opkxsgd80er8cnusns.gana7.mx/session/new',
    'SESSION_URL': 'https://admin.s8wa4opkxsgd80er8cnusns.gana7.mx/dashboard',
    'REDEMPTION_URL': 'https://admin.s8wa4opkxsgd80er8cnusns.gana7.mx/campaign/redemption_codes/new',
    'MESSAGE_URL': 'https://admin.s8wa4opkxsgd80er8cnusns.gana7.mx/data_report/sms_backflow/query_json',
    'LE_URL': 'https://admin.s8wa4opkxsgd80er8cnusns.gana7.mx/user/layers',
    'FU_URL': 'https://admin.s8wa4opkxsgd80er8cnusns.gana7.mx/data_report/user_funds',
    'TASKS_URL': 'https://admin.s8wa4opkxsgd80er8cnusns.gana7.mx/system/backend_tasks'
    },
    '7pg': {
    'USERNAME': 'chu9',
    'PASSWORD': '1e108e09',
    'LOGIN_PAGE_URL': 'https://admin-sc4t56euxk6ohsc8pbuu4ls.7pg.games/session/new',
    'SESSION_URL': 'https://admin-sc4t56euxk6ohsc8pbuu4ls.7pg.games/dashboard',
    'REDEMPTION_URL': 'https://admin-sc4t56euxk6ohsc8pbuu4ls.7pg.games/campaign/redemption_codes/new',
    'MESSAGE_URL': 'https://admin-sc4t56euxk6ohsc8pbuu4ls.7pg.games/data_report/sms_backflow/query_json',
    'LE_URL': 'https://admin-sc4t56euxk6ohsc8pbuu4ls.7pg.games/user/layers',
    'FU_URL': 'https://admin-sc4t56euxk6ohsc8pbuu4ls.7pg.games/data_report/user_funds',
    'TASKS_URL': 'https://admin-sc4t56euxk6ohsc8pbuu4ls.7pg.games/system/backend_tasks'
    },
    'brwins': {
    'USERNAME': 'felix',
    'PASSWORD': '9903011a',
    'LOGIN_PAGE_URL': 'https://admin-ss0xzksnn70lcl159288nxd.brwins.games/session/new',
    'SESSION_URL': 'https://admin-ss0xzksnn70lcl159288nxd.brwins.games/dashboard',
    'REDEMPTION_URL': 'https://admin-ss0xzksnn70lcl159288nxd.brwins.games/campaign/redemption_codes/new',
    'MESSAGE_URL': 'https://admin-ss0xzksnn70lcl159288nxd.brwins.games/data_report/sms_backflow/query_json',
    'LE_URL': 'https://admin-ss0xzksnn70lcl159288nxd.brwins.games/user/layers',
    'FU_URL': 'https://admin-ss0xzksnn70lcl159288nxd.brwins.games/data_report/user_funds',
    'TASKS_URL': 'https://admin-ss0xzksnn70lcl159288nxd.brwins.games/system/backend_tasks'
    },
    'brspin': {
    'USERNAME': 'Felix',
    'PASSWORD': '1fd5036a',
    'LOGIN_PAGE_URL': 'https://admin-sjdyrjrimetp1ltjc8wr5b5.brspin.games/session/new',
    'SESSION_URL': 'https://admin-sjdyrjrimetp1ltjc8wr5b5.brspin.games/dashboard',
    'REDEMPTION_URL': 'https://admin-sjdyrjrimetp1ltjc8wr5b5.brspin.games/campaign/redemption_codes/new',
    'MESSAGE_URL': 'https://admin-sjdyrjrimetp1ltjc8wr5b5.brspin.games/data_report/sms_backflow/query_json',
    'LE_URL': 'https://admin-sjdyrjrimetp1ltjc8wr5b5.brspin.games/user/layers',
    'FU_URL': 'https://admin-sjdyrjrimetp1ltjc8wr5b5.brspin.games/data_report/user_funds',
    'TASKS_URL': 'https://admin-sjdyrjrimetp1ltjc8wr5b5.brspin.games/system/backend_tasks'
    },
    'x7s': {
    'USERNAME': 'Felix',
    'PASSWORD': 'b572c006',
    'LOGIN_PAGE_URL': 'https://admin-skf9yvtdnf0q9xhf0sq0mhq.x7s.games/session/new',
    'SESSION_URL': 'https://admin-skf9yvtdnf0q9xhf0sq0mhq.x7s.games/dashboard',
    'REDEMPTION_URL': 'https://admin-skf9yvtdnf0q9xhf0sq0mhq.x7s.games/campaign/redemption_codes/new',
    'MESSAGE_URL': 'https://admin-skf9yvtdnf0q9xhf0sq0mhq.x7s.games/data_report/sms_backflow/query_json',
    'LE_URL': 'https://admin-skf9yvtdnf0q9xhf0sq0mhq.x7s.games/user/layers',
    'FU_URL': 'https://admin-skf9yvtdnf0q9xhf0sq0mhq.x7s.games/data_report/user_funds',
    'TASKS_URL': 'https://admin-skf9yvtdnf0q9xhf0sq0mhq.x7s.games/system/backend_tasks'
    },
     '7ss': {
    'USERNAME': 'Felix',
    'PASSWORD': 'f595b1fe',
    'LOGIN_PAGE_URL': 'https://admin-sftfee58ivny6siuvsmpkjr.7ss.games/session/new',
    'SESSION_URL': 'https://admin-sftfee58ivny6siuvsmpkjr.7ss.games/dashboard',
    'REDEMPTION_URL': 'https://admin-sftfee58ivny6siuvsmpkjr.7ss.games/campaign/redemption_codes/new',
    'MESSAGE_URL': 'https://admin-sftfee58ivny6siuvsmpkjr.7ss.games/data_report/sms_backflow/query_json',
    'LE_URL': 'https://admin-sftfee58ivny6siuvsmpkjr.7ss.games/user/layers',
    'FU_URL': 'https://admin-sftfee58ivny6siuvsmpkjr.7ss.games/data_report/user_funds',
    'TASKS_URL': 'https://admin-sftfee58ivny6siuvsmpkjr.7ss.games/system/backend_tasks'
    },

     'vana7': {
    'USERNAME': 'Felix',
    'PASSWORD': 'a1900961',
    'LOGIN_PAGE_URL': 'https://admin-sobu3szg9hry7r4wfnmqjn5.vana7.games/session/new',
    'SESSION_URL': 'https://admin-sobu3szg9hry7r4wfnmqjn5.vana7.games/dashboard',
    'REDEMPTION_URL': 'https://admin-sobu3szg9hry7r4wfnmqjn5.vana7.games/campaign/redemption_codes/new',
    'MESSAGE_URL': 'https://admin-sobu3szg9hry7r4wfnmqjn5.vana7.games/data_report/sms_backflow/query_json',
    'LE_URL': 'https://admin-sobu3szg9hry7r4wfnmqjn5.vana7.games/user/layers',
    'FU_URL': 'https://admin-sobu3szg9hry7r4wfnmqjn5.vana7.games/data_report/user_funds',
    'TASKS_URL': 'https://admin-sobu3szg9hry7r4wfnmqjn5.vana7.games/system/backend_tasks'
    },
     '7luck': {
    'USERNAME': 'Felix',
    'PASSWORD': '76a1563b',
    'LOGIN_PAGE_URL': 'https://admin-sw9nfoz72herjoat2ah7hvh.7luck.games/session/new',
    'SESSION_URL': 'https://admin-sw9nfoz72herjoat2ah7hvh.7luck.games/dashboard',
    'REDEMPTION_URL': 'https://admin-sw9nfoz72herjoat2ah7hvh.7luck.games/campaign/redemption_codes/new',
    'MESSAGE_URL': 'https://admin-sw9nfoz72herjoat2ah7hvh.7luck.games/data_report/sms_backflow/query_json',
    'LE_URL': 'https://admin-sw9nfoz72herjoat2ah7hvh.7luck.games/user/layers',
    'FU_URL': 'https://admin-sw9nfoz72herjoat2ah7hvh.7luck.games/data_report/user_funds',
    'TASKS_URL': 'https://admin-sw9nfoz72herjoat2ah7hvh.7luck.games/system/backend_tasks'
    },
      'brlucky': {
    'USERNAME': 'Felix',
    'PASSWORD': '206d068c',
    'LOGIN_PAGE_URL': 'https://admin-sh2vr4y7lt0n9vdg4su9fpv.brlucky.game/session/new',
    'SESSION_URL': 'https:/admin-sh2vr4y7lt0n9vdg4su9fpv.brlucky.game/dashboard',
    'REDEMPTION_URL': 'https://admin-sh2vr4y7lt0n9vdg4su9fpv.brlucky.game/campaign/redemption_codes/new',
    'MESSAGE_URL': 'https://admin-sh2vr4y7lt0n9vdg4su9fpv.brlucky.game/data_report/sms_backflow/query_json',
    'LE_URL': 'https://admin-sh2vr4y7lt0n9vdg4su9fpv.brlucky.game/user/layers',
    'FU_URL': 'https://admin-sh2vr4y7lt0n9vdg4su9fpv.brlucky.game/data_report/user_funds',
    'TASKS_URL': 'https://admin-sh2vr4y7lt0n9vdg4su9fpv.brlucky.game/system/backend_tasks'
    },
      '7xx': {
    'USERNAME': 'Felix',
    'PASSWORD': 'ef0404ce',
    'LOGIN_PAGE_URL': 'https://admin-spm7a6q2lf5auu2tfuqeplk.7xx.game/session/new',
    'SESSION_URL': 'https://admin-spm7a6q2lf5auu2tfuqeplk.7xx.game/dashboard',
    'REDEMPTION_URL': 'https://admin-spm7a6q2lf5auu2tfuqeplk.7xx.game/campaign/redemption_codes/new',
    'MESSAGE_URL': 'https://admin-spm7a6q2lf5auu2tfuqeplk.7xx.game/data_report/sms_backflow/query_json',
    'LE_URL': 'https://admin-spm7a6q2lf5auu2tfuqeplk.7xx.game/user/layers',
    'FU_URL': 'https://admin-spm7a6q2lf5auu2tfuqeplk.7xx.game/data_report/user_funds',
    'TASKS_URL': 'https://admin-spm7a6q2lf5auu2tfuqeplk.7xx.game/system/backend_tasks'
    },
     '7aa': {
    'USERNAME': 'Felix',
    'PASSWORD': '801823a4',
    'LOGIN_PAGE_URL': 'https://admin-swqml695wjf5wu6vl57qjr6.7aa.game/session/new',
    'SESSION_URL': 'https://admin-swqml695wjf5wu6vl57qjr6.7aa.game/dashboard',
    'REDEMPTION_URL': 'https://admin-swqml695wjf5wu6vl57qjr6.7aa.game/campaign/redemption_codes/new',
    'MESSAGE_URL': 'https://admin-swqml695wjf5wu6vl57qjr6.7aa.game/data_report/sms_backflow/query_json',
    'LE_URL': 'https://admin-swqml695wjf5wu6vl57qjr6.7aa.game/user/layers',
    'FU_URL': 'https://admin-swqml695wjf5wu6vl57qjr6.7aa.game/data_report/user_funds',
    'TASKS_URL': 'https://admin-swqml695wjf5wu6vl57qjr6.7aa.game/system/backend_tasks'
    }

   
}


def get_platfrom_config(platfrom_name):
    return PLATFROM_CONFIGS.get(platfrom_name)


def get_platfrom_cookies(platfrom_name):
    """从 JSON文件读取平台 Cookie"""
    cookies_file = f"C:/Users/wsmian/Desktop/用户资金-流失/用户资金-流失/session/cookies_{platfrom_name}.json"
    if not os.path.exists(cookies_file):
        return None
    
    try:
        with open(cookies_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return None