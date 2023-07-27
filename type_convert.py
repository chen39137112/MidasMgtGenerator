from win32com import client
import pythoncom


# 变量类型转换
def vtPnt(x, y, z=0):
    """坐标点转化为浮点数"""
    return client.VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, (x, y, z))


def vtObj(obj):
    """转化为对象数组"""
    return client.VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_DISPATCH, obj)


def vtFloat(list):
    """列表转化为浮点数"""
    return client.VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, list)


def vtInt(list):
    """列表转化为整数"""
    return client.VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_I2, list)


def vtVariant(list):
    """列表转化为变体"""
    return client.VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_VARIANT, list)
