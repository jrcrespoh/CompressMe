from project import application

if __name__ == '__main__':
    application.config['TEMPLATES_AUTO_RELOAD'] = True
    application.run()
