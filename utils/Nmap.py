import subprocess

WORDS = ["اسکن", "شبکه"]

PRIORITY = 2


def execute(cmd):
    popen = subprocess.Popen(cmd, stdout=subprocess.PIPE, universal_newlines=True)
    for stdout_line in iter(popen.stdout.readline, ""):
        yield stdout_line
    popen.stdout.close()
    return_code = popen.wait()
    if return_code:
        raise subprocess.CalledProcessError(return_code, cmd)


def run(command, iom, profile, mapper):
    # users = ["خودت"]
    i=0
    for path in execute("nmap -sn 192.168.10.0/24".split(" ")):
        print(path, end="")
        if 'Host' in path:
            i+=1
            # user = path.split('(')[-1]
            # users.append(user[:-2])

    result = f"تعداد کاربران پیدا شده: {i} تا"
    # for user in users:
    #     result += f"\n{user}"
    # print(result)
    iom.getSpeaker().say(result)


def isValid(command):
    return bool(all(word in command for word in WORDS))
