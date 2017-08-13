import requests
import os
def get_url(i):
    url = 'http://cs231n.stanford.edu/slides/2017/cs231n_2017_lecture{}.pdf'.format(i)
    return url
for i in range(1,17):
    response = requests.get(get_url(i))
    content = response.content
    file_path = '{0}/{1}.{2}'.format(os.getcwd(),'cs231n_2017_lecture{}'.format(i),'pdf')
    if not os.path.exists(file_path):
        with open(file_path, 'wb') as f:
            f.write(content)
            f.close()
print('Download finished')
