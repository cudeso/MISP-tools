"""Helper methods."""
from logging import Logger
from ._version import __version__ as MISP_IMPORT_VERSION

try:
    from pymisp import MISPObject, MISPAttribute
except ImportError as no_pymisp:
    raise SystemExit(
        "The PyMISP package must be installed to use this program."
        ) from no_pymisp

def gen_indicator(indicator, tag_list) -> MISPObject or MISPAttribute:
    """Create the appropriate MISP event object for the indicator (based upon type)."""
    if not indicator.get('type') or not indicator.get('indicator'):
        return False

    indicator_type = indicator.get('type')
    indicator_value = indicator.get('indicator')
    indicator_first = indicator.get("published_date", 0)
    indicator_last = indicator.get("last_updated", 0)
    # Type, Object_Type, Attribute Name
    ind_objects = [
        # ["hash_md5", "file", "md5"],
        # ["hash_sha256", "file", "sha256"],
        # ["hash_sha1", "file", "sha1"],
        # ["file_name", "file", "filename"],
        # ["mutex_name", "mutex", "name"],
        ["password", "credential", "password"],
        # ["url", "url", "url"],
        # ["email_address", "email", "reply-to"],
        ["username", "credential", "username"],
        # ["bitcoin_address", "btc-transaction", "btc-address"],
        # ["registry", "registry-key", "key"],
        ["x509_serial", "x509", "serial-number"],
        # ["file_path", "file", "fullpath"],
        # ["email_subject", "email", "subject"],
        # ["coin_address", "coin-address", "address"],
        ["x509_subject", "x509", "subject"],
        #["device_name", "device", "name"],
        # ["hash_imphash", "pe", "imphash"]
    ]

    for ind_obj in ind_objects:
        if indicator_type == ind_obj[0]:
            indicator_object = MISPObject(ind_obj[1])
            att = indicator_object.add_attribute(ind_obj[2], indicator_value)
            if indicator_first:
                att.first_seen = indicator_first
            if indicator_last:
                att.last_seen = indicator_last
            att.add_tag(f"CrowdStrike:indicator:type: {ind_obj[2].upper()}")
            for tag in tag_list:
                att.add_tag(tag)

            return indicator_object

    # Type, Category, Attribute Type
    ind_attributes = [
        ["hash_md5", "Artifacts dropped", "md5"],
        ["hash_sha256", "Artifacts dropped", "sha256"],
        ["hash_sha1", "Artifacts dropped", "sha1"],
        ["hash_imphash", "Artifacts dropped", "imphash"],
        ["file_name", "Artifacts dropped", "filename"],
        ["file_path", "Payload delivery", "filename"],
        ["url", "Network activity", "url"],
        ["mutex_name", "Artifacts dropped", "mutex"],
        ["bitcoin_address", "Financial fraud", "btc"],
        ["coin_address", "Financial fraud", "bic"],
        ["email_address", "Payload delivery", "email-reply-to"],
        ["email_subject", "Payload delivery", "email-subject"],
        ["registry", "Persistence mechanism", "regkey"],
        ["device_name", "Targeting data", "target-machine"],
        ["domain", "Network activity", "domain"],
        ["campaign_id", "Attribution", "campaign-id"],
        ["ip_address", "Network activity", "ip-src"],
        ["service_name", "Artifacts Dropped", "windows-service-name"],
        ["user_agent", "Network activity", "user-agent"],
        ["port", "Network activity", "port"]
    ]

    for ind_att in ind_attributes:
        if indicator_type == ind_att[0]:
            indicator_attribute = MISPAttribute()
            indicator_attribute.category = ind_att[1]
            indicator_attribute.type = ind_att[2]
            indicator_attribute.value = indicator_value

            return indicator_attribute

    return False


def thousands(int_to_format: int):
    return f"{int_to_format:,}"


def format_seconds(val: int):
    parts = str(float(val)).split(".")
    front = thousands(int(parts[0]))
    back = f"{parts[1]:.2}"
    return ".".join([front, back])


def two_decimals(float_to_format: float):
    return f"{float_to_format:.2}"


def confirm_boolean_param(val: str or bool) -> bool:
    returned = False
    if "T" in str(val).upper():
        returned = True

    return returned


def display_banner(banner: str = None,
                   logger: Logger = None,
                   fallback: str = None,
                   hide_cool_banners: bool = False  # ASCII r00lz!
                   ):
    """Logging helper to handle banner disablement."""
    if banner and logger:
        if not hide_cool_banners:
            for line in banner.split("\n"):
                logger.info(line, extra={"key": ""})
        else:
            if fallback:
                logger.info(fallback, extra={"key": ""})
    

