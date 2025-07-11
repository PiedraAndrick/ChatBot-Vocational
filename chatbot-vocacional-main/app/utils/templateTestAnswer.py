
def templateTest(infoMalla, infoPerfil, nombre):
    return f'''
    <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; margin: 0; padding: 0; background-color: #f6f6f6;">
        <div style="max-width: 600px; margin: 20px auto; padding: 20px; background-color: #ffffff; border: 1px solid #dddddd; border-radius: 10px;">
            <h1 style="color: #333333; text-align: center;">Hola {nombre}</h1>
            <p style="color: #555555; font-size: 16px;">
            {infoMalla}
            </p>      
            <h2 style="color: #333333; border-bottom: 2px solid #dddddd; padding-bottom: 5px;">Perfil de Egreso</h2>
            <p style="color: #555555; font-size: 16px;">
            <a href="{infoPerfil}" style="color: #1a73e8; text-decoration: none;">{infoPerfil}</a>
            </p>
        </div>
        </body>
    </html>
    '''

def templateTest2(infoMalla, infoPerfil, nombre,infoMalla2, infoPerfil2 ):
    return f'''
    <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; margin: 0; padding: 0; background-color: #f6f6f6;">
        <div style="max-width: 600px; margin: 20px auto; padding: 20px; background-color: #ffffff; border: 1px solid #dddddd; border-radius: 10px;">
            <h1 style="color: #333333; text-align: center;">Hola {nombre}</h1>
            <p style="color: #555555; font-size: 16px;">
            {infoMalla}
            </p>      
            <h2 style="color: #333333; border-bottom: 2px solid #dddddd; padding-bottom: 5px;">Perfil de Egreso</h2>
            <p style="color: #555555; font-size: 16px;">
            <a href="{infoPerfil}" style="color: #1a73e8; text-decoration: none;">{infoPerfil}</a>
            </p>
        </div>
        <div style="max-width: 600px; margin: 20px auto; padding: 20px; background-color: #ffffff; border: 1px solid #dddddd; border-radius: 10px;">
            <p style="color: #555555; font-size: 16px;">
            {infoMalla2}
            </p>      
            <h2 style="color: #333333; border-bottom: 2px solid #dddddd; padding-bottom: 5px;">Perfil de Egreso</h2>
            <p style="color: #555555; font-size: 16px;">
            <a href="{infoPerfil2}" style="color: #1a73e8; text-decoration: none;">{infoPerfil2}</a>
            </p>
        </div>
        </body>
    </html>
    '''
#info malla, perfil de egreso