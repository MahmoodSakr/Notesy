from website import create_app 

app = create_app()
ENV = "Production"
# ENV = "Development"
app.run(debug=False)

