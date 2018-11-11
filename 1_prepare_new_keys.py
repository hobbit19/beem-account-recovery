from beem import Steem
from beemgraphenebase.account import PrivateKey, PasswordKey
from argparse import ArgumentParser
from beem.account import Account
from prettytable import PrettyTable
from getpass import getpass

parser = ArgumentParser()
parser.add_argument("account", type=str, nargs=1,
                    help="Name of the to-be-recovered account")
parser.add_argument("-c", "--custom-password", default=False,
                    action="store_true", help="Set a custom string "
                    "as password instead of a randomly generated "
                    "one. Setting this flag will ask for a password "
                    "while running.")
parser.add_argument("-n", "--node", type=str, help="Optional: custom "
                    "node URL", default=None)
args = parser.parse_args()

stm = Steem(node=args.node)
# Acccount() call to make sure the to-be-recovered account actually exists
account =  Account(args.account[0], steem_instance=stm)
if account.get_owner_history() == []:
    print("\n**WARNING**: @%s has an empty owner history - recovering "
          "this account won't be possible!\n" % (account['name']))


#####################################################################
# Ask or generate a new master password
#####################################################################
if args.custom_password:
    new_password = getpass("Enter new master password for %s: " %
                           (account['name']))
    repMasterPwd = getpass("Repeat new master password for %s: " %
                           (account['name']))
    if new_password != repMasterPwd:
        raise ValueError("The passwords do not match!")
else:
    new_password = "P" + str(PrivateKey(prefix=stm.prefix))

#####################################################################
# Derive the new keys
#####################################################################
owner = PasswordKey(account['name'], new_password, role='owner',
                    prefix=stm.prefix)
active = PasswordKey(account['name'], new_password, role='active',
                     prefix=stm.prefix)
posting = PasswordKey(account['name'], new_password, role='posting',
                      prefix=stm.prefix)
memo = PasswordKey(account['name'], new_password, role='memo',
                   prefix=stm.prefix)

#####################################################################
# Print results
#####################################################################
print("\n1.) Store the new master password and keys safely!")
if not args.custom_password:
    t = PrettyTable(['New PRIVATE keys', \
                     'DO NOT PUBLISH OR FORWARD, STORE SAFELY!'])
    t.add_row(['Account', account['name']])
    t.add_row(['New private master password', new_password])
    t.add_row(['New private active key', active.get_private()])
    t.add_row(['New private posting key', posting.get_private()])
    t.add_row(['New private memo key', memo.get_private()])
    print(t)

print("\n2.) Make sure you stored the new password and keys safely!")

print("\n3.) Forward the new PUBLIC owner key to your recovery account:")
t = PrettyTable(['New PUBLIC owner key', \
                     'Forward this to your recovery partner'])
t.add_row(["Account", account['name']])
t.add_row(["New public owner key", format(owner.get_public(),
                                          stm.prefix)])
print(t)
