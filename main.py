from beyblade import create_app

app = create_app()

if __name__ == '__main__':
    # host='0.0.0.0' exposes WSL to Windows, port=5001 avoids Windows conflicts
<<<<<<< HEAD
    app.run(debug=True, host='0.0.0.0', port=5001)




=======
    app.run(debug=True, host='0.0.0.0', port=5001)
>>>>>>> f86cab5e2b542268c0820e7dad9c237b999423a0
