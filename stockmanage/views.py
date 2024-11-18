from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from django.db.models import Sum
from openpyxl import Workbook
import matplotlib.pyplot as plt
from plotly.offline import plot
import io
from .forms import P_S_InfoForm
from django.contrib import messages
from django.views.decorators.cache import cache_control
from django.contrib.auth.decorators import login_required
import plotly.graph_objs as go
import base64
from django.shortcuts import redirect, get_object_or_404
from . models import P_S_Info
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@login_required(login_url="sign_in")
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def dashboard(request):
    if request.method == 'POST':
        form = P_S_InfoForm(request.POST)
        if form.is_valid():
            detail_obj = form.save(commit=False)
            detail_obj.created_by = request.user
            detail_obj.save()
            messages.success(request, "Entry saved successfully.")
            return redirect('home')  # Redirect or reload the page after successful save
        else:
            # Collect form errors to show to the user
            messages.error(request, "Please correct the errors below.")
    else:
        form = P_S_InfoForm()

    return render(request, 'first.html', {'form': form})




User = get_user_model()  # Use the custom user model

@login_required(login_url="sign_in")
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def admin_dashboard(request):
    users = User.objects.filter(user_type ='normal')  # Fetch all users for the dropdown list
    selected_user_id = request.session.get('selected_user_id')
    if request.method == "POST":
        selected_user_id = request.POST.get('user_id')
        # Redirect to purchase_admin with the selected user_id
        request.session['selected_user_id'] = selected_user_id
        return redirect('purchase_admin', user_id=selected_user_id)

    return render(request, 'admin_temp/admin_dash.html', {'user_id': selected_user_id, 'users': users})

@login_required(login_url="sign_in")
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def purchase_admin(request, user_id):
    if (user_id =='all'):
        purchase_info = P_S_Info.objects.filter(SorP="purchase")
        return render(request,'admin_temp/admin_purchase.html',{'entries': purchase_info})
    else:
        user = User.objects.get(id=user_id)
        purchase_info = P_S_Info.objects.filter(SorP="purchase",created_by=user)
        return render(request,'admin_temp/admin_purchase.html',{'entries': purchase_info})

@login_required(login_url="sign_in")
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def stock_movement_admin(request, user_id):
    if (user_id =='all'):
        sale_info = P_S_Info.objects.filter(SorP="stock_Movement")
        return render(request,'admin_temp/admin_stock_movement.html',{'entries': sale_info})
    else:
        user = User.objects.get(id=user_id)
        sale_info = P_S_Info.objects.filter(SorP="stock_Movement",created_by=user)
        return render(request,'admin_temp/admin_stock_movement.html',{'entries': sale_info})

@login_required(login_url="sign_in")
@cache_control(no_cache=True, must_revalidate=True, no_store=True) 
def admin_stock(request, user_id):
    if (user_id =='all'):
         purchase_quantities = P_S_Info.objects.filter(SorP='purchase').values('item').annotate(total=Sum('quantity'))
         stock_quantities = P_S_Info.objects.filter(SorP='stock_Movement').values('item').annotate(total=Sum('quantity'))
    else:
        user = User.objects.get(id=user_id)
        purchase_quantities = P_S_Info.objects.filter(SorP='purchase',created_by=user).values('item').annotate(total=Sum('quantity'))
        stock_quantities = P_S_Info.objects.filter(SorP='stock_Movement',created_by=user).values('item').annotate(total=Sum('quantity'))

    stock_summary = {}
    
    # Populate the stock_summary with purchase quantities
    for purchase in purchase_quantities:
        stock_summary[purchase['item']] = {
            'P_quantity': purchase['total'],
            'S_quantity': 0  # Initialize S_quantity to 0
        }
    
    # Populate the stock_summary with stock movement quantities
    for stock in stock_quantities:
        if stock['item'] in stock_summary:
            stock_summary[stock['item']]['S_quantity'] = stock['total']
        else:
            stock_summary[stock['item']] = {
                'P_quantity': 0,  # Initialize P_quantity to 0 if item not in purchase
                'S_quantity': stock['total']
            }

    # Calculate stock quantities
    for item, quantities in stock_summary.items():
        quantities['stock_quantity'] = quantities['P_quantity'] - quantities['S_quantity']

    return render(request,'admin_temp/admin_stock.html', {'stocks': stock_summary.items()})

