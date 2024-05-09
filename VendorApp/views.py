from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import *
import random
import json
import string
from django.utils import timezone
from datetime import datetime
from plotly import graph_objs as go
from django.core.serializers import serialize

import logging
logging.captureWarnings(True)

def homePage(request):
    return render(request, 'index.html')


def vendorPage(request):
    return render(request, 'vendor.html')


def purchaseOrderPage(request):
    return render(request, "purchaseorder.html")


def performanceHistoryPage(request):
    return render(request, "perf_hist.html")


def vendorHandler(request, vendor_id=""):
    if request.method == "POST":
        name = request.POST.get("name")
        contact_details = request.POST.get("contact_details")
        address = request.POST.get("address")
        vendor_code = "Vendor" + ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))

        if not VendorModel.objects.filter(name=name, contact_details=contact_details, address=address).exists():
            new_vendor = VendorModel.objects.create(name=name, contact_details=contact_details, address=address, vendor_code=vendor_code)
            new_vendor.save()
            return render(request, "vendor.html", {"message": f"Vendor added successfully!! Vendor ID: {vendor_code}"})
        return render(request, "vendor.html", {"message": f"Vendor already present!! Vendor ID: {VendorModel.objects.get(name=name, contact_details=contact_details, address=address).vendor_code}"})
    if request.method == "GET":
        vendor_id = request.GET.get("vendor_id")
        if vendor_id:
            if VendorModel.objects.filter(vendor_code=vendor_id).exists():
                vendor = VendorModel.objects.get(vendor_code=vendor_id)
                return render(request, "vendor.html", {"vendor": vendor})
            return render(request, "vendor.html", {"message": "Vendor not present!!"})
        else:
            vendors = VendorModel.objects.all()
            if vendors:
                return render(request, "vendor.html", {"vendors": vendors})
            return render(request, "vendor.html", {"message": "No Vendors present!!"})
    if request.method == "PUT":
        data = request.body.decode("utf-8")
        parsed_data = json.loads(data)
        vendor_id = parsed_data.get("vendor_id")
        if vendor_id:
            updated_name = parsed_data.get("name")
            updated_contact_details = parsed_data.get("contact_details")
            updated_address = parsed_data.get("address")
            if VendorModel.objects.filter(vendor_code=vendor_id).exists():
                vendor = VendorModel.objects.get(vendor_code=vendor_id)
                should_update = 0
                if updated_name and vendor.name != updated_name:
                    vendor.name = updated_name
                    should_update += 1
                if updated_contact_details and vendor.contact_details != updated_contact_details:
                    vendor.contact_details = updated_contact_details
                    should_update += 1
                if updated_address and vendor.address != updated_address:
                    vendor.address = updated_address
                    should_update += 1
                if should_update:
                    vendor.save()
                return JsonResponse({"message": f"Vendor ID: {vendor.vendor_code} updated successfully!!"})
            return JsonResponse({"message": f"No vendor present with Vendor ID: {vendor_id}!!"})
        return JsonResponse({"message": "Provide a Vendor ID!!"})
    if request.method == "DELETE":
        if vendor_id:
            if VendorModel.objects.filter(vendor_code=vendor_id).exists():
                vendor = VendorModel.objects.get(vendor_code=vendor_id)
                vendor.delete()
                return JsonResponse({"message": f"Vendor ID: {vendor_id} deleted successfully!!"})
            return JsonResponse({"message": f"No vendor present with Vendor ID: {vendor_id}!!"})
        return JsonResponse({"message": "Provide a Vendor ID!!"})
    return redirect("vendorPage")


