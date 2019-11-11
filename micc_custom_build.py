from pathlib import Path
#if there is a custom build step the wheel tags are specific.

def build(setup_kwargs):
    
    print('hello')
    for k,v in setup_kwargs.items():
        print(k,':',v)
    d = Path.cwd() / 'micc'
    glob = d.glob('*')
    for v in glob:
        print(v)
#     raise Exception(f"cwd = {Path.cwd()}\n{glob}") 
    return 0