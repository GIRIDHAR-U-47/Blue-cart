# store/dashboard.py
from jet.dashboard.dashboard import Dashboard
from store.dashboard_widgets import OrderPricePieChart

class CustomIndexDashboard(Dashboard):
    columns = 2

    def init_with_context(self, context):
        self.children.append(OrderPricePieChart())
