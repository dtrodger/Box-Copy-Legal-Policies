import pprint

import click

import utils


NEW_FOLDER_ID = "123584148268"
LEGAL_HOLD_POLICY_ID = "2013223"


@click.command()
def list_legal_hold_policies():
    box_client = utils.get_box_client()
    policies = box_client.get_legal_hold_policies()
    for policy in policies:
        pprint.pprint(policy.response_object)


@click.command()
def get_legal_hold_policy():
    box_client = utils.get_box_client()
    legal_hold_policy = box_client.legal_hold_policy(LEGAL_HOLD_POLICY_ID).get()
    pprint.pprint(legal_hold_policy.response_object)


@click.command()
def list_legal_hold_policy_assignments():
    box_client = utils.get_box_client()
    legal_hold_policy_assignments = box_client.legal_hold_policy(LEGAL_HOLD_POLICY_ID).get_assignments()
    for assignment in legal_hold_policy_assignments:
        assignment_id = assignment.response_object["id"]
        assignment = box_client.legal_hold_policy_assignment(assignment_id).get()
        pprint.pprint(assignment.response_object)


@click.command()
def move_folder_under_hold():
    box_client = utils.get_box_client(as_user_email="drodgers+demo@boxdemo.com")
    policies = box_client.get_legal_hold_policies()
    for policy in policies:
        print(f"Found legal hold policy {policy}")
        legal_hold_policy_id = policy.response_object["id"]
        legal_hold_policy_assignments = box_client.legal_hold_policy(legal_hold_policy_id).get_assignments()
        assignments = []
        for assignment in legal_hold_policy_assignments:
            assignment_id = assignment.response_object["id"]
            assignment = box_client.legal_hold_policy_assignment(assignment_id).get()
            print(f"Found legal hold policy assignments {assignment}")
            assigned_to = assignment.response_object["assigned_to"]
            assigned_to["legal_hold_policy_id"] = legal_hold_policy_id
            assignments.append(assigned_to)

    for assignment in assignments:
        item_type = assignment["type"]
        item_id = assignment["id"]
        legal_hold_policy_id = assignment["legal_hold_policy_id"]
        if item_type == "folder":
            folder = box_client.folder(item_id)
            new_folder = box_client.folder(NEW_FOLDER_ID)
            copied_folder = folder.copy(new_folder)
            legal_hold_policy = box_client.legal_hold_policy(legal_hold_policy_id)
            legal_hold_policy.assign(copied_folder)
            print(f"Copied folder {folder} to {copied_folder} and assigned policy {legal_hold_policy}")


@click.group()
def cli() -> None:
    """
    Click application group to support multiple commands
    """
    pass


def main() -> None:
    """
    Main application function. Registers Click CLI commands to a group, then runs the Click application.
    """
    commands = [
        list_legal_hold_policies,
        get_legal_hold_policy,
        move_folder_under_hold,
        list_legal_hold_policy_assignments
    ]
    for command in commands:
        cli.add_command(command)

    cli()


if __name__ == "__main__":
    main()