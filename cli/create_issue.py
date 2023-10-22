# create issue

import click
import requests
from decouple import config

"""
https://docs.github.com/en/rest/reference/issues#create-an-issue
python cli/create_issue.py \
--title='' \
--body='' \
--labels='feature'
"""


# repositorio para adicionar o issue
REPO_OWNER = config("REPO_OWNER")
REPO_NAME = config("REPO_NAME")
TOKEN = config("TOKEN")


def write_file(filename, number, title, description, labels):
    labels = " ,".join(labels).strip()
    with open(filename, "a") as f:
        f.write(f"\n---\n\n")
        f.write(f"[ ] - {number} - {title}\n")
        f.write(f"    {labels}\n\n")

        if description:
            f.write(f"    \n\n")
        f.write(
            f'    make lint; git add .; git -m commit "{title} close #{number}"; git push\n'
        )


@click.command()
@click.option("--title", prompt="Title", help="Digite o Titulo.")
@click.option("--body", prompt="Description", help="Digite a descrição.")
# @click.option('--assignee', prompt='Assignee', help='Digite a pessoa a ser associada.') # noqa E501
@click.option("--labels", prompt="Labels", help="Digite as labels.")
def make_github_issue(title, body=None, assignee=None, milstone=None, labels=None):
    """
    Cria issue no github.com
    """

    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/issues"
    headers = {"Authorization": f"token {TOKEN}"}
    labels = labels.split(",")

    # Cria issue

    issue = {
        "title": title,
        "body": body,
        "labels": labels,
    }

    if assignee:
        issue[assignees] = [assignee]

    # Adiciona issue no repositorio

    req = requests.post(url, headers=headers, json=issue)

    if req.status_code == 201:
        print(f'Successfully created Issue "{title}".')
        number = req.json()["number"]
        description = body

        filename = "/home/luiz.cruz/tarefas.txt"

        write_file(filename, number, title, description, labels)
    else:
        print(f'Could not create Issue "{title}".')


if __name__ == "__main__":
    make_github_issue()
