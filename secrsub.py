#!/usr/bin/env python3

#  _______  _______  _______  _______  _______           ______
# (  ____ \(  ____ \(  ____ \(  ____ )(  ____ \|\     /|(  ___ \
# | (    \/| (    \/| (    \/| (    )|| (    \/| )   ( || (   ) )
# | (_____ | (__    | |      | (____)|| (_____ | |   | || (__/ /
# (_____  )|  __)   | |      |     __)(_____  )| |   | ||  __ (
#       ) || (      | |      | (\ (         ) || |   | || (  \ \
# /\____) || (____/\| (____/\| ) \ \__/\____) || (___) || )___) )
# \_______)(_______/(_______/|/   \__/\_______)(_______)|/ \___/
#                         By MAAYTHM (https://github.com/MAAYTHM)

import os
import random
import re
import sys
import signal
import json
import time
from requests import Session
import traceback
from threading import Thread, active_count
from termcolor import colored


class Worker(Thread):
    # intializing Thread class and setting 'target_page'
    def __init__(self, target_page, domain):
        """
        Workers for parallel requests task
        """
        Thread.__init__(self)
        self.target_page = target_page
        self.apex_domain = domain

    # work of threads
    def run(self):
        global stop_loading_print, user_agents, rq_session, stop_threads, timeout

        # if 'stop_threads' set to True
        if stop_threads:
            return

        subdomain_url = (
            f"https://securitytrails.com/_next/data/local/list/apex_domain/{self.apex_domain}.json?query={self.apex_domain}&max_page=100&page="
            + str(self.target_page)
        )  # for fetching subdomains in one go

        resp = rq_session.get(
            subdomain_url,
            headers={"User-Agent": random.choice(user_agents)},
            timeout=timeout,
        )

        # uniq subdomains
        subdomains = set(
            [
                i["hostname"]
                for i in resp.json()["pageProps"]["apexDomainData"]["data"]["records"]
            ]
        )

        # if 'stop_threads' set to True
        if stop_threads:
            return

        stop_loading_print = True
        # printing actual subdomains
        for subdomain in subdomains:
            if subdomain and not subdomain.isspace():
                flushPrint(subdomain)
        stop_loading_print = False


def lock():
    """
    Lock main thread until all threads finished their work
    """

    # loader before any thread start
    loader(
        constant_string="Spawning Threads",
        temp_string='"." * index',
        loop_condition="not len(threads)",
        break_condition="stop_loading_print",
        reset_condition="(index-1) == max_index",
        max_index=3,
    )

    # loader after any thread start
    loader(
        constant_string="Threads Remaining -",
        temp_string="active_count()",
        reset_condition="stop_loading_print",
        loop_condition="True in [t.is_alive() for t in threads]",
    )


def loader(
    constant_string="",
    temp_string="",
    final_string="",
    loop_condition="",
    break_condition="",
    reset_condition="",
    max_index=0,
    time_gap=0.5,
):
    """
    Responsible for handling loading strings based on given conditions
    """
    global silent

    # I used the eval function, in order to run given conditions each time properly
    # in terms of 'temp_string', I used eval becoz i need to change this string content each time thats why it is 'temp_string'

    # If 'user' used 'silent flag "-s"', then 'loader' will not print anything
    if not silent:
        index = 1
        while eval(loop_condition):
            loading_string = f"{constant_string} {eval(temp_string)}"
            flushPrint(loading_string, end="\r")
            time.sleep(time_gap)

            # increasing index value if max_index is given
            if max_index:
                index += 1

            # resetting index value
            if (index - 1) == max_index:
                index = 1

            # overwriting above print
            if reset_condition and eval(reset_condition):
                flushPrint(" " * len(loading_string), end="\r")

            # breaking condition
            if break_condition and eval(break_condition):
                break

        # for removing any above remaining line
        flushPrint(" " * (len(constant_string) + 5), end="\r")

        # print final words
        if final_string and not final_string.isspace():
            flushPrint(eval(final_string), end="\r")
            time.sleep(time_gap)


