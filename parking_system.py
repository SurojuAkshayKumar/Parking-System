 
# parking_system.py
from flask import Flask
from app.routes import pre_book

app = Flask(__name__)

# ... (your existing code)

# Register the pre-book blueprint
app.register_blueprint(pre_book)

if __name__ == "__main__":
    app.run(debug=True)
