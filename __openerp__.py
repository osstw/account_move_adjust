# -*- coding: utf-8 -*-
{
    "name": "account move adjust",
    "author":"糖葫芦(39181819@qq.com)",
    "depends": ["account"],
    "data": ["views/account_move_view.xml",
             "wizard/account_move_auto_adjust_wizard.xml"],
    "description": """
    给分录增加四舍五入功能

    2016-2-19 更新

    1、对已经post的分录自动先取消post，再进行四舍五入操作，然后再重新post。

    2、加入新功能：对批量选中的分录，一次性自动完成四舍五入操作。

    3、account.move 加入新字段：is_adjusted，用以标识分录是否被四舍五入操作过。并且在search view里加入两个filter。
    """
}
