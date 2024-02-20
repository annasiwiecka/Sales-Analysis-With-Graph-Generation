import uuid, base64
from customers.models import Customer
from profiles.models import Profile
from io import BytesIO
import matplotlib.pyplot as plt
import seaborn as sns


def generate_code():
    code = str(uuid.uuid4()).replace("-", "").upper()[:12]
    return code


def get_customer_from_id(val):
    customer = Customer.objects.get(id=val)
    return customer


def get_salesman_from_id(val):
    salesman = Profile.objects.get(id=val)
    return salesman


def get_graph():
    buffer = BytesIO()
    plt.savefig(buffer, format="png")
    buffer.seek(0)
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png).decode("utf-8")
    buffer.close()
    return graph


def get_key(res_by):
    if res_by == "#1":
        key = "transaction_id"
    elif res_by == "#2":
        key = "category"
    elif res_by == "#3":
        key = "created_at"
    return key


def get_chart(chart_type, data, results_by, **kwargs):
    plt.switch_backend("AGG")
    fig = plt.figure(figsize=(10, 4))
    key = get_key(results_by)
    d = data.groupby(key, as_index=False)["total_price"].agg("sum")
    if chart_type == "#1":
        print("bar chart")
        sns.barplot(x=key, y="total_price", data=d, palette="Set1")
    elif chart_type == "#2":
        print("pie chart")
        labels = kwargs.get("labels")
        plt.pie(data=d, x="price", labels=labels)
    elif chart_type == "#3":
        print("line chart")
        plt.plot(data["transaction_id"], data["price"], marker="o")

    plt.tight_layout()
    chart = get_graph()
    return chart


def get_chart1(chart_type, data, **kwargs):
    plt.switch_backend("AGG")
    fig = plt.figure(figsize=(10, 4))
    if chart_type == "#1":
        # plt.bar(data["transaction_id"], data["price"])
        sns.barplot(x="category", y="price", data=data, palette="Set1")
    elif chart_type == "#2":
        labels = kwargs.get("labels")
        plt.pie(data=data, x="price", labels=labels)
    elif chart_type == "#3":
        plt.plot(data["category"], data["price"], marker="o")

    plt.tight_layout()
    chart = get_graph()
    return chart
