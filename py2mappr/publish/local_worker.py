import os
import webbrowser
import socketserver
import http.server
from pathlib import Path


def local_worker(web_dir: Path, PORT=8080):
    # change to project directory where index.html and data folder are
    os.chdir(web_dir)

    # open new tab in browswer
    webbrowser.open_new_tab("http://localhost:" + str(PORT))

    Handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(
            "\nServing locally at port",
            PORT,
            "go to http://localhost:%s \nCTL_C to quit\n" % str(PORT),
        )
        httpd.serve_forever()
