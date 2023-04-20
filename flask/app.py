from flask import Flask, render_template
# import os

app = Flask(__name__)

@app.route('/')
def index():
   # os.system("pwd")
   return render_template('neo4j-browser.html')

if __name__ == '__main__':
   app.run()