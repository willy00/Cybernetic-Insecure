from cybernetic import app, db
import random
from datetime import datetime
from cybernetic.Models import Order, User, UserCart, Product, OrderedProduct, Card, Address, ProductRating
import requests


def add_test_data():
    user_list = []
    # test users
    user1 = User(
        email="test@test.com",
        password="password",
        username="tester"
    )
    db.session.add(user1)
    user2 = User(
        email="dylanliew0503@gmail.com",
        password="password",
        username="forgetful"
    )
    db.session.add(user2)
    admin1 = User(
        email="admin@test.com",
        password="password",
        username="admin",
        admin=True
    )
    db.session.add(admin1)
    db.session.commit()
    cart1 = UserCart(user_id=user1.id)
    db.session.add(cart1)
    cart2 = UserCart(user_id=user2.id)
    db.session.add(cart2)
    db.session.commit()
    user_list.append((user1, "Testing Dude"))
    user_list.append((user2, "William"))

    print("=== Test Users === ")
    print("User 1 - Test User \n"
          "email: test@test.com\n"
          "password: password\n")
    print("User 2 - Forget Password Demo\n"
          "email: dylanliew0503@gmail.com\n"
          "password: password\n")
    print("User 3 - Admin Demo\n"
          "email: admin@gmail.com\n"
          "password: password\n")

    # Adding Sample Products
    p1 = Product(name="Blackpods pro",
                 retail_price=129,
                 description="This is a scam",
                 stock=20,
                 pic_filename="scampods_3529963a5-a2fa-458c-8b71-b4f8acdc1e12.jpg")
    db.session.add(p1)
    p2 = Product(name="Blackpods 3",
                 retail_price=80,
                 description="This is actually not bad",
                 stock=20,
                 pic_filename="blackpods_26da9d352-5a7e-4284-a17e-76f90eae03ef.jpg")
    db.session.add(p2)
    p3 = Product(name="Airpods 2",
                 retail_price=180,
                 description="Very revolutionary",
                 stock=190,
                 pic_filename="Airpods_25ba37068-f15d-436b-9639-a91e15d2d33a.jpg")
    db.session.add(p3)
    count = 4
    for i in range(100):
        sample_p = Product(name="Sample Product {}".format(count),
                           retail_price=random.uniform(50, 100),
                           description="Sample Product",
                           stock=random.randint(50, 200),
                           pic_filename="samples.jpeg")
        count += 1
        db.session.add(sample_p)
    db.session.commit()

    def generate_contact_number():
        number = "9"
        for x in range(7):
            number += str(random.randint(0, 9))
        return number

    # Sample Users
    r = requests.get("https://randomuser.me/api/?results=100")
    results = r.json()["results"]

    for dat in results:
        login_dat = dat.get("login")
        user = User(
            email=dat.get("email"),
            password=login_dat.get("password"),
            username=login_dat.get("username")
        )
        db.session.add(user)
        db.session.commit()
        user_list.append((user, f"{dat['name']['first']} {dat['name']['last']}"))
        cart = UserCart(user_id=user.id)
        db.session.add(cart)
        db.session.commit()
        print(
            f"Fake User Created\nUser ID: {user.id}\nUsername: {user.username}\nEmail: {user.email}\nPassword: {login_dat.get('password')}")
    product_list = Product.query.all()

    # Sample Cards
    for user, full_name in user_list[:5]:
        for x in range(2):
            s_nums = [4, 3, 6, 5]
            c_type = ""
            c_d = ["Credit", "Debit"]
            c_number = str(random.choice(s_nums)) + str(random.randint(100000000000000, 999999999999999))
            if c_number[0] == "4":
                c_type += "Visa "
            elif c_number[0] == "3":
                c_type += "AMEX "
            elif c_number[0] == "6":
                c_type += "Discover "
            else:
                c_type += "Mastercard "
            c_type += random.choice(c_d)
            print(f"{c_number}, {c_type}")
            c = Card(name=full_name, type=c_type, cvc=random.randint(100, 9999),
                     expiry=datetime(random.randint(2023, 2030), random.randint(1, 12),
                                     1).timestamp(),
                     number=c_number, user_id=user.id)
            db.session.add(c)
            db.session.commit()

    # Sample Address
    for user, full_name in user_list[:5]:
        a = Address(description="Home",
                    contact=generate_contact_number(),
                    name=full_name,
                    address_1="521 Woodlands Dr 14 #02-343",
                    address_2="#02-343",
                    postal_code="730521", user_id=user.id, default=True)
        db.session.add(a)
        a = Address(description="Office",
                    contact=generate_contact_number(),
                    name=full_name,
                    address_1="101 THOMSON ROAD",
                    address_2=None,
                    postal_code="307591", user_id=user.id, default=False)
        db.session.add(a)
        db.session.commit()

    # Sample Orders
    for user, _ in user_list[:2]:
        ts_now = 1609459200000
        for y in range(0, 5):
            ts_now -= 31556952000
            for x in range(0, 10):
                ts = ts_now
                month = random.randint(0, 11)
                ts += 2629746000 * month
                total = 0
                s_list = []
                for z in range(0, random.randint(1, 2)):
                    product = random.choice(product_list)
                    if len(s_list) != 0:
                        while True:
                            counter = 0
                            for p_id, qty, price in s_list:
                                if p_id == product.id:
                                    product = random.choice(product_list)
                                else:
                                    counter += 1
                            if counter == len(s_list):
                                break
                    s_list.append((product.id, random.randint(1, 5), product.retail_price))
                for _, qty, price in s_list:
                    total += qty * price
                o = Order(
                    order_date=ts,
                    total_price=total,
                    user_id=user.id
                )
                db.session.add(o)
                db.session.commit()
                for p_id, qty, price in s_list:
                    ordered = OrderedProduct(
                        order_id=o.id,
                        product_id=p_id,
                        quantity=qty
                    )
                    db.session.add(ordered)
                db.session.commit()
                print(f"Fake order created.\nOrder ID: {o.id}")

    # Sample Rating
    orders = Order.query.all()
    for order in orders:
        ordered_stuffs = OrderedProduct.query.filter_by(order_id=order.id)
        for stuff in ordered_stuffs:
            review = ProductRating(user_id=order.user_id, rating=random.randint(1, 5), comments="nil",
                                   product_id=stuff.product_id)
            db.session.add(review)
    db.session.commit()


@app.cli.command('db_create')
def db_create():
    db.create_all()
    print('Database Created!')


@app.cli.command('db_drop')
def db_drop():
    db.drop_all()
    print('Database Dropped!')


@app.cli.command('db_seed')
def db_seed():
    add_test_data()
    print("Sample Data Added!")


@app.cli.command('db_reset')
def db_reset():
    db.drop_all()
    db.create_all()
    add_test_data()
    print("Database Reset Successfully!")


if __name__ == '__main__':
    app.run(debug=True, port=1000)