@login_required(login_url="sign_in")  
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def purchase(request):
    purchase_info = P_S_Info.objects.filter(SorP="purchase",created_by=request.user)
    return render(request,'purchase.html',{'entries': purchase_info})

@login_required(login_url="sign_in")
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def stockmovement(request):
    sale_info = P_S_Info.objects.filter(SorP="stock_Movement",created_by=request.user)
    return render(request,'stockmovement.html',{'entries': sale_info})

@login_required(login_url="sign_in")
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def stock(request):
    purchase_quantities = P_S_Info.objects.filter(SorP='purchase',created_by=request.user).values('item').annotate(total=Sum('quantity'))
    
    # Calculate total stock movement quantities (S_quantity)
    stock_quantities = P_S_Info.objects.filter(SorP='stock_Movement',created_by=request.user).values('item').annotate(total=Sum('quantity'))

    # Create a dictionary to hold the results
    stock_summary = {}
    
    # Populate the stock_summary with purchase quantities
    for purchase in purchase_quantities:
        stock_summary[purchase['item']] = {
            'P_quantity': purchase['total'],
            'S_quantity': 0  # Initialize S_quantity to 0
        }
    
    # Populate the stock_summary with stock movement quantities
    for stock in stock_quantities:
        if stock['item'] in stock_summary:
            stock_summary[stock['item']]['S_quantity'] = stock['total']
        else:
            stock_summary[stock['item']] = {
                'P_quantity': 0,  # Initialize P_quantity to 0 if item not in purchase
                'S_quantity': stock['total']
            }

    # Calculate stock quantities
    for item, quantities in stock_summary.items():
        quantities['stock_quantity'] = quantities['P_quantity'] - quantities['S_quantity']

    return render(request,'stock.html', {'stocks': stock_summary.items()})

def delete_entry(request, id):
    entry = get_object_or_404(P_S_Info, id=id)
    entry.delete()
    return redirect(request.META.get('HTTP_REFERER', 'home'))

def update_entry(request):
    if request.method == 'POST':
        entry_id = request.POST.get('entry_id')
        entry = get_object_or_404(P_S_Info, id=entry_id)

        # Update entry fields with form data
        entry.date = request.POST.get('date')
        entry.mr_mh_no = request.POST.get('mr_mh_no')
        entry.item = request.POST.get('item')
        entry.unit_of_measure = request.POST.get('unit')
        entry.quantity = request.POST.get('quantity')
        entry.supplier_name = request.POST.get('supplier')
        entry.project_no = request.POST.get('project')
        entry.invoice_no = request.POST.get('invoice')

        entry.save()
        return redirect(request.META.get('HTTP_REFERER', 'home')) 
    

