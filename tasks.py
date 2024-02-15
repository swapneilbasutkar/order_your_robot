from robocorp.tasks import task
from robocorp.browser import Browser
from robocorp import browser
from RPA.HTTP import HTTP
from RPA.Tables import Tables

@task
def order_robot_from_RobotSpareBin():
    """
    Orders robots from RobotSpareBin Industries Inc.
    Saves the order HTML receipt as a PDF file.
    Saves the screenshot of the ordered robot.
    Embeds the screenshot of the robot to the PDF receipt.
    Creates ZIP archive of the receipts and the images.
    """
    browser.configure(slowmo=200)
    open_robot_order_website()
    #download_orders_file()
    fill_form_with_csv_data()

def open_robot_order_website():
    """Navigates to the given URL and clicks on pop up"""
    browser.goto("https://robotsparebinindustries.com/#/robot-order")
    page = browser.page()
    page.click('text=OK')

def download_orders_file():
    """Downloads the orders file from the give URL"""
    http = HTTP()
    http.download("https://robotsparebinindustries.com/orders.csv"
                  , overwrite=True)

def order_another_bot():
    page = browser.page()
    page.click("#order-another")

def clicks_ok():
    page = browser.page()
    page.click('text=OK')

def fill_and_submit_robot_data(order):
    """Fills in the robot order details and clicks the 'Order' button"""
    #bro = Browser()
    page = browser.page()
    head_names = {
        "1" : "Roll-a-thor head",
        "2" : "Peanut crusher head",
        "3" : "D.A.V.E head",
        "4" : "Andy Roid head",
        "5" : "Spanner mate head",
        "6" : "Drillbit 2000 head"
    }
    head_number = order["Head"]
    page.select_option("#head", head_names.get(head_number))
    page.click('//*[@id="root"]/div/div[1]/div/div[1]/form/div[2]/div/div[{0}]/label'.format(order["Body"]))
    page.fill("input[placeholder='Enter the part number for the legs']", order["Legs"])
    page.fill("#address", order["Address"])
    while True:
        page.click("#order")
        order_another = page.query_selector("#order-another")
        if order_another:
            order_another_bot()
            clicks_ok()
            break

def fill_form_with_csv_data():
    """Read data from csv and fill in the robot order form"""
    csv_file = Tables()
    robot_orders = csv_file.read_table_from_csv("orders.csv")
    for order in robot_orders:
        fill_and_submit_robot_data(order)

    
