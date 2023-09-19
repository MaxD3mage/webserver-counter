import sqlite3
from aiohttp import web
from datetime import datetime

conn = sqlite3.connect('visits.db')
c = conn.cursor()

#таблица
c.execute('''
    CREATE TABLE IF NOT EXISTS visits (
        id INTEGER PRIMARY KEY,
        ip TEXT NOT NULL,
        path TEXT NOT NULL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(ip, path)
    )
''')

async def handle(request):
    ip = request.remote
    path = request.path

    with conn:
        c.execute("INSERT INTO visits (ip, path) VALUES (?, ?)", (ip, path))

    return web.Response(text="Hello,\n"
                                 "If you want to see counter - use /stats/{period}\n"
                                 "If you want to see unique counter - use /unistats/{period}\n"
                                 "Where period can be day/month/year/total")

async def get_stats(request):
    period = request.match_info.get('period')
    sql = None

    if period == 'day':
        sql = "SELECT COUNT(*) FROM visits WHERE DATE(timestamp) = DATE('now')"
    elif period == 'month':
        sql = "SELECT COUNT(*) FROM visits WHERE strftime('%Y-%m', timestamp) = strftime('%Y-%m', 'now')"
    elif period == 'year':
        sql = "SELECT COUNT(*) FROM visits WHERE strftime('%Y', timestamp) = strftime('%Y', 'now')"
    elif period == 'total':
        sql = "SELECT COUNT(*) FROM visits"

    with conn:
        c.execute(sql)
        count = c.fetchone()[0]

    return web.Response(text=f"Number of visits this {period}: {count}")

async def get_unique_stats(request):
    period = request.match_info.get('period')

    sql = None
    if period == 'day':
        sql = "SELECT COUNT(DISTINCT ip || path) FROM visits WHERE DATE(timestamp) = DATE('now')"
    elif period == 'month':
        sql = "SELECT COUNT(DISTINCT ip || path) FROM visits WHERE strftime('%Y-%m', timestamp) = strftime('%Y-%m', 'now')"
    elif period == 'year':
        sql = "SELECT COUNT(DISTINCT ip || path) FROM visits WHERE strftime('%Y', timestamp) = strftime('%Y', 'now')"
    elif period == 'total':
        sql = "SELECT COUNT(DISTINCT ip || path) FROM visits"

    with conn:
        c.execute(sql)
        count = c.fetchone()[0]

    return web.Response(text=f"Number of unique visits this {period}: {count}")

app = web.Application()
app.router.add_get('/', handle)
app.router.add_get('/stats/{period}', get_stats)
app.router.add_get('/unistats/{period}', get_unique_stats)

if __name__ == '__main__':
    web.run_app(app)