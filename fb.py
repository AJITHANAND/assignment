import os
import facebook,json,requests
import  pandas as pd

class Facebook:
    def __init__(self):
        self.__access_token = os.getenv('facebook_token')
        self.graph = facebook.GraphAPI(self.__access_token)
        self.url = 'http://graph.facebook.com/v15.0/me/posts?fields=reactions.summary(total_count).type(LIKE),comments.summary(total_count)&access_token=%s' % self.__access_token
    def get_posts_data(self):
        res = requests.get(self.url)
        # print(res.status_code)
        # return None
        return res.json() if res.status_code==200 else None
    def cleanup(self,data):
        new_dict = {}
        count = 0
        for d in data['data']:
            new_dict[count] = {}
            new_dict[count]['id'] = d['id']
            new_dict[count]['likes'] = d['reactions']['summary']['total_count']
            new_dict[count]['comments'] = d['comments']['summary']['total_count']
            count+=1
        return new_dict
    def gen_DataFrame(self,data):
        df = pd.DataFrame.from_dict(data,orient='index')
        df.columns = ['id','likes','comments']
        return df
def main():
    fb = Facebook()
    data = fb.get_posts_data()
    if data is None:
        print('No data')
        exit(1)
    data = fb.cleanup(data)
    df = fb.gen_DataFrame(data)
    print(df)
    

if __name__ == '__main__':
    main()