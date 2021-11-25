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
sentence = os.environ.get("SENTENCE").split(':')
# définition du resultat attendu
expected_result = os.environ.get("EXPECTED_RESULT").split(':')


# itération pour les tests d'authorisation
for u, p in zip(api_username, api_password):
    for v in version:
        for s, e in zip(sentence, expected_result):
            # requête
            r = requests.get(
                url=f'http://{api_address}:{api_port}/{v}/sentiment',
                params= {
                    'username': f'{u}',
                    'password': f'{p}',
                    'sentence': f'{s}'
                }
            )

            # score de la requête
            score = r.json()["score"]
            if score >= 0 :
                score_result = "POSITIF"
            else:
                score_result = "NEGATIF"

            # affichage des résultats
            if score_result == e:
                test_status = 'SUCCESS'
            else:
                test_status = 'FAILURE'

            # Affichage du test
            output = f'''
    ============================
            Content test
    ============================

    request done at "/{v}/sentiment"
    | username="{u}"
    | password="{p}"
    | sentence="{s}"

    expected result = {e}
    actual restult = {score_result}

    ==>  {test_status}

    '''
            print(output)

            # impression dans un fichier
            if os.environ.get('LOG') == '1':
                with open('./log/api_test.log', 'a') as file:
                    file.write(output)
