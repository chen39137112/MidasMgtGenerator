import sys
from utils import NODE_HEADER, ELASTIC_LINK_HEADER

def check_points(fd):
    # midas支持的最大节点数量
    points = [[None, None, None] for _ in range(1000000)]
    text = fd.readline()

    while text != '\n':
        if text[0] == ';':
            text = fd.readline()
            continue
        point_info = text.strip().split(',')
        points[int(point_info[0])] = point_info[1:]
        text = fd.readline()

    return points


def get_scaffolds_up_points(fd, mat, pro, points):
    up_points = []
    text = fd.readline()
    while text != '\n':
        if text[0] == ';':
            text = fd.readline()
            continue
        ele_info = text.strip().split(',')

        # 比较材料号和截面号
        if ele_info[2].strip() == mat and ele_info[3].strip() == pro:
            p1 = int(ele_info[4])
            p2 = int(ele_info[5])
            try:
                up_points.append(p1 if int(points[p1][2]) > int(points[p2][2]) else p2)
            except Exception as e:
                print(f"单元中存在未定义的节点号{p1}、{p2}")
                sys.exit()

        text = fd.readline()

    return up_points


def get_params():
    if len(sys.argv) != 5:
        print("e.g.: python AddElasyicLink.py mgt文件名 材料号 截面号 距离")
        return
    return sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]


def write_mgt_file(up_points, points, distance):
    distance = int(distance)
    p_id = 1
    targets = [0 for _ in range(len(up_points))]

    for i, p in enumerate(up_points):
        while points[p_id][0] != None:
            p_id += 1
        targets[i] = p_id
        p_id += 1


    f = open("./result.txt", 'w')
    f.write(NODE_HEADER)
    for t_id, point in zip(targets, up_points):
        f.write(f'{t_id}, {points[point][0]}, {points[point][1]}, {int(points[point][2]) + distance}\n')


    f.write(ELASTIC_LINK_HEADER)
    i = 1
    for t_id, point in zip(targets,up_points):
        # todo 刚度可指定
        f.write(f'{i}, {point}, {t_id}, COMP, 0, 1000, NO, 0.5, 0.5,\n')
        i += 1


def add_elastic_links():
    try:
        mgt_name, material, section, distance = get_params()
    except:
        return

    # 调试用
    # mgt_name, material, section, distance = 'model', '2', '5', '120'
    if not mgt_name.endswith('.mgt'):
        mgt_name += '.mgt'
    fd = open(f'./{mgt_name}')

    text = fd.readline()
    while text:
        if text.startswith('*NODE'):
            points = check_points(fd)
        elif text.startswith('*ELEMENT'):
            up_points = get_scaffolds_up_points(fd, material, section, points)
            break
        text = fd.readline()

    fd.close()
    write_mgt_file(up_points, points, distance)



if __name__ == '__main__':
    add_elastic_links()
