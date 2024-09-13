# from stats.utils.admin.general.avg import get_avg_income
# from stats.utils.admin.general.income import (
#     get_daily_income,
#     get_monthly_income,
#     get_yearly_income,
# )
# from stats.utils.admin.products.count import (
#     get_in_stock_products_count,
#     get_out_of_stock_products_count,
# )
# from stats.utils.admin.products.new import (
#     get_daily_new_products,
#     get_monthly_new_products,
#     get_yearly_new_products,
# )
# from stats.utils.admin.products.sold import (
#     get_daily_sold_products,
#     get_monthly_sold_products,
#     get_yearly_sold_products,
# )
# from stats.utils.admin.rfq.count import (
#     get_total_approved_quotes_count,
#     get_total_pending_quotes_count,
#     get_total_quotes_count,
#     get_total_rejected_quotes_count,
# )
# from stats.utils.admin.rfq.value import (
#     get_daily_accepted_offers_value,
#     get_monthly_accepted_offers_value,
#     get_yearly_accepted_offers_value,
# )
# from stats.utils.admin.users.active import (
#     get_daily_active_users,
#     get_monthly_active_users,
#     get_yearly_active_users,
# )
# from stats.utils.admin.users.count import get_users_count
# from stats.utils.admin.users.new import (
#     get_daily_new_users,
#     get_monthly_new_users,
#     get_yearly_new_users,
# )


# def dashboard_callback(request, context):

#     if not context:
#         context = {}

#     general = {
#         "daily_income": get_daily_income(),
#         "monthly_income": get_monthly_income(),
#         "yearly_income": get_yearly_income(),
#         "avg": get_avg_income(),
#     }

#     users = {
#         "count": get_users_count(),
#         "daily_active": get_daily_active_users(),
#         "monthly_active": get_monthly_active_users(),
#         "yearly_active": get_yearly_active_users(),
#         "daily_new": get_daily_new_users(),
#         "monthly_new": get_monthly_new_users(),
#         "yearly_new": get_yearly_new_users(),
#     }

#     products = {
#         "in_stock_count": get_in_stock_products_count(),
#         "out_stock_count": get_out_of_stock_products_count(),
#         "daily_new": get_daily_new_products(),
#         "monthly_new": get_monthly_new_products(),
#         "yearly_new": get_yearly_new_products(),
#         "daily_sold": get_daily_sold_products(),
#         "monthly_sold": get_monthly_sold_products(),
#         "yearly_sold": get_yearly_sold_products(),
#     }

#     rfq = {
#         "count": get_total_quotes_count(),
#         "approved": get_total_approved_quotes_count(),
#         "rejected": get_total_rejected_quotes_count(),
#         "pending": get_total_pending_quotes_count(),
#         "daily_value": get_daily_accepted_offers_value(),
#         "monthly_value": get_monthly_accepted_offers_value(),
#         "yearly_value": get_yearly_accepted_offers_value(),
#     }

#     context.update({"general": general, "users": users, "products": products, "rfq": rfq})

#     return context

