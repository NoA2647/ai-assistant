import subprocess

WORDS = ["search", "network"]

PRIORITY = 2


def execute(cmd):
    popen = subprocess.Popen(cmd, stdout=subprocess.PIPE, universal_newlines=True)
    for stdout_line in iter(popen.stdout.readline, ""):
        yield stdout_line
    popen.stdout.close()
    return_code = popen.wait()
    if return_code:
        raise subprocess.CalledProcessError(return_code, cmd)


def run(command, speaker, profile, mapper):
    users = ["yourself"]
    for path in execute("sudo nmap -sn 192.168.1.0/24".split(" ")):
        print(path, end="")
        if 'MAC' in path:
            user = path.split('(')[-1]
            users.append(user[:-2])

    result = f"number of users is {len(users)} ,and users are:"
    for user in users:
        result += f"\n{user}"
    print(result)
    speaker.say(result)


def isValid(command):
    return bool(all(word in command for word in WORDS))
