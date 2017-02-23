import requests, json

# Get the DBLP's url for faculty's publications
def get_url(faculty):
    # Get the current faculty name
    full_name = faculty.split()

    # Get the url
    prefix = "http://dblp.uni-trier.de/search/publ/api?callback=&q=author%3A"
    surname = full_name[1]
    name = full_name[0]
    suffix = "%3A&compl=venue&p=2&h=0&c=1000&format=json"

    url = prefix + name + '_' + surname + suffix
    return url, name, surname

# Conference lists
conferences = {
    'STOC':0,
    'FOCS':0,

    'ITCS':0,
    'ICS':0,
    'SODA':0,
    'IEEE_Conference_on_Computational_Complexity':0,
    'Conference_on_Computational_Complexity':0,
    'Structure_in_Complexity_Theory_Conference':0,
    'ICALP':0,

    'WINE':0,
    'ESA':0,

    'CRYPTO':0,
    'EUROCRYPT':0,
    'ASIACRYPT':0,
    'IEEE_Symposium_on_Security_and_Privacy':0,
    'TCC':0,

    'EC':0,

    'LICS':0,

    'PODC':0,
    'SPAA':0,

    'ICML':0,
    'NIPS':0,
    'COLT':0,
    'IJCAI':0,
    'AAAI':0,

    'IEEE_Trans._Information_Theory':0,
    'ISIT':0,

    'Quantum_Information_&_Computation':0,

    'SIAM_J._Comput.':0,
    'J._Comput._Syst._Sci.':0,
    'J._ACM':0
}

# Get the faculty list
faculty_list_file = open('other_list', 'r')
faculty_list = faculty_list_file.readlines()

faculty_stat_file = open('other_faculty_stat.csv', 'w')

print('DBLP_Name, STOC, FOCS, ITCS, SODA, CCC, ICALP, '\
      'CRYPTO, EURO, ASIA, EC, LICS, PODC, SPAA, '\
      'ICML, NIPS, COLT, ISIT')

for faculty in faculty_list:
    # Clean up conferences statistic
    for conf in conferences:
        conferences[conf] = 0

    # Get the url and data
    faculty_name = faculty[:-1]
    url, name, surname = get_url(faculty_name)
    stats = requests.get(url).json()
    hits = stats['result']['hits']['@total']

    while hits == '0':
        print("\n\nName Error:", name, surname)
        faculty_name = input("Please input the corrected name: ")

        # Get the url and data
        url, name, surname = get_url(faculty_name)
        stats = requests.get(url).json()
        hits = stats['result']['hits']['@total']

    pub_list = stats['result']['completions']['c']
    length = len(pub_list)

    print("\n\n{}".format(faculty_name))
    for idx in range(length):
        type = pub_list[idx]['text'][13:]
        cnt = pub_list[idx]['@sc']
        print(type, " ", cnt)

        if type in conferences:
            conferences[type] += int(cnt)

        result = faculty_name
        result += ', ' + str(conferences['STOC'])
        result += ', ' + str(conferences['FOCS'])
        result += ', ' + str(conferences['ITCS']+conferences['ICS'])
        result += ', ' + str(conferences['SODA'])
        result += ', ' + str(conferences['IEEE_Conference_on_Computational_Complexity'] + \
                             conferences['Conference_on_Computational_Complexity'] + \
                             conferences['Structure_in_Complexity_Theory_Conference'])
        result += ', ' + str(conferences['ICALP'])
        result += ', ' + str(conferences['CRYPTO'])
        result += ', ' + str(conferences['EUROCRYPT'])
        result += ', ' + str(conferences['ASIACRYPT'])
        result += ', ' + str(conferences['EC'])
        result += ', ' + str(conferences['LICS'])
        result += ', ' + str(conferences['PODC'])
        result += ', ' + str(conferences['SPAA'])
        result += ', ' + str(conferences['ICML'])
        result += ', ' + str(conferences['NIPS'])
        result += ', ' + str(conferences['COLT'])
        result += ', ' + str(conferences['ISIT'])

    # Output the stat
    print(result, file=faculty_stat_file)
    faculty_stat_file.flush()

faculty_stat_file.close()
