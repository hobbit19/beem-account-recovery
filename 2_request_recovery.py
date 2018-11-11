from beem import Steem
from beem.account import Account
from beembase import operations
from beemgraphenebase.account import PasswordKey, PublicKey, PrivateKey
from beem.transactionbuilder import TransactionBuilder
from argparse import ArgumentParser
from getpass import getpass
import json

parser = ArgumentParser()
parser.add_argument("-a", "--account-to-recover", type=str, required=True,
                    help="Name of the to-be-recovered account")
parser.add_argument("-r", "--recovery-account", type=str,
                    required=True, help="Name of the recovery account")
parser.add_argument("-d", "--dry-mode", default=False,
                    action="store_true", help="Dry mode, don't send "
                    "any operation to the blockchain")
parser.add_argument("-n", "--node", type=str, help="Optional: custom "
                    "node URL", default=None)
args = parser.parse_args()

stm = Steem(node=args.node, nobroadcast=args.dry_mode)
# Account() calls to make sure both accounts exits
Account(args.account_to_recover, steem_instance=stm)
Account(args.recovery_account, steem_instance=stm)


#####################################################################
# Ask and verify the new pubkey for the to-be-recovered account
#####################################################################
new_owner_key = getpass("Enter new PUBLIC owner key for @%s: " %
                        (args.account_to_recover))
# PublicKey call to make sure it is a valid public key
pk_validity_check = PublicKey(new_owner_key, prefix=stm.prefix)
if format(pk_validity_check, stm.prefix) != new_owner_key:
    raise ValueError("Invalid public owner key!")


#####################################################################
# Ask and verify the active key of the recovery account
#####################################################################
recovery_ak = getpass("Enter active key, owner key or master "
                      "password for @%s: " % (args.recovery_account))
try:
    pk_check = PrivateKey(recovery_ak, prefix=stm.prefix)
except Exception:
    # PrivateKey() failed - treat it as a master password
    pk = PasswordKey(args.recovery_account, recovery_ak,
                     role="active", prefix=stm.prefix)
    recovery_ak = str(pk.get_private())


#####################################################################
# Assemble the account recovery request operation
#####################################################################
new_owner_authority = {
    'key_auths': [[new_owner_key, 1]],
    'account_auths': [],
    'weight_threshold': 1,
    'prefix': stm.prefix
    }

op = operations.Request_account_recovery(**{
    'account_to_recover': args.account_to_recover,
    'recovery_account': args.recovery_account,
    'new_owner_authority': new_owner_authority,
    'extensions': [],
    'prefix': stm.prefix
})


#####################################################################
# Send the operation to the blockchain
#####################################################################
tb = TransactionBuilder(steem_instance=stm)
tb.appendOps([op])
tb.appendWif(recovery_ak)
tb.sign()
result = tb.broadcast()
if args.dry_mode:
    print("The following operation would have been sent:")
else:
    print("SUCCESS: @%s requested account recovery for @%s:" %
          (args.recovery_account, args.account_to_recover))
print(json.dumps(result, indent=2))