def purchaseOrderHandler(request, po_id=""):
    if request.method == "POST":
        data = request.body.decode("utf-8")
        parsed_data = json.loads(data)

        vendor_id = parsed_data.get("vendor_id")
        po_id = "PO" + ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        order_date = datetime.strptime(parsed_data.get("order_date"), "%Y-%m-%dT%H:%M")
        delivery_date = datetime.strptime(parsed_data.get("delivery_date"), "%Y-%m-%dT%H:%M")
        items = parsed_data.get("items")
        quantity = int(parsed_data.get("quantity"))

        if VendorModel.objects.filter(vendor_code=vendor_id).exists():
            vendor = VendorModel.objects.get(vendor_code=vendor_id)
            if not PurchaseOrderModel.objects.filter(vendor=vendor, order_date=order_date, delivery_date=delivery_date, items=items, quantity=quantity).exists():
                new_po = PurchaseOrderModel.objects.create(po_number=po_id, vendor=vendor, order_date=order_date, delivery_date=delivery_date, items=items, quantity=quantity)
                new_po.save()
                return JsonResponse({"message": f"New Purchase Order added successfully!! Purchase Order ID: {po_id}"})
            return JsonResponse({"message": f"Purchase Order already present!! Purchase Order ID: {PurchaseOrderModel.objects.get(vendor=vendor, order_date=order_date, delivery_date=delivery_date, items=items, quantity=quantity).po_number}"})
        return JsonResponse({"message": f"No vendor present with Vendor ID: {vendor_id}"})
    if request.method == "GET":
        po_id = request.GET.get("po_id")
        if po_id:
            if PurchaseOrderModel.objects.filter(po_number=po_id).exists():
                po = PurchaseOrderModel.objects.get(po_number=po_id)
                return render(request, "purchaseorder.html", {"po": po})
            return render(request, "purchaseorder.html", {"message": f"No purchase order present with Purchase Order: {po_id}"})
        else:
            pos = PurchaseOrderModel.objects.all()
            if pos:
                return render(request, "purchaseorder.html", {"pos": pos})
            return render(request, "purchaseorder.html", {"message": "No Purchase Orders present!!"})
    if request.method == "PUT":
        data = request.body.decode("utf-8")
        parsed_data = json.loads(data)
        po_id = parsed_data.get("po_id")
        if po_id:
            updated_status = parsed_data.get("status")
            updated_quality_rating = parsed_data.get("quality_rating")
            if PurchaseOrderModel.objects.filter(po_number=po_id).exists():
                po = PurchaseOrderModel.objects.get(po_number=po_id)
                should_update = 0
                if po.status.lower() != "completed" or po.status.lower() != "cancelled":
                    if parsed_data.get("delivery_date") and updated_status != "cancelled":
                        updated_delivery_date = datetime.strptime(parsed_data.get("delivery_date"), "%Y-%m-%dT%H:%M")
                        if po.delivery_date != updated_delivery_date:
                            po.delivery_date = updated_delivery_date
                            should_update += 1
                    if parsed_data.get("issue_date") and updated_status != "cancelled":
                        updated_issue_date = datetime.strptime(parsed_data.get("issue_date"), "%Y-%m-%dT%H:%M")
                        if po.issue_date != updated_issue_date:
                            po.issue_date = updated_issue_date
                            should_update += 1
                    if updated_quality_rating and po.quality_rating != updated_quality_rating and updated_status != "cancelled":
                        po.quality_rating = updated_quality_rating
                        should_update += 1
                    if updated_status and po.status != updated_status:
                        po.status = updated_status
                        should_update += 1
                    if should_update:
                        po.save()
                        if updated_status:
                            calculateFulfillmentRate(po_id)
                            if updated_status.lower() == "completed":
                                if po.delivery_date.astimezone() > timezone.now():
                                    po.delivered_late = False
                                else:
                                    po.delivered_late = True
                                calculateOnTimeDeliveryRate(po_id)
                                calculateQualityRatingAverage(po_id)
                        return JsonResponse({"message": "Purchase Order updated successfully!!"})
                    return JsonResponse({"message": "Provide data to update!!"})
                return JsonResponse({"message": f"Purchase Order has been {po.status.lower()}!! Can't update!!"})
            return JsonResponse({"message": f"No purchase order with Purchase Order ID: {po_id}!!"})
        return JsonResponse({"message": "Provide a Purchase Order ID to update!!"})
    if request.method == "DELETE":
        if po_id:
            if PurchaseOrderModel.objects.filter(po_number=po_id).exists():
                po = PurchaseOrderModel.objects.get(po_number=po_id)
                po.delete()
                return JsonResponse({"message": f"Purchase Order ID: {po_id} deleted successfully!!"})
            return JsonResponse({"message": f"No purchase order present with Purchase Order ID: {po_id}!!"})
        return JsonResponse({"message": "Provide a Purchase Order ID to delete!!"})
    return redirect("purchaseOrderPage")


def acknowledgeOrder(request, po_id=""):
    if request.method == "GET":
        if po_id:
            if PurchaseOrderModel.objects.filter(po_number=po_id).exists():
                po = PurchaseOrderModel.objects.get(po_number=po_id)
                po.acknowledgement_date = timezone.now()
                po.save()
                calculateAverageResponseTime(po_id)
                return JsonResponse({"message": f"Purchase Order ID: {po_id} acknowledged!!!"})
            return JsonResponse({"message": f"No purchase order present with Purchase Order ID: {po_id}!!"})
        return JsonResponse({"message": "Provide a Purchase Order ID to acknowledge!!"})
    return redirect("getAllPurchaseOrders")


def calculateOnTimeDeliveryRate(po_id):
    vendor_id = PurchaseOrderModel.objects.get(
        po_number=po_id).vendor.vendor_code
    vendor = VendorModel.objects.get(vendor_code=vendor_id)
    pos = PurchaseOrderModel.objects.filter(vendor=vendor)

    n = 0
    d = 0
    for po in pos:
        if po.status.lower() == "completed":
            d += 1
            if not po.delivered_late:
                n += 1
    if d != 0:
        vendor.on_time_delivery_rate = n/d
        vendor.save()
        addToPerfHistTable(vendor, timezone.now())


