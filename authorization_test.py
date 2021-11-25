import os
import requests


# définition de l'adresse de l'API
api_address = "fastapi"
# port de l'API
api_port = 8000

# définition de l'username
api_username = os.environ.get("USER_NAME").split(':')
# définition du mot de passe
api_password = os.environ.get("PASSWORD").split(':')
# définition de la version
version = os.environ.get("VERSION").split(':')
# définition de la phrase
sentence = "It's a test sentence"
# définition du resultat attendu
expected_result = os.environ.get("EXPECTED_RESULT").split(':')

# itération pour les tests d'authorisation
i = 0
for u, p in zip(api_username, api_password):
    for v in version:
        # requête
        r = requests.get(
            url=f'http://{api_address}:{api_port}/{v}/sentiment',
            params= {
                'username': f'{u}',
                'password': f'{p}',
                'sentence': f'{sentence}'
            }
        )

        # statut de la requête
        status_code = r.status_code

        # affichage des résultats
        if status_code == int(expected_result[i]):
            test_status = 'SUCCESS'
        else:
            test_status = 'FAILURE'

        # Affichage du test
        output = f'''
    ============================
        Authorization test
    ============================

    request done at "/{v}/sentiment"
    | username="{u}"
    | password="{p}"

    expected result = {expected_result[i]}
    actual restult = {status_code}

    ==>  {test_status}

    '''
        print(output)

        # impression dans un fichier
        if os.environ.get('LOG') == '1':
            with open('./log/api_test.log', 'a') as file:
                file.write(output)

        i += 1
