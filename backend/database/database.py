import sqlite3

conn = sqlite3.connect('backend\database\it_support.db')
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
    ("incorrect credentials", "reset or reconfigure your login credentials."),
    ("software plugin is not installed", "identify and install the necessary plugin."),
    ("failed to update password", "attempt to change the password again or contact support."),
    ("printer is malfunctioning", "check for paper jams, ink levels, or error messages on the printer."),
    ("printer has run out of ink", "replace the ink cartridges."),
    ("sap server is currently down", "wait until the server is back up or contact IT support."),
    ("server is not responding", "check server status and restart if necessary."),
    ("new service request is needed", "submit a service request form to IT support."),
    ("network switch has failed", "inspect the switch and replace if necessary."),
    ("email not syncing", "check internet connection and sync settings."),
    ("vpn connection failed", "verify login credentials and server address."),
    ("hard drive is full", "delete unnecessary files or upgrade storage."),
    ("system overheating", "ensure proper ventilation and check if cooling fans are working."),
    ("forgotten password", "use the password recovery process to reset it."),
    ("frequent software crashes", "update the software and check for compatibility issues."),
    ("slow computer performance", "close unnecessary programs and clear cache."),
    ("mobile device not connecting to wifi", "ensure the correct password is used and restart the device."),
    ("unable to open a file", "check file format and compatibility with the software."),
    ("keyboard malfunction", "clean the keyboard or replace if necessary."),
    ("mouse not working", "check the mouse connection and replace batteries if wireless."),
    ("blue screen of death", "restart the computer and check for updates."),
    ("no sound from computer", "check sound settings and speakers/headphones connection."),
    ("video not playing", "update media player and check file format."),
    ("popup ads are frequent", "install ad blocker and scan for malware."),
    ("cannot print to network printer", "check network connection and printer settings."),
    ("lost data", "restore data from backup or use data recovery software."),
    ("duplicate ip address conflict", "renew IP address or set a static IP."),
    ("website not loading", "clear browser cache and check if the website is down."),
    ("firewall blocking application", "adjust firewall settings to allow the application."),
    ("outdated antivirus software", "update antivirus software and run a scan."),
    ("unauthorized access detected", "change passwords and review security settings."),
    ("wifi keeps dropping", "restart the router or move closer to it."),
    ("router setup issues", "refer to the router manual or contact support."),
    ("computer won't boot up", "check power supply and inspect hardware connections."),
    ("corrupted files", "restore the files from a backup or attempt repair."),
    ("low battery life on device", "reduce screen brightness and close unnecessary apps."),
    ("software needs reinstallation", "uninstall the software and install the latest version."),
    ("two-factor authentication failure", "sync device time or regenerate authentication code."),
    ("usb device not recognized", "try another USB port or restart the computer."),
    ("zoom meeting issues", "check audio/video settings and internet connectivity."),
    ("email attachment issues", "check size limits and file format restrictions."),
    ("data breach", "notify IT security and start an investigation."),
    ("file sharing not working", "check network permissions and sharing settings."),
    ("outdated network drivers", "download and install the latest network drivers."),
    ("cloud sync problems", "check cloud service status and connectivity."),
    ("application license expired", "renew the license or contact the software provider."),
    ("error codes on software", "consult the software documentation for troubleshooting."),
    ("insufficient user permissions", "request necessary permissions from the administrator.")
]

cursor.executemany('INSERT OR IGNORE INTO solutions (error, solution) VALUES (?, ?)', data)
conn.commit()
conn.close()