def wait_till():
    """
    Wait for prev threads to finish
    """
    global threads

    while True in [t.is_alive() for t in threads]:
        pass

    # clearing threads list after this
    threads.clear()


def handler(signum, frame):
    """
    Handling Ctrl-C signals
    """
    global stop_threads, threads

    stop_threads = True
    [t.join() for t in threads]  # waiting to finish up threads
    sys.exit(1)


def help_():
    """
    Print the help information
    """
    global fileName

    msg = f"""
a small python3 wrapper tool around 'https://securitytrails.com/' website to find subdomains
- By MAAYTHM (https://github.com/MAAYTHM)

Flags :-
    * -h  --help      Print this help message.
    * -f  --file      Take input from file (.txt).
    * -t  --timeout   Timeout for requests (in seconds) (default: 10 seconds).
    * -v  --verbose   Verbose mode for detailed error messages.
    * -q  --quiet     Silent mode (Only print subdomains/error messages).
    * --conf          Path to file which contains credentials for 'https://securitytrails.com/' (.json) (default - './secrsub.json').
    * --verify        Verify the credentials for 'https://securitytrails.com/'

Examples :-
    * python3 {fileName} -h
    * python3 {fileName} -f anyfile.txt
    * echo 'anything' | python3 {fileName} -

Note :-
    * If you want to give input from stdin then checkout example number 3 (above).
    * Export / Save email address and password of securitytrails website (https://securitytrails.com/app/auth/login) in 'secrsub.json'.
    * If stacktrace is not shown while using '-v', then it means the error is explained only with the single line printed with '[-] Error'.
"""
    print_banner()
    flushPrint(msg)
    sys.exit()


def flushPrint(*a, end="\n"):
    """
    Print output with 'flush=True', means print as unbuffered output which can be reused with pipes.
    """
    if a and not str(a).isspace():
        print(*a, flush=True, end=end)


def print_banner():
    """
    Print tool Banner
    """
    global banner_printed

    banner = """
.d8888. d88888b  .o88b. d8888b. .d8888. db    db d8888b. 
88'  YP 88'     d8P  Y8 88  `8D 88'  YP 88    88 88  `8D 
`8bo.   88ooooo 8P      88oobY' `8bo.   88    88 88oooY' 
  `Y8b. 88~~~~~ 8b      88`8b     `Y8b. 88    88 88~~~b. 
db   8D 88.     Y8b  d8 88 `88. db   8D 88b  d88 88   8D 
`8888Y' Y88888P  `Y88P' 88   YD `8888Y' ~Y8888P' Y8888P'
    """

    footer = "                        By MAAYTHM (https://github.com/MAAYTHM)"

    colors = {
        "red": "blue",
        "green": "magenta",
        "blue": "yellow",
        "yellow": "cyan",
        "magenta": "green",
        "cyan": "red",
    }
    # random color choosing
    color = random.choice(list(colors.keys()))

    # printing banner
    print(colored(banner, color=color), end="")
    print(
        colored(footer, color=colors[color]),
    )

    # setting 'banner_printed' to True, means now there is no need to print banner again
    banner_printed = True


def error(errorMsg=""):
    """
    Print error messages.
    """
    global verbose, stop_loading_print, stop_threads, banner_printed

    # if tool banner not printed still, print it
    if not banner_printed:
        print_banner()

    print()
    # if verbose mode is enabled then print whole stack trace
    if verbose:
        flushPrint(traceback.format_exc())

    elif errorMsg and not str(errorMsg).isspace():
        print(colored(f"[-] Error, {errorMsg} !!!", "red", attrs=["reverse", "bold"]))

    stop_threads = stop_loading_print = True
    sys.exit(1)


def pipeInput():
    """
    Extracting domains from pipe
    """
    global domains

    for domain in sys.stdin:
        domain = domain.splitlines()[0]
        if type(domain) != list:
            domain = [domain]

        domains.extend(domain)


def fileInput(name):
    """
    Extracting domains from file
    """
    global domains

    with open(name, "r") as f:
        domains = f.read().splitlines()

    # verify domain names
    domains = list(set(domains))


