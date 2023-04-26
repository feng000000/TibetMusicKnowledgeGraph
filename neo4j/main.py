from CypherOperator import *

# localhost
driver = connect("bolt://localhost:7687", "neo4j", "neo4j@Feng0@@")

# neo4j aura
# driver = connect(
#     "neo4j+s://55157283.databases.neo4j.io",
#     "neo4j",
#     "uNR4GQVbKgi9JaNWFIqm1T1sqN59nvVoaCxT61ySj9o"
# )

TibetMusic      = Node("一级类别", {'name': "西藏民族音乐"})

# 西藏民族音乐
FolkMusic       = Node("二级类别", {'name': "民间音乐"})
TibetDrama      = Node("二级类别", {'name': "藏戏音乐"})
PalaceMusic     = Node("二级类别", {'name': "宫廷音乐"})
ReligiousMusic  = Node("二级类别", {'name': "宗教音乐"})

# 民间音乐
FolkDance       = Node("三级类别", {'name': "民间歌舞类"})
FolkSong        = Node("三级类别", {'name': "民歌类"}  )
LaborSong       = Node("三级类别", {'name': "劳动歌曲类"})
RapSong         = Node("三级类别", {'name': "说唱音乐类"})



add_node(driver, TibetMusic     )

add_node(driver, FolkMusic      )
add_node(driver, TibetDrama)
add_node(driver, PalaceMusic    )
add_node(driver, ReligiousMusic )

add_node(driver, FolkDance      )
add_node(driver, FolkSong       )
add_node(driver, LaborSong      )
add_node(driver, RapSong        )

add_edges(driver, TibetMusic, [
        FolkMusic      ,
        TibetDrama,
        PalaceMusic    ,
        ReligiousMusic      ,
], "Subset")

add_edges(driver, FolkMusic, [
        FolkDance   ,
        FolkSong    ,
        LaborSong   ,
        RapSong     ,
], "Subset")


# 歌曲歌手
with open("data/csv/Song.csv", "r") as f:
    temp = f.readline()
    data = f.readlines()

for item in data:
    line = item.strip().split(',')
    singerNode = Node("歌手", {'name': line[0], '演唱歌曲': line[1]})
    songNode = Node("歌曲", {'name':line[1]})
    songTypeNpde = Node("四级类别", {'name': line[2]})
    add_node(driver, singerNode)
    add_node(driver, songNode)
    add_node(driver, songTypeNpde)
    add_edge(driver, songNode, singerNode, "演唱者")
    add_edge(driver, songTypeNpde, songNode, "entity")
    add_edge(driver, FolkSong, songTypeNpde, "Subset")


# 舞蹈
with open("data/csv/TibetDance.csv", "r") as f:
    temp = f.readline()
    data = f.readlines()

for item in data:
    line = item.strip().split(',')

    danceNode = Node("舞蹈", data = {
        "name": line[3],
        "非遗网站项目编号": line[2],
        "类别": line[4],
        "申报地区或单位": line[7],
    })
    danceTypeName = line[3].split('(')[0].strip()
    faNode = Node("四级类别", {'name': danceTypeName})

    add_node(driver, danceNode)
    add_node(driver, faNode)
    add_edge(driver, FolkDance, faNode, "Subset")
    add_edge(driver, faNode, danceNode, "Subset")

# 传承人
with open("data/csv/Successor.csv", "r") as f:
    temp = f.readline()
    data = f.readlines()

for item in data:
    line = item.strip().split(',')
    peopleName = line[1].strip()
    peopleSex = line[2].strip()
    danceName = line[6].strip()
    danceNum = line[5].strip()
    danceArea = line[7].strip()
    peopleNode = Node("传承人", {'name': peopleName, 'sex': peopleSex})
    danceNode = Node("舞蹈", {'name': danceName, '非遗网站项目编号': danceNum, '申报地区或单位': danceArea})
    add_node(driver, peopleNode)
    add_node(driver, danceNode)
    add_edge(driver, danceNode, peopleNode, "传承人")


# 藏戏
with open("data/csv/TibetDrama.csv", "r") as f:
    temp = f.readline()
    data = f.readlines()

for item in data:
    line = item.strip().split(',')
    fullName = line[3].strip()
    type = line[4].strip()
    area = line[7].strip()
    if '(' in line[3]:
        className = line[3].split('(')[1].split(')')[0]
    else:
        className = line[3]
    dramaNode = Node('戏曲', {'name': fullName, '类别': type, '申报地区或单位': area})
    classNode = Node('三级类别', {'name': className})
    add_node(driver, dramaNode)
    add_node(driver, classNode)
    add_edge(driver, TibetDrama, classNode, "Subset")
    add_edge(driver, classNode, dramaNode, "entity")