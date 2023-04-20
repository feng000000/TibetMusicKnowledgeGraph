ch_nums = ['一', '二', '三', '四', '五', '六', '七', '八', '九', '十', '零', '百', '千', '万']

for i in ch_nums:
    print(i.encode("unicode_escape"))

print('\u4e05')