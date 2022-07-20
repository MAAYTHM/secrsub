## Whats use of this tool?
To get subdomains from [SecurityTrails](https://securitytrails.com/). As there is no api endpoint, it uses valid credentials to login and then get subdomains.

## Why secrsub?
To simply bypass api limit of [SecurityTrails](https://securitytrails.com/).

## Requirement?
* python 3.x
* [SecurityTrails](https://securitytrails.com/) Credentials `email`&`password`.

## Installation
```bash
git clone https://github.com/MAAYTHM/secrsub.git
cd secrsub
```
* EITHER
```bash
pip3 install -r requirements.txt
python3 secrsub.py -h
```
* OR
```bash
pip install -r requirements.txt
python secrsub.py -h
```

## Help Banner
```bash
$ python secrsub.py -h

.d8888. d88888b  .o88b. d8888b. .d8888. db    db d8888b. 
88'  YP 88'     d8P  Y8 88  `8D 88'  YP 88    88 88  `8D 
`8bo.   88ooooo 8P      88oobY' `8bo.   88    88 88oooY' 
  `Y8b. 88~~~~~ 8b      88`8b     `Y8b. 88    88 88~~~b. 
db   8D 88.     Y8b  d8 88 `88. db   8D 88b  d88 88   8D 
`8888Y' Y88888P  `Y88P' 88   YD `8888Y' ~Y8888P' Y8888P'
                            By MAAYTHM (https://github.com/MAAYTHM)

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
    * python3 secrsub.py -h
    * python3 secrsub.py -f anyfile.txt
    * echo 'anything' | python3 secrsub.py -

Note :-
    * If you want to give input from stdin then checkout example number 3 (above).
    * Export / Save email address and password of securitytrails website (https://securitytrails.com/app/auth/login) in 'secrsub.json'.
    * If stacktrace is not shown while using '-v', then it means the error is explained only with the single line printed with '[-] Error'.
```

## Saving Credentials
* For using this tool, **Valid credentials** are needed which you can get by creating an account on [securityTrails](https://securitytrails.com/app/signup).
* Then enter your credentials in `secrsub.json` or create your own `custom_name.json`.
* The config JSON file should follow this format :
```python
{
    "email":"youremail@yahoo.com",
    "pass":"yourPassw0rd"
}
```
* **After saving** your credentials in proper `config file`, You can use this tool with only `--verify` flag to check that **creds are valid**.
```bash
python3 secrsub.py --verify
```

## Few Examples
> **Simple Input**
```bash
python3 secrsub.py example.com
```
![1.png](https://github.com/MAAYTHM/secrsub/raw/main/images/1.png)

> **File Input**
```bash
echo example.com | python3 secrsub.py -
```
![3.png](https://github.com/MAAYTHM/secrsub/raw/main/images/3.png)

> **Pipe Input**
```bash
python3 secrsub.py --verify
```
![2.png](https://github.com/MAAYTHM/secrsub/raw/main/images/2.png)

## Last Note
* Ignore any error like :
```diff
- safeurl 0.0.7 requires requests==2.7.0, but you have requests 2.28.1 which is incompatible.
```
* All issues / updates suggestion are welcomed.

## Disclaimer
The developer assumes no liability and is not responsible for any misuse or damage caused by this program. Please use responsibly.
