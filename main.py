from website import create_app

if __name__ == '__main__':
    app = create_app()
    # Port 5000 is used by AirPlay Receiver on macOS, so default to 5001
    app.run(host='127.0.0.1', port=5001)