from openstaad import Geometry, Root, Output, Load

def instance_exist():
    try:
        filename = Root().GetSTAADFile()
        if filename: return True
        else: return False
    except:
        return False


def get_selected_members():
    if not instance_exist(): return []
    return list(Geometry().GetSelectedBeams())


def get_selected_nodes():
    if not instance_exist(): return []
    return list(Geometry().GetSelectedNodes())

#test if main
if __name__ == '__main__':
    print(instance_exist())
    print(get_selected_members())
    print(get_selected_nodes())