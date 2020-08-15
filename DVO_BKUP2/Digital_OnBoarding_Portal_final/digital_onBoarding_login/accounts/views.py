from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import OrderForm, CreatingMyUserForm
from django.contrib import messages
import json


# selected_id = ''


def registerPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = CreatingMyUserForm()
        if request.method == 'POST':
            form = CreatingMyUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Account was created for ' + user)

                return redirect('login')

        context = {'form': form}
        return render(request, 'accounts/register.html', context)


def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('home')
            else:

                messages.warning(request, 'Username OR password is incorrect')

        context = {}
        return render(request, 'accounts/login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def home(request):
    def getJSON(filePathAndName):
        with open(filePathAndName, 'r') as fp:
            return json.load(fp)

    products_data = getJSON('./data.json')

    # api stuff
    # products = []
    # api_token = "0cc4ebe9-3f7e-4766-9b14-6b49385b53d3"
    # api_endpoint = "http://196.216.224.167:8080/handler/api/all-products"
    # headers = {'Authorization': 'Bearer' + api_token,
    #            'Content-Type': 'application/json; charset=utf-8',
    #            }
    # api_data = requests.get(api_endpoint, headers=headers)
    # json_data = json.loads(api_data.text)
    #
    # for i in range(0, len(json_data) - 1):
    #     products.append(
    #         {
    #             'product_name': json_data[i]['productName'],
    #             'short_description': json_data[i]['productName']
    #         }
    #     )

    #
    # orders = Order.objects.all()
    # customers = Customer.objects.all()
    #
    # total_customers = customers.count()
    #
    # total_orders = orders.count()
    # delivered = orders.filter(status='Delivered').count()
    # pending = orders.filter(status='Pending').count()

    # context = {'orders': orders, 'customers': customers,
    #            'total_orders': total_orders, 'delivered': delivered,
    #            'pending': pending
    #            }
    total_products = len(products_data)
    products = []
    for i in range(0, 5):
        products.append(
            {
                'productName': products_data[i]['productName'],
                'applicableCurrencies': products_data[i]['applicableCurrencies']
            }
        )

    context = {'products': products, 'total_products': total_products}

    return render(request, 'accounts/dashboard.html', context)


@login_required(login_url='login')
def products_view(request):
    def getJSON(filePathAndName):
        with open(filePathAndName, 'r') as fp:
            return json.load(fp)

    products_json = getJSON('./data.json')
    context = {'products_json': products_json}

    return render(request, 'accounts/products.html', context)


@login_required(login_url='login')
def product_view(request, id):
    context = {'id': id}

    def getJSON(filePathAndName):
        with open(filePathAndName, 'r') as fp:
            return json.load(fp)

    products = []
    products_details = []
    products_image = []
    products_Terms = []
    products_Conditions = []
    products_full_Description = []
    products_MinimumRequirements = []
    products_Code = []
    products_applicable_Currencies = []
    product_shortdescription = []
    wanted_product = id
    selected_id = id

    products_data = getJSON('./data.json')

    for i in range(0, len(products_data) - 1):
        if products_data[i]['id'] == selected_id:
            products.append(
                {

                    products_data[i]['id'],

                }

            )
            products_details.append(
                {

                    products_data[i]['productName'],
                })

            product_shortdescription.append({

                products_data[i]['shortDescription'],
            }
            )
            products_image.append({

                products_data[i]['imageUrl'],
            }
            )
            products_Terms.append({

                products_data[i]['productTerms'],
            }
            )
            products_Conditions.append({

                products_data[i]['productConditions'],
            }
            )

            products_full_Description.append({

                products_data[i]['fullDescription'],
            }
            )

            products_MinimumRequirements.append({

                products_data[i]['productMinimumRequirements'],
            }
            )

            products_Code.append({

                products_data[i]['productCode'],
            }
            )

            products_applicable_Currencies.append({

                'applicable_Currencies': products_data[i]['applicableCurrencies'],
            }
            )

            if wanted_product in products[len(products) - 1]:
                print('found')

                def convert_list_to_string(org_list, seperator=' '):
                    return seperator.join(org_list)

                full_str = convert_list_to_string(products_image[0])
                product_name = convert_list_to_string(products_details[0])
                shortdescription = convert_list_to_string(product_shortdescription[0])
                products_Terms = convert_list_to_string(products_Terms[0])
                products_Conditions = convert_list_to_string(products_Conditions[0])
                products_full_Description = convert_list_to_string(products_full_Description[0])
                products_MinimumRequirements = convert_list_to_string(products_MinimumRequirements[0])
                products_Code = convert_list_to_string(products_Code[0])
                products_applicable_Currencies = convert_list_to_string(products_applicable_Currencies[0])

                context = {'id': products[0],
                           'product_details': product_name,
                           'product_shortdescription': shortdescription,
                           'products_image': full_str,
                           'products_Terms': products_Terms,
                           'products_Conditions': products_Conditions,
                           'products_full_Description': products_full_Description,
                           'products_MinimumRequirements': products_MinimumRequirements,
                           'products_Code': products_Code,
                           'products_applicable_Currencies': products_applicable_Currencies,

                           }
                print(context)
            else:
                print('did not execute context')

        else:
            print('not found')

    return render(request, 'accounts/product_view.html', context)


@login_required(login_url='login')
def update_product(request, selected_id):
    print('inside update')
    print(selected_id)
    if request.method == 'POST':
        description = request.POST.get('description')
    if len(description) > 0:
        print(description)

    else:
        print('No description')

    return request, "product_view.html", {'description': 'description'}


@login_required(login_url='login')
def product_configure(request):
    return render(request, "accounts/product_configure.html", {'Key': 'value'})


@login_required(login_url='login')
def product_add(request):
    context = {}

    return render(request, 'accounts/product_add.html', context)


@login_required(login_url='login')
def reports(request):
    context = {}

    return render(request, 'accounts/reports.html', context)
