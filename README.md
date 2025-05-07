# tables-agent
`scp -i ~/.ssh/droplet -r ./* root@207.154.206.41:~/notion-agent/`
`docker run -p 8000:8000 -e OPENAI_API_KEY=<Key> -e NOTION_KEY=<Key> notion-agent`


from dotenv import load_dotenv
from openai import OpenAI
from schemas import People, SimilarNames
load_dotenv('.env')


client = OpenAI()
titles = ['Aviv', 'Ari ', 'Ella Amit', 'Hani Tirnover', 'Meni Tirnover', 'Doron Lazar', 'Or Eitan', 'Doron (Dudi)', 'Aliza Ments', 'Aharon Ments', 'Lidar Cohen', 'Tamir Yungman', 'Noam Goldberg', 'Bar Amsalem', 'Shahar Shafir', 'Reut', 'Yoav Yatskan', 'Gilad Shenar', 'Dvir (Lior Minay)', 'Elon Landman', 'Zohar Halkon', 'Orel Boutbul', 'Shimon', 'Dafi Hachmov', 'Boaz Hachmov', 'Ariel Gabbay', 'Naama Roth', 'Nitzan Kenig', 'Yoav Unger', 'Yonatan Unger ', 'Hadas Focus ', 'Hadas tamar', 'Talya Clymer', 'Achinoam Sharf', 'Shoval Cohen', 'Inbar Fried', 'Idan Basre', 'Viki Yoffe', 'Avi Nae', 'Michal (Gilad)', 'Gilad Yakovian', 'Ofir Yakovian', 'Ruti', 'Shimi', 'Iris', 'Ariel', 'Yaniv', 'Merav', 'Aharon Lichtenstain', 'Orna Lichtenstain', 'Chai’s Father', 'Meri (Chai’s Mother)', 'Inbar', 'Gal (Lilach)', 'Lilach', 'Yonatan', 'David', 'Rina Pinchover', 'Benny Fellman', 'Sara Goldstein', 'Inbar Avni', 'Shay Abargil', 'Boaz Wiesner', 'Gefen Wiesner', 'Lior Rubin', 'Ilan “Lani” Rubin', 'Michal Rubin', 'Lior Minay', 'Yardena (Ella’s mom)', 'Adi Gvitzman', 'Sharon’s Guy', 'Sharon', 'Erez Gvitzman', 'Pnina Gvitzman', 'Shemuel', 'Carmela', 'Liran', 'Eran', 'Rani Kaufman', 'Tal Ben Naeh', 'Aviad Tal', 'Dani Meltz', 'Noa Aggasi', 'Noa Nissan', 'Avigial (Shay’s)', 'Adi Malka', 'Joseph', 'Itay Livneh', 'Roey Livneh', 'Idan Livneh', 'Ella Lazar', 'Avi Elyatim', 'Annet Mustaki', 'Zecharia Mustaki', 'Chai Ben Simon', 'Dudi', 'Liat Mustaki', 'Shlomo Mustaki', 'Ora Mustaki', 'Yehudit Bas', 'Nirit Kaufman', 'Matanya', 'Nili Kaufman', 'Yahali Kaufman', 'Bar Kaufman', 'Anny Kaufman', 'Aviad Kaufman', 'Ron', 'Gil Kaufman', 'Shay Kaufman', 'Idit Kaufman', 'Amiram Kaufman', 'Tomer Gerbi', 'Shira Orbach', 'Orpaz’s Tomer (cant come)', 'Orpaz (cant come)', 'Barak Ben Khalifa', 'Kfir Krakauer', 'Maya Rubin', 'Liad Rubin', 'Talia Krakauer Rubin', 'Ofira Krakauer', 'Eli Krakauer', 'Nitzan Ben Meir Maman', 'Mordi Maman', 'Dian Pollak', 'Ella Wiener', 'Doron Pollak', 'Oshra Pollak', 'Yossi Pollak', 'Yeala Krakauer Pollak', 'Daniel Pollak']
name = 'ענבר אבני'

response = client.responses.create(
    model="gpt-4.1-nano",
    input=[
        {
            "role": "user",
            "content": f"""
            hey, find all similar names in structure to '{name}' from the following list:
            '{titles}'
            Return names only from the given list!!!
            """,
        }
    ],
)

response = client.responses.parse(
    model="gpt-4.1-nano",
    input=[
        {
            "role": "user",
            "content": response.output_text,
        }
    ],
    text_format=SimilarNames
)
response