import json
from beembase import operations
from beem.account import Account
from beemgraphenebase.account import PasswordKey
from beem.transactionbuilder import TransactionBuilder
from beem import Steem
from argparse import ArgumentParser
from getpass import getpass

parser = ArgumentParser()
parser.add_argument("account", type=str, nargs=1,
                    help="Name of the to-be-recovered account")
parser.add_argument("-d", "--dry-mode", default=False, action="store_true",
                    help="Dry mode, don't send any operation to the blockchain")
parser.add_argument("-n", "--node", type=str, help="Optional: custom "
                    "node URL", default=None)
args = parser.parse_args()

stm = Steem(node=args.node, nobroadcast=args.dry_mode)
acc = Account(args.account[0], steem_instance=stm)


#####################################################################
# ask & verify the old owner key
#####################################################################
old_priv_owner_key = getpass("Enter the old master password or owner "
                             "key for @%s: " % (acc['name']))
try:
    old_pk = PrivateKey(old_priv_owner_key, prefix=stm.prefix)
    old_public_owner_key = format(old_pk.get_public(), stm.prefix)
except Exception:
    # not a PrivateKey -> treat as master password
    old_pk = PasswordKey(acc['name'], old_priv_owner_key, role="owner",
                         prefix=stm.prefix)
    old_priv_owner_key = str(old_pk.get_private())
    old_public_owner_key = format(old_pk.get_public(), stm.prefix)


#####################################################################
# get the new password to prepare all new keys
#####################################################################
new_pwd = getpass("Enter the new master password for @%s: " %
                  (acc['name']))
key_auths = {}
for role in ['owner', 'active', 'posting', 'memo']:
    pk = PasswordKey(acc['name'], new_pwd, role=role)
    key_auths[role] = format(pk.get_public_key(), stm.prefix)
    if role == 'owner':
        new_priv_owner_key = str(pk.get_private())


#####################################################################
# Assemble the account recovery operation
#####################################################################
recent_owner_authority = {
    "key_auths": [[old_public_owner_key, 1]],
    "account_auths": [],
    "weight_threshold": 1,
    "prefix": stm.prefix
    }
new_owner_authority = {
    "key_auths": [[key_auths['owner'], 1]],
    "account_auths": [],
    "weight_threshold": 1,
    "prefix": stm.prefix
    }
op = operations.Recover_account(**{
    'account_to_recover': acc['name'],
    'new_owner_authority': new_owner_authority,
    'recent_owner_authority': recent_owner_authority,
    'extensions': [],
    "prefix": stm.prefix})


#####################################################################
# Send the recovery operations to the blockchain
#####################################################################
tb = TransactionBuilder(steem_instance=stm)
tb.appendOps([op])
tb.appendWif(new_priv_owner_key)
tb.appendWif(old_priv_owner_key)
tb.sign()
result = tb.broadcast()
if args.dry_mode:
    print("The following operation would have been sent:")
else:
    print("SUCCESS: @%s recovered:" % (acc['name']))
print(json.dumps(result, indent=2))


#####################################################################
# Assemble the account update operation
#####################################################################
op = operations.Account_update(**{
    "account": acc["name"],
    'active': {
        'account_auths': [],
        'key_auths': [[key_auths['active'], 1]],
        "address_auths": [],
        'weight_threshold': 1,
        'prefix': stm.prefix},
    'posting': {
        'account_auths': acc['posting']['account_auths'],
        'key_auths': [[key_auths['posting'], 1]],
        "address_auths": [],
        'weight_threshold': 1,
        'prefix': stm.prefix},
    'memo_key': key_auths['memo'],
    "json_metadata": acc['json_metadata'],
    "prefix": stm.prefix})

#####################################################################
# Send the recovery operations to the blockchain
#####################################################################
tb = TransactionBuilder(steem_instance=stm)
tb.appendOps([op])
tb.appendWif(new_priv_owner_key)
tb.sign()
result = tb.broadcast()
if args.dry_mode:
    print("The following operation would have been sent:")
else:
    print("SUCCESS: @%s updated:" % (acc['name']))
print(json.dumps(result, indent=2))
