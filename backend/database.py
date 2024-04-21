import sqlite3

conn = sqlite3.connect('it_support.db')
cursor = conn.cursor()

cursor.execute('''
DROP TABLE IF EXISTS solutions 
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS solutions (
    error TEXT PRIMARY KEY,
    solution TEXT NOT NULL
)
''')

data = [
    ("hardware malfunction", "check warranty and seek repairs."),
    ("cable connection lost", "check and reconnect cables."),
    ("device driver outdated", "update driver from manufacturer's website."),
    ("incorrect credentials are", "reset or reconfigure your login credentials."),
    ("software plugin is not installed", "identify and install the necessary plugin."),
    ("failed to update password", "attempt to change the password again or contact support."),
    ("printer is malfunctioning", "check for paper jams, ink levels, or error messages on the printer."),
    ("printer has run out of ink", "replace the ink cartridges."),
    ("sap server is currently down", "wait until the server is back up or contact IT support."),
    ("server is not responding", "check server status and restart if necessary."),
    ("new service request is needed", "submit a service request form to IT support."),
    ("network switch has failed", "inspect the switch and replace if necessary.")
]

cursor.executemany('INSERT OR IGNORE INTO solutions (error, solution) VALUES (?, ?)', data)
conn.commit()
conn.close()
