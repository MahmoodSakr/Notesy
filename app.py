from website import create_app 

app = create_app()
ENV = "Production"
# ENV = "Development"

if __name__ == '__main__':
    if ENV == "Production":
        app.run(debug=False)
    elif ENV == "Development":
        app.run(debug=True,port=5000)