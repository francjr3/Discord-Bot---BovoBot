# data_format.py
# 
# Author: Francisco Rodriguez Santana
# 
# Date: 12/14/2021
#
# Description:
# Formats discord bot information in a presentable manner.
#

def formatList(header=str, list_data=list):
    form_str = header + "\n"
    form_str += "=" * 30 + "\n"
    list_form = [f"-{list_data[i]:<14} -{list_data[i+1]}" if i != len(list_data)-1 else f"-{list_data[i]:<14} " for i in range(0, len(list_data), 2)]
    list_form = "\n".join(list_form)
    form_str += list_form + "\n"
    form_str += "=" * 30 + "\n"
    return form_str