def verify_domains():
    """
    Verify domain with regex pattern
    """
    global domains, stadalone_flags

    for domain in domains:
        if not re.findall(".*\.[a-z]+$", domain) and domain not in stadalone_flags:
            error(
                errorMsg="Invalid Domain Name: " + colored(" " + domain + " ", "blue")
            )


def verify_creds():
    """
    for checking if user given email and pass for securitytrails website and these creds are right or not
    """
    global conf_file, rq_session, user_agents, stop_threads, timeout, dispose_string, threads

    try:

        thread = Thread(
            target=loader,
            kwargs={
                "constant_string": "Verifying Credentials",
                "temp_string": "'.' * index",
                "final_string": "dispose_string",
                "loop_condition": "not stop_threads",
                "reset_condition": "(index - 1) == max_index",
                "max_index": 3,
                "time_gap": 0.3,
            },
        )
        threads.append(thread)
        thread.start()

        u_email = json.load(open(conf_file, "r"))["email"]
        u_pass = json.load(open(conf_file, "r"))["pass"]
        data = {"email": u_email, "password": u_pass}
        login_url = "https://securitytrails.com/api/auth/login"
        dispose_string = colored(
            "[+] Credentials Verified", "green", attrs=["reverse", "bold"]
        )

        # response from securitytrails server for login
        resp = rq_session.post(
            login_url,
            data=data,
            headers={"User-Agent": random.choice(user_agents)},
            timeout=timeout,
        )

        # if credentials are wrong
        if not resp.status_code == 200 or not resp.json()["success"]:
            dispose_string = colored(
                "[-] Credentials not valid", "red", attrs=["reverse", "bold"]
            )
            return False

        return True

    except:
        error(errorMsg="Invalid credentials for securitytrails")


def main():
    """
    Main function which is responsible for getting subdomain from securitytrails website
    """
    global domains, rq_session, user_agents, stop_threads, stop_loading_print

    try:
        # resetting 'stop_threads' variable (just to ensure)
        stop_threads = False

        for domain in domains:
            subdomain_url = f"https://securitytrails.com/_next/data/local/list/apex_domain/{domain}.json?query={domain}&max_page=100&page=1"  # for fetching total number of subdomains
            resp = rq_session.get(
                subdomain_url, headers={"User-Agent": random.choice(user_agents)}
            )

            # total number of pages to get subdomains from securitytrails
            total_pages = resp.json()["pageProps"]["apexDomainData"]["data"]["meta"][
                "total_pages"
            ]

            # uniq subdomains from above 1st request
            subdomains = set(
                [
                    i["hostname"]
                    for i in resp.json()["pageProps"]["apexDomainData"]["data"][
                        "records"
                    ]
                ]
            )

            flushPrint("\n".join(subdomains))

            # for stopping loading_string, if total_pages is less than or equal to 1
            if total_pages <= 1:
                stop_loading_print = True

            # starting threads pages from '2 to total_pages'
            for page_number in range(2, total_pages + 1):
                thread = Worker(target_page=page_number, domain=domain)
                threads.append(thread)
                thread.start()

            # lock main thread until all threads finished
            lock()

    except SystemExit:
        pass

    except:
        error(errorMsg=f"While Connecting with Securitytrails")