def calculateQualityRatingAverage(po_id):
    vendor_id = PurchaseOrderModel.objects.get(
        po_number=po_id).vendor.vendor_code
    vendor = VendorModel.objects.get(vendor_code=vendor_id)
    pos = PurchaseOrderModel.objects.filter(vendor=vendor)

    n = 0
    d = 0
    for po in pos:
        if po.status.lower() == "completed" and po.quality_rating:
            n += float(po.quality_rating)
            d += 1
    if d != 0:
        vendor.quality_rating_avg = n/d
        vendor.save()
        addToPerfHistTable(vendor, timezone.now())


def calculateAverageResponseTime(po_id):
    vendor_id = PurchaseOrderModel.objects.get(
        po_number=po_id).vendor.vendor_code
    vendor = VendorModel.objects.get(vendor_code=vendor_id)
    pos = PurchaseOrderModel.objects.filter(vendor=vendor)

    n = 0
    d = 0
    for po in pos:
        if po.acknowledgement_date and po.issue_date:
            n += abs((po.acknowledgement_date.astimezone() - po.issue_date.astimezone()).total_seconds())/(60*60*24)
            d += 1
    if d != 0:
        vendor.average_response_time = n/d
        vendor.save()
        addToPerfHistTable(vendor, timezone.now())


def calculateFulfillmentRate(po_id):
    vendor_id = PurchaseOrderModel.objects.get(
        po_number=po_id).vendor.vendor_code
    vendor = VendorModel.objects.get(vendor_code=vendor_id)
    pos = PurchaseOrderModel.objects.filter(vendor=vendor)

    n = 0
    d = 0
    for po in pos:
        if po.issue_date:
            d += 1
        if po.status.lower() == "completed" and not po.issue_date:
            n += 1
    if d != 0:
        vendor.fulfillment_rate = n/d
        vendor.save()
        addToPerfHistTable(vendor, timezone.now())


def addToPerfHistTable(vendor, date):
    perf_hist_obj = 0
    if not PerformanceHistory.objects.filter(vendor=vendor, date=date).exists():
        perf_hist_obj = PerformanceHistory.objects.create(
            vendor=vendor, date=date)
    else:
        perf_hist_obj = PerformanceHistory.objects.get(
            vendor=vendor, date=date)
    perf_hist_obj.on_time_delivery_rate = vendor.on_time_delivery_rate
    perf_hist_obj.quality_rating_avg = vendor.quality_rating_avg
    perf_hist_obj.average_response_time = vendor.average_response_time
    perf_hist_obj.fulfillment_rate = vendor.fulfillment_rate
    perf_hist_obj.save()


def getPerformance(request):
    if request.method == "GET":
        vendor_id = request.GET.get("vendor_id")
        if vendor_id:
            if VendorModel.objects.filter(vendor_code=vendor_id).exists():
                vendor = VendorModel.objects.get(vendor_code=vendor_id)
                if PerformanceHistory.objects.filter(vendor=vendor).exists():
                    performances = PerformanceHistory.objects.filter(
                        vendor=vendor)
                    scores = {
                        "Date": [],
                        "On Time Delivery Rate": [],
                        "Quality Rating Average": [],
                        "Average Response Time": [],
                        "Fulfillment Rate": []
                    }
                    for p in performances:
                        scores["Date"].append(str(p.date))
                        scores["On Time Delivery Rate"].append(p.on_time_delivery_rate)
                        scores["Quality Rating Average"].append(p.quality_rating_avg)
                        scores["Average Response Time"].append(p.average_response_time)
                        scores["Fulfillment Rate"].append(p.fulfillment_rate)

                    serialized_performances = serialize('json', performances)

                    fig = go.Figure()

                    if 'Date' in scores:
                        for key, values in scores.items():
                            if key != 'Date':
                                fig.add_trace(go.Scatter(
                                    x=scores['Date'], y=values, mode='lines+markers', name=key))

                    fig.update_layout(title='Vendor Performance Attributes',
                                      xaxis_title='Date',
                                      yaxis_title='Value',
                                      legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))

                    return render(request, "perf_hist.html", {"graph": fig.to_html(full_html=False, include_plotlyjs='cdn'), "serialized_performances": serialized_performances})
                return render(request, "perf_hist.html", {"message": f"No performance history present with Vendor ID: {vendor_id}!!"})
            return render(request, "perf_hist.html", {"message": f"No vendor present with Vendor ID: {vendor_id}!!"})
        return render(request, "perf_hist.html", {"message": f"Provide a Vendor ID to get the performance!!"})
    return redirect("performanceHistoryPage")
