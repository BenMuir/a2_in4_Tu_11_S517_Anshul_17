
import os
#connecting db to app
from beyblade import db_beyblade, create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)