from type_convert import *

NODE_HEADER = """*NODE    ; Nodes
; iNO, X, Y, Z\n"""

ELEMENT_HEADER = """*ELEMENT    ; Elements
; iEL, TYPE, iMAT, iPRO, iN1, iN2, ANGLE, iSUB,                     ; Frame  Element
; iEL, TYPE, iMAT, iPRO, iN1, iN2, ANGLE, iSUB, EXVAL, EXVAL2, bLMT ; Comp/Tens Truss
; iEL, TYPE, iMAT, iPRO, iN1, iN2, iN3, iN4, iSUB, iWID , LCAXIS    ; Planar Element
; iEL, TYPE, iMAT, iPRO, iN1, iN2, iN3, iN4, iN5, iN6, iN7, iN8     ; Solid  Element\n"""

wincad = client.Dispatch("ZWCAD.Application")  # 链接cad，这里是调用目前打开的cad
doc = wincad.ActiveDocument  # doc表示当前活跃的Document
mp = doc.ModelSpace  # mp表示模


def get_selected_elements():
    try:
        doc.SelectionSets.Item("SS1").Delete()
    except:
        print("Delete selection failed")

    elements = list()
    slt = doc.SelectionSets.Add("SS1")
    print("请在屏幕拾取图元，以Enter键结束")
    slt.SelectOnScreen()

    basic_point = None
    for selected in slt:
        # todo有多个基准点时报错
        if selected.EntityName == 'AcDbPoint':
            basic_point = selected.Coordinates
            continue
        elements.append([selected.StartPoint, selected.EndPoint])

    return basic_point, elements


def points_converter(elements, basic_point, midas_basic_point, proportion):
    if proportion != 1:
        elements = [[[_ / proportion for _ in p] for p in element] for element in elements]
        basic_point = [_ / proportion for _ in basic_point]
    delta = [basic_point[0] - midas_basic_point[0],
             basic_point[1] - midas_basic_point[1],
             basic_point[2] - midas_basic_point[2]]

    ret = list()
    for element in elements:
        start = (element[0][0] - delta[0],
                 element[0][1] - delta[1],
                 element[0][2] - delta[2])
        end = (element[1][0] - delta[0],
               element[1][1] - delta[1],
               element[1][2] - delta[2])
        ret.append([start, end])
    return ret


def generate_mgt_file(elements, drawBeam=True):
    points = dict()
    i = 999999
    for element in elements:
        for p in element:
            if p not in points:
                points[p] = i
                i -= 1

    f = open("./tmp.txt", 'w')
    f.write(NODE_HEADER)
    for key, value in points.items():
        f.write(f'{value}, {key[0]}, {key[1]}, {key[2]}\n')

    if not drawBeam:
        f.close()
        return

    i = 999999
    f.write(ELEMENT_HEADER)

    for element in elements:
        start, end = element
        start = points[start]
        end = points[end]
        f.write(f"{i}, BEAM, 999, 999, {start}, {end}, 0, 0\n")
        i -= 1
    f.close()


if __name__ == '__main__':
    basic_point, elements = get_selected_elements()
    if basic_point is None:
        print("请先输入基准点！")
        exit()
    print(len(elements))

    # proportion = int(input("请输入midas和cad的单位长度比例："))
    # midas_basic_point = input("请输入基准点在midas中的坐标值，用空格分割：")
    # midas_basic_point = [float(_) for _ in midas_basic_point.split(' ')]
    midas_basic_point = [21.5, 5.0, 0.0]
    proportion = 1

    elements = points_converter(elements, basic_point, midas_basic_point, proportion)
    generate_mgt_file(elements)