if __name__ == "__main__":

    # for handling ctrl+c keyboard interrupt
    signal.signal(signal.SIGINT, handler)

    # If SIGPIPE is not available, then we dont have to do anything to ignore 'Broken Pipe'
    try:
        signal.signal(signal.SIGPIPE, signal.SIG_DFL)  # for 'broken pipe' error
    except:
        pass

    try:
        # taking cmdline arguments
        arguments = []
        arguments.extend(sys.argv[1:])

        # some global variables space
        Author = "MAAYTHM"
        GithubUrl = "https://github.com/MAAYTHM/"
        fileName = sys.argv[0].split("/")[-1].split("\\")[-1]
        stadalone_flags = [
            "-h",
            "--help",
            "?",
            "--verify",
        ]  # flags to remove from checking in 'verify_domains' function
        dispose_string = ""  # disposable variable just to use to transfer one value to another function
        banner_printed = False  # true if tool banner already printed
        verbose = False
        silent = False  # for suppressing banner print
        only_verify = False  # only run 'verify_creds' function if it is True
        conf_file = "secrsub.json"
        rq_session = Session()
        domains = []
        threads = []  # contain threads variables
        stop_loading_print = (
            False  # for stop printing 'loading_string' in lock function
        )
        stop_threads = False  # for stopping threads after any error or interruption
        timeout = 10  # timeout for requests in seconds
        user_agents = [
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/37.0.2062.94 Chrome/37.0.2062.94 Safari/537.36",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36",
            "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko",
            "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/600.8.9 (KHTML, like Gecko) Version/8.0.8 Safari/600.8.9",
            "Mozilla/5.0 (iPad; CPU OS 8_4_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12H321 Safari/600.1.4",
            "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.10240",
            "Mozilla/5.0 (Windows NT 6.3; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0",
            "Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko",
            "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36",
            "Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko",
            "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_4) AppleWebKit/600.7.12 (KHTML, like Gecko) Version/8.0.7 Safari/600.7.12",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:40.0) Gecko/20100101 Firefox/40.0",
        ]

        # error if user doesnt provided any arguments
        if len(arguments) == 0:
            error("No input provided")

        # if arguments are given
        else:

            # if user used '-q'
            if "-q" in arguments:
                silent = True

            # check if user used any help flag
            if "-h" in arguments or "?" in arguments or "--help" in arguments:
                help_()

            # if user used "--conf" flag,
            try:
                if "--conf" in arguments:
                    conf_file = arguments[arguments.index("--conf") + 1]

                # checking if file exists
                if os.path.isfile(conf_file):
                    pass

                # checking in this script file location
                elif os.path.isfile(
                    os.path.join(os.path.abspath(os.path.dirname(__file__)), conf_file)
                ):
                    conf_file = os.path.join(
                        os.path.abspath(os.path.dirname(__file__)), conf_file
                    )

                else:
                    raise Exception(
                        "Config File not exists"
                    )  # -> Config File not exists

            except:
                error(errorMsg=f"Invalid/Empty configuration file")

            # if verbose mode is enabled by user,
            if "-v" in arguments:
                verbose = True

            # if user specified "--verify" flag
            if "--verify" in arguments:
                only_verify = True

            # if user given timeout as '-t'
            if "-t" in arguments:
                try:
                    if "-t" in arguments:
                        timeout = int(arguments[arguments.index("-t") + 1])
                    else:
                        timeout = int(arguments[arguments.index("--timeout") + 1])
                except:
                    error("Invalid Timeout value")

            # if file flag is used
            if "-f" in arguments or "--file" in arguments:
                try:
                    if "-f" in arguments:
                        Input_filename = arguments[arguments.index("-f") + 1]
                    else:
                        Input_filename = arguments[arguments.index("--file") + 1]

                    # checking if file exists?
                    if not os.path.isfile(Input_filename):
                        raise Exception(
                            "Input File not exists"
                        )  # ->  Input File not exists

                    # extracting urls from file
                    fileInput(Input_filename)

                except:
                    error(errorMsg=f"Input File not found")

            # if user used "-" in argument, then take input from pipe/stdin
            elif "-" in arguments:
                pipeInput()

            # if none of the above condition run, then it means user is giving input simply like (example.py example)
            else:
                domains.extend(arguments)

            if not silent:
                print_banner()

            # verifying domain names with regex patterns
            verify_domains()

            # for checking if user given email and pass for securitytrails website and these creds are right or not
            verified = verify_creds()
            stop_threads = True  # to finish the work of prev thread
            wait_till()  # wait till prev thread is finished

            # if user creds verified, then run main function
            if verified and not only_verify:
                print(
                    " " * (len(dispose_string) + 5) + "\n", end="\r"
                )  # to remove dispose string
                main()

            else:
                print()  # to not remove dispose_string

        # session close
        rq_session.close()

    # Handling exceptions
    except Exception as errors:
        error(errors)
