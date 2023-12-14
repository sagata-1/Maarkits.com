from helpers import lookup
from helpers import apology_test
from helpers import total_computation
from helpers import leaderboard
from helpers import buy_test, sell_test
import psycopg2
from psycopg2.extras import RealDictCursor


con = psycopg2.connect(dbname="postgres", user="postgres", password="Saucepan03@!", host="db.krvuffjhmqiyerbpgqtv.supabase.co")
db = con.cursor(cursor_factory=RealDictCursor)

def test_buy_sell():
    db.execute(
        "SELECT * FROM portfolios WHERE user_id = (%s)", (2, )
    )
    portfolio = db.fetchall()
    db.execute (
        "SELECT bought FROM users WHERE id = (%s)", (2, )
    )
    bought = db.fetchall()
    bought = bought[0]["bought"]
    db.execute (
        "SELECT sold FROM users WHERE id = (%s)", (2, )
    )
    sold = db.fetchall()
    sold = sold[0]["sold"]
    assert(bought > 0)
    assert(sold > 0)
    assert(len(portfolio) == 0)
    # Test buy capabilities
    assert(buy_test("TSLA", "2", "5", "temp") == 200)
    assert(buy_test("GOOG", "2", "1000000", "temp") == 400)
    assert(buy_test("TSLA", "2", "5", "Forex") == 400)
    assert(buy_test("MYR/EUR", "2", "5", "temp") == 400)
    db.execute(
        "SELECT * FROM portfolios WHERE user_id = (%s)", (2, )
    )
    portfolio = db.fetchall()
    db.execute (
        "SELECT bought FROM users WHERE id = (%s)", (2, )
    )
    bought_1 = db.fetchall()
    bought_1 = bought_1[0]["bought"]
    assert(bought_1 > bought)
    # Test sell capabilities
    assert(portfolio[0]["stock_name"] == "Tesla, Inc.")
    assert(portfolio[0]["stock_symbol"] == "TSLA")
    assert(portfolio[0]["num_shares"] == 5)
    assert(sell_test("TSLA", "2", "10000000") == 400)
    assert(sell_test("TSLA", "2", "5") == 200)
    db.execute (
        "SELECT sold FROM users WHERE id = (%s)", (2, )
    )
    sold_1 = db.fetchall()
    sold_1 = sold_1[0]["sold"]
    assert(sold_1 > sold)
    db.execute(
        "SELECT * FROM portfolios WHERE user_id = (%s)", (2, )
    )
    portfolio = db.fetchall()
    assert(len(portfolio) == 0)
    

def test_total():
    db.execute(
        "SELECT * FROM portfolios WHERE user_id IN (SELECT id FROM users WHERE username = (%s))", ("ss", )
    )
    portfolio = db.fetchall()
    db.execute("SELECT * FROM users WHERE username = (%s)", ("ss",))
    cash = db.fetchall()
    cash = float(cash[0]["cash"])
    total = cash
    for stock in portfolio:
        total += stock["price"] * stock["num_shares"]
    assert(total_computation("ss") == (total, cash))
    
def test_leaderboard():
    assert(len(leaderboard()) == 10)
    for i in range(9):
        assert(leaderboard()[i]["total"] >= leaderboard()[i + 1]["total"])
        