def admin_export_to_excel(request, record_type,user_id):

    if (user_id =='all'):
        if record_type == 'purchase':
            entries = P_S_Info.objects.filter(SorP='purchase')
            filename = 'Purchase_Details.xlsx'
        elif record_type == 'stock_movement':
            entries = P_S_Info.objects.filter(SorP='stock_Movement')
            filename = 'Stock_Movement_Details.xlsx'
        else:
            # If an invalid type is passed, return an empty response or handle error
            return HttpResponse("Invalid record type", status=400)
    else:
        user = User.objects.get(id=user_id)
        if record_type == 'purchase':
            entries = P_S_Info.objects.filter(SorP='purchase',created_by=user)
            filename = 'Purchase_Details.xlsx'
        elif record_type == 'stock_movement':
            entries = P_S_Info.objects.filter(SorP='stock_Movement',created_by=user)
            filename = 'Stock_Movement_Details.xlsx'
        else:
            # If an invalid type is passed, return an empty response or handle error
            return HttpResponse("Invalid record type", status=400)

            

    # Check record type ('purchase' or 'stock_Movement') to filter data
    

    # Create a new Excel workbook and select the active sheet
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Records"

    # Define the headers
    headers = ["Date", "MR or MH no", "Item", "Unit of Measure", "Quantity", "Supplier Name", "Project No", "Invoice No"]
    sheet.append(headers)  # Add header row to the sheet

    # Write data to Excel
    for entry in entries:
        row = [
            entry.date,
            entry.mr_mh_no,
            entry.item,
            entry.unit_of_measure,
            entry.quantity,
            entry.supplier_name,
            entry.project_no,
            entry.invoice_no,
        ]
        sheet.append(row)

    # Create an HTTP response with the Excel content
    response = HttpResponse(content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response["Content-Disposition"] = f'attachment; filename="{filename}"'

    # Save workbook to response
    workbook.save(response)
    return response



def export_to_excel(request, record_type):
    # Check record type ('purchase' or 'stock_Movement') to filter data
    if record_type == 'purchase':
        entries = P_S_Info.objects.filter(SorP='purchase',created_by=request.user)
        filename = 'Purchase_Details.xlsx'
    elif record_type == 'stock_movement':
        entries = P_S_Info.objects.filter(SorP='stock_Movement',created_by=request.user)
        filename = 'Stock_Movement_Details.xlsx'
    else:
        # If an invalid type is passed, return an empty response or handle error
        return HttpResponse("Invalid record type", status=400)

    # Create a new Excel workbook and select the active sheet
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Records"

    # Define the headers
    headers = ["Date", "MR or MH no", "Item", "Unit of Measure", "Quantity", "Supplier Name", "Project No", "Invoice No"]
    sheet.append(headers)  # Add header row to the sheet

    # Write data to Excel
    for entry in entries:
        row = [
            entry.date,
            entry.mr_mh_no,
            entry.item,
            entry.unit_of_measure,
            entry.quantity,
            entry.supplier_name,
            entry.project_no,
            entry.invoice_no,
        ]
        sheet.append(row)

    # Create an HTTP response with the Excel content
    response = HttpResponse(content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response["Content-Disposition"] = f'attachment; filename="{filename}"'

    # Save workbook to response
    workbook.save(response)
    return response

@login_required(login_url="sign_in")
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def admin_analysis(request, user_id):
    if (user_id =='all'):
        purchase_data = P_S_Info.objects.filter(SorP='purchase').values('item').annotate(total=Sum('quantity'))
        stock_data = P_S_Info.objects.filter(SorP='stock_Movement').values('item').annotate(total=Sum('quantity'))

    else:
        user = User.objects.get(id=user_id) 
        purchase_data = P_S_Info.objects.filter(SorP='purchase',created_by=user).values('item').annotate(total=Sum('quantity'))
        stock_data = P_S_Info.objects.filter(SorP='stock_Movement',created_by=user).values('item').annotate(total=Sum('quantity'))

    # Prepare data for plotting purchase totals
    purchase_items = [data['item'] for data in purchase_data]
    purchase_totals = [data['total'] for data in purchase_data]

    # Prepare data for plotting stock movement totals
    stock_items = [data['item'] for data in stock_data]
    stock_totals = [data['total'] for data in stock_data]

    # Create a bar plot for purchase totals
    plt.figure(figsize=(10, 5))
    plt.bar(purchase_items, purchase_totals, color='blue')
    plt.title('Total Purchases by Item')
    plt.xlabel('Items')
    plt.ylabel('Total Quantity')
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Save purchase plot to a PNG image
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close(plt.gcf())
    buf.seek(0)
    purchase_image_png = buf.getvalue()
    buf.close()
    purchase_plot_url = base64.b64encode(purchase_image_png).decode('utf-8')
    purchase_plot_url = f'data:image/png;base64,{purchase_plot_url}'

    # Create a bar plot for stock movement totals
    plt.figure(figsize=(10, 5))
    plt.bar(stock_items, stock_totals, color='orange')
    plt.title('Total Stock Movement by Item')
    plt.xlabel('Items')
    plt.ylabel('Total Quantity')
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Save stock movement plot to a PNG image
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close(plt.gcf())
    buf.seek(0)
    stock_image_png = buf.getvalue()
    buf.close()
    stock_plot_url = base64.b64encode(stock_image_png).decode('utf-8')
    stock_plot_url = f'data:image/png;base64,{stock_plot_url}'

     # Prepare purchase summary
    purchase_summary = {
        'total_items': len(purchase_items),
        'total_quantity': sum(purchase_totals),
        'item_details': zip(purchase_items, purchase_totals)  # Pair items with totals
    }   

    # Create a pie chart for stock movement
    pie_fig = go.Figure(data=[go.Pie(labels=purchase_items, values=purchase_totals)])
    pie_plot_url1 = plot(pie_fig, output_type='div')

    # Create a pie chart for stock movement
    pie_fig = go.Figure(data=[go.Pie(labels=stock_items, values=stock_totals)])
    pie_plot_url = plot(pie_fig, output_type='div')

    # Return render with plot URLs
    return render(request, 'admin_temp/admin_analysis.html', {
        'purchase_plot_url': purchase_plot_url,
        'stock_plot_url': stock_plot_url,
        'purchase_totals': purchase_totals,
        'purchase_summary': purchase_summary,
        'pie_plot_url1': pie_plot_url1,
        'pie_plot_url': pie_plot_url,
        'stock_summary': zip(stock_items, stock_totals),  # Use zip to pair items with totals for stock
    })


@login_required(login_url="sign_in")
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def analysis(request):
    # Query purchase and stock movement data
    purchase_data = P_S_Info.objects.filter(SorP='purchase',created_by=request.user).values('item').annotate(total=Sum('quantity'))
    stock_data = P_S_Info.objects.filter(SorP='stock_Movement',created_by=request.user).values('item').annotate(total=Sum('quantity'))

    # Prepare data for plotting purchase totals
    purchase_items = [data['item'] for data in purchase_data]
    purchase_totals = [data['total'] for data in purchase_data]

    # Prepare data for plotting stock movement totals
    stock_items = [data['item'] for data in stock_data]
    stock_totals = [data['total'] for data in stock_data]

    # Create and save the purchase plot
    fig1 = plt.figure(figsize=(10, 5))
    plt.bar(purchase_items, purchase_totals, color='blue')
    plt.title('Total Purchases by Item')
    plt.xlabel('Items')
    plt.ylabel('Total Quantity')
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Save purchase plot to a PNG image
    buf_purchase = io.BytesIO()
    fig1.savefig(buf_purchase, format='png')
    plt.close(fig1)  # Close the specific figure instance
    buf_purchase.seek(0)
    purchase_image_png = buf_purchase.getvalue()
    buf_purchase.close()
    purchase_plot_url = base64.b64encode(purchase_image_png).decode('utf-8')
    purchase_plot_url = f'data:image/png;base64,{purchase_plot_url}'

    # Create and save the stock movement plot
    fig2 = plt.figure(figsize=(10, 5))
    plt.bar(stock_items, stock_totals, color='orange')
    plt.title('Total Stock Movement by Item')
    plt.xlabel('Items')
    plt.ylabel('Total Quantity')
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Save stock movement plot to a PNG image
    buf_stock = io.BytesIO()
    fig2.savefig(buf_stock, format='png')
    plt.close(fig2)  # Close the specific figure instance
    buf_stock.seek(0)
    stock_image_png = buf_stock.getvalue()
    buf_stock.close()
    stock_plot_url = base64.b64encode(stock_image_png).decode('utf-8')
    stock_plot_url = f'data:image/png;base64,{stock_plot_url}'

     # Prepare purchase summary
    purchase_summary = {
        'total_items': len(purchase_items),
        'total_quantity': sum(purchase_totals),
        'item_details': zip(purchase_items, purchase_totals)  # Pair items with totals
    }   

    # Create a pie chart for stock movement
    pie_fig = go.Figure(data=[go.Pie(labels=purchase_items, values=purchase_totals)])
    pie_plot_url1 = plot(pie_fig, output_type='div')

    # Create a pie chart for stock movement
    pie_fig = go.Figure(data=[go.Pie(labels=stock_items, values=stock_totals)])
    pie_plot_url = plot(pie_fig, output_type='div')

    # Return render with plot URLs
    return render(request, 'analysis.html', {
        'purchase_plot_url': purchase_plot_url,
        'stock_plot_url': stock_plot_url,
        'purchase_totals': purchase_totals,
        'purchase_summary': purchase_summary,
        'pie_plot_url1': pie_plot_url1,
        'pie_plot_url': pie_plot_url,
        'stock_summary': zip(stock_items, stock_totals),  # Use zip to pair items with totals for stock
    })

@login_required
@csrf_exempt
def get_stock_quantity(request):
    item_name = request.GET.get('item')
    if not item_name:
        return JsonResponse({'success': False, 'message': 'Item name is required.'})
    
    try:
        # Calculate available stock for the current user
        available_stock = P_S_Info.get_available_stock(item_name, request.user)
        return JsonResponse({'success': True, 'stock_quantity': available_stock})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})