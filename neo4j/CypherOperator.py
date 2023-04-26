from neo4j import GraphDatabase


class Node:
    def __init__(self, type, data):
        self.type = type
        self.data = data


def SQLWhere(filter, node):
    res = ""
    for k, v in filter.items():
        res += " and " if res != "" else ""
        res += f"{node}.{k} = '{v}'"
    return res


def unpack(pack, separator=":", connector=", "):
    """
    字典解包来配合query语句

    Args:
        pack (dict):        要解包的字典
        separator (str):     key和value之间的分割符
        connector (str):      每组key和value之间的连接符
    """
    res = ""
    for k, v in pack.items():
        res += connector if res != "" else ""
        if v.isdigit():
            res += f"{k} {separator} {v}"
        else:
            res += f"{k} {separator} '{v}'"
    return res


def connect(uri, user, passwd):
    return GraphDatabase.driver(
        uri,
        auth=(user, passwd)
    )


def operate(driver, command):
    """直接用命令操作"""
    # with open("./neo4j/CypherOperator.log", "a") as f:
    #     f.write("operate: " + command + "\n")
    print("operate: ", command)
    with driver.session() as session:
        result = session.run(command)
        return [record for record in result]


def query(driver, type, filter={}):
    """
    查询节点

    Args:
        driver:     driver
        filter:     dict

    Return:
        result:     string
    """
    command = f"match (p:{type} {{ {unpack(filter)} }}) return p"

    return operate(driver, command)


def create_node(driver, type, data={}):
    """
    创建节点, 无论是否有相同节点存在

    Args:
        driver: driver
        type:   string
        data:   dict
    """
    command = f"create (:{type} {{ {unpack(data)} }})"

    return operate(driver, command)


def add_node(driver, node):
    """
    如果没有相同节点存在, 则创建节点

    Args:
        driver: driver
        type:   string
        data:   dict
    """
    command = f"merge (:{node.type} {{ {unpack(node.data)} }})"

    return operate(driver, command)


def set_node(driver, filter={}, newdata={}):
    """
    修改节点

    Args:
        driver:     driver
        filter:     dict
        newdata:    dict
    """
    command = f"match (p:Person {{ {unpack(filter)} }}) set {unpack(newdata, '=')} RETURN p"

    return operate(driver, command)


def del_node(driver, filter):
    pass


def add_edge(driver, node1, node2, relation):
    """
    添加一条从节点1到节点2的边

    Args:
        node1 (Node):        节点1
        node2 (Node):        节点2
        relation (str):     节点的关系名

    """
    query = f"match (a:{node1.type}) with a match (b:{node2.type}) where {SQLWhere(node1.data, 'a')} and {SQLWhere(node2.data, 'b')} merge (a) -[:{relation}]-> (b)"
    operate(driver, query)


def add_edges(driver, node1, nodes, relation):
    """
    从node1到nodes中的每个点都加一条边
    Node类型: 包含节点的信息, 包含两个key
        type (str):     节点类型
        data (dict):    节点属性

    Args:
        node1 (Node):   节点1信息
        nodes (Node[]): 节点1指向的点的信息
        relation (str): 节点的关系名
    """
    for node2 in nodes:
        add_edge(driver, node1, node2, relation)
