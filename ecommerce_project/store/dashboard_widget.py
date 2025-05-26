# store/dashboard_widgets.py
from jet.dashboard.modules import DashboardModule
from django.db.models import Sum
from .models import Order
import json

class OrderPricePieChart(DashboardModule):
    title = "Order Price Distribution"
    template = 'store/widgets/order_pie_chart.html'
    children = []
    collapsible = False

    def init_with_context(self, context):
        data = (
            Order.objects
            .values('product__name')
            .annotate(total_price=Sum('product__price'))
        )
        labels = [d['product__name'] for d in data]
        values = [float(d['total_price']) for d in data]
        self.children = [{
            'labels': json.dumps(labels),
            'data': json.dumps(values),
        }]
