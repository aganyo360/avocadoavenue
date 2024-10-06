from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
import pandas as pd
from .models import AvocadoAvenue, Sheet
from django.db.models import Count, Sum, F
from django.contrib import messages
import pandas as pd
from django.shortcuts import render, redirect
from .models import AvocadoAvenue, Sheet

def index(request):
    if request.method == 'POST' and 'xlsx' in request.FILES:
        xlsx = request.FILES.get('xlsx')
        sheet_name = request.POST.get('sheet_name')
        try:
            df1 = pd.read_excel(xlsx)
            df = df1.dropna()
            sheet, created = Sheet.objects.get_or_create(name=sheet_name)
            for index, row in df.iterrows():
                # Hello
                grn, type_of_fruit, initial_weight, fruit_cost, sorted_weight = row.values
                AvocadoAvenue.objects.create(grn=grn, type_of_fruit=type_of_fruit, initial_weight=initial_weight, fruid_cost=fruit_cost, sorted_weight=sorted_weight, sheet=sheet)     
            return redirect('analytics')
        
        except Exception as e:
            messages.error(request, f"Error occurred while processing the file: {e}")
            return redirect('index')
    
    return render(request, 'index.html')


def analytics(request):
    if 'sheet' not in request.GET:
        return redirect(f"{reverse('analytics')}?sheet={Sheet.objects.last().id}")
    sheet_id=request.GET.get('sheet')
    sheet = get_object_or_404(Sheet, id=sheet_id)
    sheets = Sheet.objects.all()
    fruit_data = (AvocadoAvenue.objects.filter(sheet = sheet ).values('type_of_fruit').annotate(total_count=Count('id'), total_initial_weight=Sum('initial_weight'), total_sorted_weight=Sum('sorted_weight'), total_shrinkage=Sum(F('initial_weight') - F('sorted_weight')),))
    # print(fruit_data)
    
    results = []
    for fruit in fruit_data:
        total_initial_weight = fruit['total_initial_weight']
        total_sorted_weight = fruit['total_sorted_weight']
        total_shrinkage = fruit['total_shrinkage']
        shrinkage_percentage = (total_shrinkage / total_initial_weight * 100) if total_initial_weight else 0

        results.append({
            'type_of_fruit': fruit['type_of_fruit'],
            'total_count': fruit['total_count'],
            'total_initial_weight': total_initial_weight,
            'total_shrinkage': total_shrinkage,
            "total_sorted_weight":total_sorted_weight,
            'shrinkage_percentage': shrinkage_percentage,
        })
    subtotal_initial_weight = sum(item['total_initial_weight'] for item in fruit_data)
    subtotal_sorted_weight=sum(item['total_sorted_weight'] for item in fruit_data)
    subtotal_shrinkage= sum(item['total_shrinkage'] for item in fruit_data)
    total_shrinkage_percentage = (subtotal_shrinkage / subtotal_initial_weight * 100) if subtotal_initial_weight else 0
    subtotals = {
    'subtotal_count': sum(item['total_count'] for item in fruit_data),
    'subtotal_initial_weight': subtotal_initial_weight ,
    'subtotal_sorted_weight': subtotal_sorted_weight,
    'subtotal_shrinkage':subtotal_shrinkage,  
    'total_shrinkage_percentage': total_shrinkage_percentage
    }
    
    context ={
        'fruit_data': results,
        "sheet_id": sheet,
        "sheets":sheets,
        "subtotals":subtotals
    }
    return render(request, 'analytics.html', context )