# These are here because I didn't want us to have to import pyFiglet
ADVERSARIES_BANNER = """
  ____  ___    __ __    ___  ____    _____  ____  ____   ____    ___  _____
 /    T|   \  |  T  |  /  _]|    \  / ___/ /    T|    \ l    j  /  _]/ ___/
Y  o  ||    \ |  |  | /  [_ |  D  )(   \_ Y  o  ||  D  ) |  T  /  [_(   \_
|     ||  D  Y|  |  |Y    _]|    /  \__  T|     ||    /  |  | Y    _]\__  T
|  _  ||     |l  :  !|   [_ |    \  /  \ ||  _  ||    \  |  | |   [_ /  \ |
|  |  ||     | \   / |     T|  .  Y \    ||  |  ||  .  Y j  l |     T\    |
l__j__jl_____j  \_/  l_____jl__j\_j  \___jl__j__jl__j\_j|____jl_____j \___j
"""

INDICATORS_BANNER = """
 ____  ____   ___    ____    __   ____  ______   ___   ____    _____
l    j|    \ |   \  l    j  /  ] /    T|      T /   \ |    \  / ___/
 |  T |  _  Y|    \  |  T  /  / Y  o  ||      |Y     Y|  D  )(   \_
 |  | |  |  ||  D  Y |  | /  /  |     |l_j  l_j|  O  ||    /  \__  T
 |  | |  |  ||     | |  |/   \_ |  _  |  |  |  |     ||    \  /  \ |
 j  l |  |  ||     | j  l\     ||  |  |  |  |  l     !|  .  Y \    |
|____jl__j__jl_____j|____j\____jl__j__j  l__j   \___/ l__j\_j  \___j
"""
REPORTS_BANNER = """
 ____     ___  ____    ___   ____  ______  _____
|    \   /  _]|    \  /   \ |    \|      T/ ___/
|  D  ) /  [_ |  o  )Y     Y|  D  )      (   \_
|    / Y    _]|   _/ |  O  ||    /l_j  l_j\__  T
|    \ |   [_ |  |   |     ||    \  |  |  /  \ |
|  .  Y|     T|  |   l     !|  .  Y |  |  \    |
l__j\_jl_____jl__j    \___/ l__j\_j l__j   \___j
"""
MISP_BANNER = f"""
'##::::'##:'####::'######::'########:::::'########::'#######:::'#######::'##::::::::'######::
 ###::'###:. ##::'##... ##: ##.... ##::::... ##..::'##.... ##:'##.... ##: ##:::::::'##... ##:
 ####'####:: ##:: ##:::..:: ##:::: ##::::::: ##:::: ##:::: ##: ##:::: ##: ##::::::: ##:::..::
 ## ### ##:: ##::. ######:: ########:::::::: ##:::: ##:::: ##: ##:::: ##: ##:::::::. ######::
 ##. #: ##:: ##:::..... ##: ##.....::::::::: ##:::: ##:::: ##: ##:::: ##: ##::::::::..... ##:
 ##:.:: ##:: ##::'##::: ##: ##:::::::::::::: ##:::: ##:::: ##: ##:::: ##: ##:::::::'##::: ##:
 ##:::: ##:'####:. ######:: ##:::::::::::::: ##::::. #######::. #######:: ########:. ######::
..:::::..::....:::......:::..:::::::::::::::..::::::.......::::.......:::........:::......:::
           _____
            /  '
         ,-/-,__ __
        (_/  (_)/ (_
                     _______                        __ _______ __        __ __
                    |   _   .----.-----.--.--.--.--|  |   _   |  |_.----|__|  |--.-----.
                    |.  1___|   _|  _  |  |  |  |  _  |   1___|   _|   _|  |    <|  -__|
                    |.  |___|__| |_____|________|_____|____   |____|__| |__|__|__|_____|
                    |:  1   |                         |:  1   |
                    |::.. . |                         |::.. . |  Threat Intelligence v{MISP_IMPORT_VERSION}
                    `-------'                         `-------'
"""
DELETE_BANNER = """
______  _______        _______ _______ _______
|     \ |______ |      |______    |    |______
|_____/ |______ |_____ |______    |    |______
"""
IMPORT_BANNER = """
_____ _______  _____   _____   ______ _______
  |   |  |  | |_____] |     | |_____/    |
__|__ |  |  | |       |_____| |    \_    |
"""
CONFIG_BANNER = """
_______ _     _ _______ _______ _     _      _______  _____  __   _ _______ _____  ______
|       |_____| |______ |       |____/       |       |     | | \  | |______   |   |  ____
|_____  |     | |______ |_____  |    \_      |_____  |_____| |  \_| |       __|__ |_____|
"""
FINISHED_BANNER = r"""
 _______  __  .__   __.  __       _______. __    __   _______  _______
|   ____||  | |  \ |  | |  |     /       ||  |  |  | |   ____||       \
|  |__   |  | |   \|  | |  |    |   (----`|  |__|  | |  |__   |  .--.  |
|   __|  |  | |  . `  | |  |     \   \    |   __   | |   __|  |  |  |  |
|  |     |  | |  |\   | |  | .----)   |   |  |  |  | |  |____ |  '--'  |
|__|     |__| |__| \__| |__| |_______/    |__|  |__| |_______||_______/
"""
CHECKS_PASSED = r"""
____ _  _ ____ ____ _  _ ____    ___  ____ ____ ____ ____ ___
|    |__| |___ |    |_/  [__     |__] |__| [__  [__  |___ |  \
|___ |  | |___ |___ | \_ ___]    |    |  | ___] ___] |___ |__/
"""
CHECKS_FAILED = r"""
____ _  _ ____ ____ _  _ ____    ____ ____ _ _    ____ ___
|    |__| |___ |    |_/  [__     |___ |__| | |    |___ |  \
|___ |  | |___ |___ | \_ ___]    |    |  | | |___ |___ |__/
"""
WARNING_BANNER = r"""
@@@  @@@  @@@   @@@@@@   @@@@@@@   @@@  @@@  @@@  @@@  @@@   @@@@@@@@  @@@
@@@  @@@  @@@  @@@@@@@@  @@@@@@@@  @@@@ @@@  @@@  @@@@ @@@  @@@@@@@@@  @@@
@@!  @@!  @@!  @@!  @@@  @@!  @@@  @@!@!@@@  @@!  @@!@!@@@  !@@        @@!
!@!  !@!  !@!  !@!  @!@  !@!  @!@  !@!!@!@!  !@!  !@!!@!@!  !@!        !@
@!!  !!@  @!@  @!@!@!@!  @!@!!@!   @!@ !!@!  !!@  @!@ !!@!  !@! @!@!@  @!@
!@!  !!!  !@!  !!!@!!!!  !!@!@!    !@!  !!!  !!!  !@!  !!!  !!! !!@!!  !!!
!!:  !!:  !!:  !!:  !!!  !!: :!!   !!:  !!!  !!:  !!:  !!!  :!!   !!:
:!:  :!:  :!:  :!:  !:!  :!:  !:!  :!:  !:!  :!:  :!:  !:!  :!:   !::  :!:
 :::: :: :::   ::   :::  ::   :::   ::   ::   ::   ::   ::   ::: ::::   ::
  :: :  : :     :   : :   :   : :  ::    :   :    ::    :    :: :: :   :::
"""
MUSHROOM = r"""
    {}     _.-^^---....,,---;
     _--/                  `--_
    <                        >)
    |{}        {}KA-BOOM! {}       {} |
     \._                   _./
        ```--{}{}. . , ; .{}{}--'''{}
              {}| |   |
           {}{}.-={}{}||  | |{}{}=-.{}{}
           {}{}`-=#$%&%$#=-'{}{}
              | ;  :|
     {}_____{}.,-#%&$@%#&#~,.{}_____
         {}COMMAND  ACCEPTED{}
"""

INDICATOR_TYPES = {
    "hash_md5" : "md5",
    "hash_sha256" : "sha256",
    "hash_sha1" : "sha1",
    "hash_imphash" : "imphash",
    "file_name" : "filename",
    "file_path" : "filename",
    "url" : "url",
    "mutex_name" : "mutex",
    "bitcoin_address" : "btc",
    "coin_address" : "bic",
    "email_address" : "email-reply-to",
    "email_subject" : "email-subject",
    "registry" : "regkey",
    "device_name" : "target-machine",
    "domain" : "domain",
    "campaign_id" : "campaign-id",
    "ip_address" : "ip-src",
    "service_name" : "windows-service-name",
    "user_agent" : "user-agent",
    "port" : "port",
    # These are outstanding
    "password" : "",
    "username" : "",
    "x509_serial" : "",
    "x509_subject" : "",
}
