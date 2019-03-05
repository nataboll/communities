import json
import requests

def logger(func):
    def wrapped(*args, **kwargs):
        result = func(*args, **kwargs)
        with open('log.txt', 'w') as f:
            f.write(json.dumps(result))
        return result
    return wrapped

@logger
def get_graph():
    return requests.get("https://raw.githubusercontent.com/plotly/datasets/master/miserables.json").json()

def write_data(filename):
        with open(filename, 'w') as f:
            f.seek(0)
            f.write('1\n')
            f.write(str(N)+' '+str(L)+'\n')
            for item in Edges:
                f.write(str(item[0])+' '+str(item[1])+' '+str(item[2])+'\n')

if __name__ == "__main__":
    data = get_graph()
    N = len(data['nodes'])
    L = len(data['links'])
    Edges = [(data['links'][k]['source'], data['links'][k]['target'], data['links'][k]['value']) for k in range(L)]
    write_data("input.txt")
