from myapp.models import *


def get_currency_list():
    currency_list = list()
    import requests
    from bs4 import BeautifulSoup
    url = "https://thefactfile.org/countries-currencies-symbols/"
    response = requests.get(url)
    if not response.status_code == 200:
        return currency_list
    soup = BeautifulSoup(response.content)
    data_lines = soup.find_all('tr')
    for line in data_lines:
        try:
            detail = line.find_all('td')
            currency = detail[2].get_text().strip()
            iso = detail[3].get_text().strip()
            if (currency, iso) in currency_list:
                continue
            currency_list.append((currency, iso))
        except:
            continue
    return currency_list


def add_currencies(currency_list):
    for currency in currency_list:
        currency_name = currency[0]
        currency_symbol = currency[1]
        try:
            c = Currency.objects.get(iso=currency_symbol)
        except:
            c = Currency(long_name=currency_name, iso=currency_symbol)
        c.name = currency_name
        # c.save() #To test out the code, replace this by print(c)
        print(c)
    return


# from django.http import HttpResponseRedirect
# from django.urls import reverse


# def maintenance(request):
#     data = dict()
#     try:
#         choice = request.GET['selection']
#         if choice == "currencies":
#             support_functions.add_currencies(support_functions.get_currency_list())
#             c_list = Currency.objects.all()
#             print("Got c_list", len(c_list))
#             data['currencies'] = c_list
#             return HttpResponseRedirect(reverse('currencies'))
#     except:
#         pass
#     return render(request, "maintenance.html", context=data)
